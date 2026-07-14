#!/usr/bin/env python3
"""
Medium Feed Parser

Fetches the latest posts from the Medium feed and updates the
"On my blog" section of README.md.

Dependencies:
    - https://github.com/kurtmckee/feedparser
"""

import os
import re

import feedparser

FEED_URL = "https://medium.com/feed/@johnidouglasmarangon"
README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
SECTION_HEADING = "## ✍️ On my blog:"
POST_LIMIT = 10


def fetch_posts(limit=POST_LIMIT):
    data = feedparser.parse(FEED_URL)
    items = data["items"][:limit]

    return [
        {"title": i["title"], "publishedAt": i["published"], "link": i["link"].split("?")[0]}
        for i in items
    ]


def render_section(posts):
    lines = [SECTION_HEADING, ""]
    lines += [f"- [{post['title']}]({post['link']})" for post in posts]
    return "\n".join(lines)


def update_readme(posts, readme_path=README_PATH):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        rf"{re.escape(SECTION_HEADING)}\n(?:.*\n)*?(?=\n##|\Z)",
        re.MULTILINE,
    )
    new_section = render_section(posts) + "\n"

    if pattern.search(content):
        content = pattern.sub(new_section, content, count=1)
    else:
        content = content.rstrip("\n") + "\n\n" + new_section

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    posts = fetch_posts()
    update_readme(posts)
    print(f"Updated {SECTION_HEADING} with {len(posts)} posts in {README_PATH}")


if __name__ == "__main__":
    main()
