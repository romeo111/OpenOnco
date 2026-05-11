#!/usr/bin/env python3
"""Install git hooks from scripts/hooks/ into .git/hooks/.

Usage:
    python scripts/install_hooks.py

Run this once after cloning or when hooks are updated.
"""

import shutil
import stat
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).parent.parent
    hooks_src = repo_root / "scripts" / "hooks"

    # Resolve .git — could be a directory (main worktree) or a file
    # (linked worktree pointing to the real .git).
    git_entry = repo_root / ".git"
    if git_entry.is_file():
        # Worktree: .git is "gitdir: /path/to/real/.git/worktrees/X"
        # We want the main .git dir which is two levels up from the worktree dir.
        gitdir_line = git_entry.read_text(encoding="utf-8").strip()
        if gitdir_line.startswith("gitdir:"):
            worktree_gitdir = Path(gitdir_line[len("gitdir:"):].strip())
            # worktrees/X → two parents up = main .git dir
            real_git = worktree_gitdir.parent.parent
        else:
            real_git = git_entry.parent / ".git"
    else:
        real_git = git_entry

    hooks_dst = real_git / "hooks"

    if not hooks_src.is_dir():
        print(f"No hooks directory found at {hooks_src}", file=sys.stderr)
        sys.exit(1)
    if not hooks_dst.is_dir():
        print(f"Not inside a git repo (no .git/hooks at {hooks_dst})", file=sys.stderr)
        sys.exit(1)

    installed: list[str] = []
    skipped: list[str] = []

    for src in sorted(hooks_src.iterdir()):
        if src.name.endswith((".sample", ".md", ".txt", ".py")):
            skipped.append(src.name)
            continue
        dst = hooks_dst / src.name
        shutil.copy2(src, dst)
        # Make executable (required on POSIX; Windows ignores this but it's harmless).
        dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        installed.append(src.name)
        print(f"  installed  .git/hooks/{src.name}")

    if not installed:
        print("No hooks to install.")
    else:
        print(f"\n{len(installed)} hook(s) installed.")
    if skipped:
        print(f"{len(skipped)} file(s) skipped: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
