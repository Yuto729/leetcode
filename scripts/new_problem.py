#!/usr/bin/env python3
"""Fetch a LeetCode problem and scaffold leetcode/<slug>/main.md.

Usage:
    python3 scripts/new_problem.py 199
"""

import argparse
import datetime
import json
import re
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

USER_AGENT = "Mozilla/5.0 (compatible; leetcode-note-scaffold/1.0)"

ENTITIES = {
    "&nbsp;": " ",
    "&lt;": "<",
    "&gt;": ">",
    "&amp;": "&",
    "&quot;": '"',
    "&#39;": "'",
}


def fetch_json(url, data=None, headers=None):
    req_headers = {"User-Agent": USER_AGENT}
    req_headers.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=req_headers)
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode("utf-8"))


def find_title_slug(number):
    data = fetch_json("https://leetcode.com/api/problems/all/")
    for pair in data["stat_status_pairs"]:
        if pair["stat"]["frontend_question_id"] == number:
            return pair["stat"]["question__title_slug"]
    raise SystemExit(f"Problem number {number} not found")


def fetch_question(slug):
    query = """
    query problemContent($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
        content
        difficulty
        codeSnippets {
          langSlug
          code
        }
      }
    }
    """
    body = json.dumps({"query": query, "variables": {"titleSlug": slug}}).encode("utf-8")
    data = fetch_json(
        "https://leetcode.com/graphql",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    question = data.get("data", {}).get("question")
    if not question:
        raise SystemExit(f'No question data for "{slug}"')
    return question


def find_python_snippet(question):
    for snippet in question.get("codeSnippets") or []:
        if snippet["langSlug"] == "python3":
            return snippet["code"]
    return ""


def strip_constraints(html):
    m = re.search(r"<p>\s*(<strong>)?\s*Constraints:?\s*(</strong>)?\s*</p>", html, re.I)
    return html[: m.start()] if m else html


def html_to_markdown(html):
    text = html
    text = re.sub(r"&nbsp;|&lt;|&gt;|&amp;|&quot;|&#39;", lambda m: ENTITIES[m.group(0)], text)

    text = re.sub(r'<img[^>]*\balt="([^"]*)"[^>]*\bsrc="([^"]*)"[^>]*>', r"![\1](\2)", text, flags=re.I)
    text = re.sub(r'<img[^>]*\bsrc="([^"]*)"[^>]*\balt="([^"]*)"[^>]*>', r"![\2](\1)", text, flags=re.I)
    text = re.sub(r'<img[^>]*\bsrc="([^"]*)"[^>]*>', r"![](\1)", text, flags=re.I)

    text = re.sub(r"</?strong[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</?b[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</?em[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</?i[^>]*>", "", text, flags=re.I)
    text = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", text, flags=re.I | re.S)
    text = re.sub(r"<sup[^>]*>(.*?)</sup>", r"^\1", text, flags=re.I | re.S)

    text = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1\n", text, flags=re.I | re.S)
    text = re.sub(r"</?ul[^>]*>", "", text, flags=re.I)

    text = re.sub(r"</?span[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</?div[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</?pre[^>]*>", "", text, flags=re.I)

    text = re.sub(r"<p[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</p>", "\n\n", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)

    text = re.sub(r"<[^>]+>", "", text)

    text = "\n".join(line.strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(Example \d+:)\n\n+", r"\1\n", text)
    return text.strip()


def build_note(question, slug):
    date = datetime.date.today().isoformat()
    url = f"https://leetcode.com/problems/{slug}/"
    body = html_to_markdown(strip_constraints(question["content"]))
    signature = find_python_snippet(question)
    return f"""---
tags:
  - leetcode
date: {date}
url: {url}
difficulty: {question['difficulty']}
---

# {question['questionFrontendId']}. {question['title']}

{body}

## Step1

```py
{signature}
```

## Step2

## Step3
"""


def main():
    parser = argparse.ArgumentParser(description="Scaffold a LeetCode problem note")
    parser.add_argument("number", type=int, help="LeetCode problem number")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing main.md")
    args = parser.parse_args()

    slug = find_title_slug(args.number)
    question = fetch_question(slug)
    note = build_note(question, slug)

    target_dir = REPO_ROOT / slug
    target_file = target_dir / "main.md"
    if target_file.exists() and not args.force:
        raise SystemExit(f"{target_file} already exists. Use --force to overwrite.")

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(note, encoding="utf-8")
    print(f"Created {target_file}")


if __name__ == "__main__":
    main()
