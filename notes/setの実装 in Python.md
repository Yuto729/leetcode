---
tags:
  - leetcode
  - python
  - cs/data-structure
  - algorithm/hash-table
  - cs/internals
---

セットの挿入について解説する

- オープンアドレッシングを用いている。

以下がセットに要素を追加するコアな関数

- input: セットオブジェクト, key, hash値
- 初期位置の計算: hash値をテーブルサイズで割った位置
- while do文内でハッシュが衝突するかしないかを判断. 衝突しない場合は`go to`でループを抜ける. 衝突した場合は`probes`が0になるまで連続したスロットを調べる.
- `probes`が0になっても衝突する場合, 再ハッシュして新しい場所を探す.
- 空きスロットがない場合, リサイズをする. リサイズはテーブルの60%が埋まったらされるっぽい. リサイズの際は全エントリでハッシュ値を計算し直す.
- setの挿入はO(1)と略されるが, バケットの占有率が上がってくると参照, 削除の効率が低下するのでコストが上がりすぎないところでリサイズが必要なのだと思われる.（数理工学社の教科書に書いてある）

```c
set_add_entry_takeref(PySetObject *so, PyObject *key, Py_hash_t hash)
{
    setentry *table;
    setentry *freeslot;
    setentry *entry;
    size_t perturb;
    size_t mask;
    size_t i;                       /* Unsigned for defined overflow behavior */
    int probes;
    int cmp;

  restart:
    
    /* 初期位置の計算 */ 
    mask = so->mask;
    /* hash % table_sizeと同じ計算. ビット演算は1クロックでできるので高速. 
    普通の除算は2桁クロックかかるらしい.*/
	  i = (size_t)hash & mask;
	  /* 削除済みスロットのアドレスを一時的に記録する*/
    freeslot = NULL;
    perturb = hash;

    while (1) {
        entry = &so->table[i];
        probes = (i + LINEAR_PROBES <= mask) ? LINEAR_PROBES: 0;
        do {
            if (entry->hash == 0 && entry->key == NULL)
            　　 /* hash=0は空であることを意味する.*/
                goto found_unused_or_dummy;
            if (entry->hash == hash) {
                PyObject *startkey = entry->key;
                assert(startkey != dummy);
                if (startkey == key)
		                /* 同一オブジェクトであるとき, setには追加しない */
                    goto found_active;
                if (PyUnicode_CheckExact(startkey)
                    && PyUnicode_CheckExact(key)
                    && unicode_eq(startkey, key))
                    /* 両方文字列のとき */
                    goto found_active;
                table = so->table;
                Py_INCREF(startkey);
                
                /* 上記以外のとき, __eq__メソッドを呼んで比較する. 遅め*/
                cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                Py_DECREF(startkey);
                if (cmp > 0)
                    goto found_active;
                if (cmp < 0)
                    goto comparison_error;
                if (table != so->table || entry->key != startkey)
                    goto restart;
                mask = so->mask;
            }
            else if (entry->hash == -1) {
		            /* hash = -1は削除済みであることを表す.*/
                assert (entry->key == dummy);
                freeslot = entry;
            }
            /* 衝突したとき: 連続したスロットを調べる. */
            entry++;
        } while (probes--);
        
        /* 再ハッシュして新しい位置に移動 */
        perturb >>= PERTURB_SHIFT;
        i = (i * 5 + 1 + perturb) & mask;
    }

  found_unused_or_dummy:
    if (freeslot == NULL)
        goto found_unused;
    FT_ATOMIC_STORE_SSIZE_RELAXED(so->used, so->used + 1);
    /* 削除済みスロットがあれば利用 */
    freeslot->key = key;
    freeslot->hash = hash;
    return 0;

  found_unused:
    so->fill++;
    FT_ATOMIC_STORE_SSIZE_RELAXED(so->used, so->used + 1);
    entry->key = key;
    entry->hash = hash;
    if ((size_t)so->fill*5 < mask*3)
        return 0;
    return set_table_resize(so, so->used>50000 ? so->used*2 : so->used*4);

  found_active:
    /* <https://docs.python.org/ja/3.10/c-api/refcounting.html?highlight=py_decref#c.Py_DECREF>
    keyオブジェクトの参照カウンタを減らす. 
    */
    Py_DECREF(key);
    return 0;

  comparison_error:
    Py_DECREF(key);
    return -1;
}
```