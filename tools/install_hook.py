"""Install the pre-commit hook into .git/hooks/.

Run from repo root:
  python tools/install_hook.py
"""
import os
import shutil
import stat
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    src = repo_root / ".githooks" / "pre-commit"
    dst = repo_root / ".git" / "hooks" / "pre-commit"

    if not src.exists():
        print(f"source hook not found: {src}", file=sys.stderr)
        return 1
    if not dst.parent.exists():
        print(
            f".git/hooks not found at {dst.parent} — is this a git repo?",
            file=sys.stderr,
        )
        return 1

    shutil.copy(src, dst)

    # Make executable on POSIX. On Windows, Git Bash invokes the hook via sh,
    # so executable bit is informational only.
    if os.name != "nt":
        st = dst.stat()
        dst.chmod(st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    print(f"installed pre-commit hook: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
