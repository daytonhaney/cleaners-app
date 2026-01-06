#!/usr/bin/env python3
"""Simple script to create GitHub release"""

import os
import subprocess
from datetime import datetime


def create_release():
    """Create and push release with executable"""

    # Stage and commit changes
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(
        ["git", "commit", "-m", "Add executable and fix database issues"], check=True
    )

    # Create version tag
    version = f"v1.0.{datetime.now().strftime('%Y%m%d')}"
    subprocess.run(
        ["git", "tag", "-a", version, "-m", f"Release {version} - Executable version"],
        check=True,
    )

    # Push to GitHub
    subprocess.run(["git", "push", "origin", "main"], check=True)
    subprocess.run(["git", "push", "origin", version], check=True)

    print(f"✅ Pushed {version} to GitHub")
    print(f"📦 Executable ready in dist/ folder")

    # Instructions for manual GitHub release
    print("\n📝 To create GitHub release:")
    print(f"1. Go to: https://github.com/YOUR_USERNAME/cleaners-app/releases/new")
    print(f"2. Tag: {version}")
    print(f"3. Title: CleanersApp {version}")
    print(f"4. Upload files from dist/ folder:")

    for file in os.listdir("dist"):
        print(f"   - dist/{file}")


if __name__ == "__main__":
    create_release()
