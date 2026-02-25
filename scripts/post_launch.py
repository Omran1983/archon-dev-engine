#!/usr/bin/env python3
"""
ARCHON Launch Post Automator
=============================
Posts ARCHON v0.1.0 launch content to X (Twitter), LinkedIn, and Cursor Forum.

SETUP:
  1. Copy .env.example to .env and fill in your API keys.
  2. pip install requests python-dotenv tweepy
  3. python post_launch.py --platform all
     OR
     python post_launch.py --platform x
     python post_launch.py --platform linkedin
     python post_launch.py --platform cursor
"""

import os
import sys
import argparse
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# ─── X (TWITTER) ────────────────────────────────────────────────────────────

X_THREAD = [
    """AI can generate backend code in seconds.
It can also introduce production instability just as fast.

Most AI-generated backends include:
• Blocking I/O in async routes
• Inconsistent JSON responses
• Hardcoded secrets
• Silent config failures

Today we're launching ARCHON Dev Engine 🧵""",

    """ARCHON is a Cursor plugin that enforces production-grade backend discipline in real time.

Not a linter. A guardrail layer.

If AI suggests blocking code inside an async route → ARCHON vetoes it.
If a secret is hardcoded → ARCHON blocks the commit.""",

    """v0.1.0 includes:
• Async-First enforcement
• Structured JSON output validation
• Deterministic config checks
• Architecture scoring CLI
• Optional strict Git pre-commit guard

No external runtime. Drop it into any Cursor project.""",

    """We built ARCHON after repeatedly reviewing AI-generated backend code that looked correct but failed architectural discipline.

Speed is easy.
Production integrity isn't.
ARCHON enforces it automatically.""",

    """Open alpha — first 25 teams get early access to Pro enforcement features.

Drop a ⭐ or open an issue:
https://github.com/Omran1983/archon-dev-engine

Looking for feedback on async detection precision.""",
]

LINKEDIN_POST = """Stop AI from introducing backend fragility.

Most teams use AI to write code faster.
Few enforce architectural discipline on AI-generated backends.

Common issues we observed:
- Blocking I/O inside async routes
- Inconsistent API response structures
- Hardcoded configuration values
- Silent fallback behavior

We built ARCHON Dev Engine to enforce backend discipline inside Cursor.

v0.1.0 ships with:
→ Async-first enforcement
→ Structured output validation
→ Deterministic config checks
→ Optional strict Git-level guard

Open alpha now available.
First 25 teams get early access to Pro features.

GitHub: https://github.com/Omran1983/archon-dev-engine

Looking specifically for feedback on Async enforcement precision.

#AI #SoftwareEngineering #Cursor #Backend #Developer"""

CURSOR_FORUM = {
    "title": "ARCHON – Async enforcement for AI-generated backends",
    "body": """Hey all,

After reviewing a lot of AI-generated backend code, we noticed recurring async discipline issues: blocking I/O inside routes, mixed response structures, config leaks.

We built **ARCHON** as a Cursor plugin to enforce production-grade discipline automatically.

**v0.1.0 scope:**
- Async-First rule enforcement
- Structured JSON validation
- Deterministic config checks
- Optional strict Git pre-commit guard
- Architecture scoring CLI (`python scripts/score.py`)

No external runtime required. Clone the repo and load it as a Cursor plugin.

**Repo:** https://github.com/Omran1983/archon-dev-engine

Looking specifically for feedback on rule precision and false positives in async detection. If you hit a false positive, open an issue — we're on a 48-hour patch cycle.""",
    "category": 9  # "Share" category on forum.cursor.com — verify before posting
}


# ─── X POSTING ──────────────────────────────────────────────────────────────

def post_x_thread():
    """Post the X thread using Twitter API v2."""
    import tweepy

    client = tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    )

    prev_id = None
    for i, post in enumerate(X_THREAD):
        try:
            if prev_id:
                resp = client.create_tweet(text=post, in_reply_to_tweet_id=prev_id)
            else:
                resp = client.create_tweet(text=post)
            prev_id = resp.data["id"]
            print(f"[X] Post {i+1}/{len(X_THREAD)} published. ID: {prev_id}")
            time.sleep(2)  # Avoid rate limits
        except Exception as e:
            print(f"[X] ERROR on post {i+1}: {e}")
            return False
    return True


# ─── LINKEDIN POSTING ────────────────────────────────────────────────────────

def post_linkedin():
    """Post to LinkedIn using the LinkedIn API v2."""
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Get your person URN
    r = requests.get("https://api.linkedin.com/v2/userinfo",
                     headers={"Authorization": f"Bearer {token}"})
    if not r.ok:
        print(f"[LinkedIn] Failed to get user: {r.text}")
        return False

    person_urn = f"urn:li:person:{r.json()['sub']}"

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": LINKEDIN_POST},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    r = requests.post("https://api.linkedin.com/v2/ugcPosts",
                      headers=headers, json=payload)
    if r.ok:
        print(f"[LinkedIn] Post published successfully.")
        return True
    else:
        print(f"[LinkedIn] ERROR: {r.status_code} {r.text}")
        return False


# ─── CURSOR FORUM POSTING ────────────────────────────────────────────────────

def post_cursor_forum():
    """Post to Cursor Forum (Discourse) via API."""
    base_url = os.getenv("CURSOR_FORUM_URL", "https://forum.cursor.com")
    api_key  = os.getenv("CURSOR_FORUM_API_KEY")
    username = os.getenv("CURSOR_FORUM_USERNAME")

    headers = {
        "Api-Key": api_key,
        "Api-Username": username,
        "Content-Type": "application/json"
    }

    payload = {
        "title":    CURSOR_FORUM["title"],
        "raw":      CURSOR_FORUM["body"],
        "category": CURSOR_FORUM["category"],
    }

    r = requests.post(f"{base_url}/posts.json", headers=headers, json=payload)
    if r.ok:
        slug = r.json().get("topic_slug")
        print(f"[Forum] Post created: {base_url}/t/{slug}")
        return True
    else:
        print(f"[Forum] ERROR: {r.status_code} {r.text}")
        return False


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ARCHON Launch Post Automator")
    parser.add_argument("--platform", choices=["x", "linkedin", "cursor", "all"],
                        default="all", help="Platform to post to")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print content without posting")
    args = parser.parse_args()

    if args.dry_run:
        print("\n--- X THREAD (DRY RUN) ---")
        for i, p in enumerate(X_THREAD):
            print(f"\n[POST {i+1}]\n{p}")
        print("\n--- LINKEDIN (DRY RUN) ---")
        print(LINKEDIN_POST)
        print("\n--- CURSOR FORUM (DRY RUN) ---")
        print(f"Title: {CURSOR_FORUM['title']}\n{CURSOR_FORUM['body']}")
        return

    if args.platform in ("x", "all"):
        print("\n--- Posting X Thread ---")
        try:
            import tweepy
        except ImportError:
            print("[X] ERROR: tweepy not installed. Run: pip install tweepy")
        else:
            post_x_thread()

    if args.platform in ("linkedin", "all"):
        print("\n--- Posting LinkedIn ---")
        post_linkedin()

    if args.platform in ("cursor", "all"):
        print("\n--- Posting Cursor Forum ---")
        post_cursor_forum()

    print("\nDone.")


if __name__ == "__main__":
    main()
