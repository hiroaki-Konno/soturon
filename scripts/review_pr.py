#!/usr/bin/env python3
"""PRのdiffをClaudeでレビューしてGitHubにコメントを投稿する。"""

import json
import os
import sys
import urllib.request

import anthropic

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]

_GH_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

MAX_DIFF_BYTES = 100_000


def get_pr_diff() -> str:
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    req = urllib.request.Request(
        url,
        headers={**_GH_HEADERS, "Accept": "application/vnd.github.v3.diff"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="replace")


def review_with_claude(diff: str) -> str:
    if len(diff) > MAX_DIFF_BYTES:
        diff = diff[:MAX_DIFF_BYTES] + "\n... (diffが長いため省略)"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": (
                    "以下のPull Requestのdiffをレビューしてください。\n\n"
                    "コードの品質・バグ・セキュリティ・可読性の観点でコメントをMarkdownで"
                    "日本語で出力してください。\n"
                    "問題がなければ「問題なし」と一言だけ述べてください。\n\n"
                    f"```diff\n{diff}\n```"
                ),
            }
        ],
    )
    return message.content[0].text


def post_comment(body: str) -> None:
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    payload = json.dumps({"body": f"## AIレビュー（Claude）\n\n{body}"}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={**_GH_HEADERS, "Accept": "application/vnd.github+json", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req):
        pass


def main() -> None:
    diff = get_pr_diff()
    if not diff.strip():
        print("diffが空のためスキップします")
        sys.exit(0)

    review = review_with_claude(diff)
    post_comment(review)
    print("レビューを投稿しました")


if __name__ == "__main__":
    main()
