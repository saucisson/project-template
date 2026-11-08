"""Daily integration driver: rebase daily onto origin/main (ADR-0020).

The merge flow is one-directional (ADR-0009): work lands in ``daily``
through reviewed pull requests, and the human merges ``daily`` into
``main`` at the end of the day. But ``main`` can also move WITHOUT
passing through ``daily``: a template sync the human commits on
``main``, a hotfix, a release. The branches then diverge, and until
now nothing could reconcile them: merging ``main`` into ``daily``
writes a merge commit (linear history forbids it), and a raw rebase
rewrites a protected branch - a force push outside any driver.

This driver is the one sanctioned path (ADR-0020):

- run it from a clean ``daily`` checkout, early in the day (right
  after ``make day-start``, before opening pull requests);
- ``daily`` already contains ``origin/main`` -> exit 0, nothing
  written;
- ``daily`` is strictly behind -> fast-forward, a normal push, no
  rewrite at all;
- diverged -> rebase ``daily`` onto ``origin/main``, verify the
  replayed ``daily`` contains ``origin/main`` and the same number of
  daily-only commits, then push with ``--force-with-lease``;
- a rebase conflict aborts the rebase and refuses (exit 1):
  resolving accepted ``main`` content against accepted ``daily``
  work is a human decision, never an unattended merge;
- ``main`` is never rewritten, and unattended (night) sessions never
  run this driver (ADR-0020).

Exit codes: 0 synced (or nothing to do), 1 refused (wrong branch,
dirty tree, conflict - nothing was written), 2 protocol failure
(daily restored, remote untouched).

Usage::

    make sync-daily
"""

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

DAILY_BRANCH_NAME = "daily"
MAIN_REMOTE_REFERENCE = "origin/main"

EXIT_CODE_SYNCED = 0
EXIT_CODE_REFUSED = 1
EXIT_CODE_PROTOCOL_FAILURE = 2


def run_git(*, arguments: Sequence[str]) -> subprocess.CompletedProcess:
    """Run one git command in the repository; the caller checks the exit."""
    return subprocess.run(
        ["git", *arguments],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def current_branch() -> str:
    """Return the checked-out branch name (or the empty detached state)."""
    return run_git(arguments=["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def working_tree_is_clean() -> bool:
    """Whether the working tree has no uncommitted or untracked change."""
    return run_git(arguments=["status", "--porcelain"]).stdout.strip() == ""


def remote_main_exists() -> bool:
    """Whether the remote main branch was fetched at all."""
    verification = run_git(
        arguments=["rev-parse", "--quiet", "--verify", f"refs/remotes/{MAIN_REMOTE_REFERENCE}"]
    )
    return verification.returncode == 0


def is_ancestor(*, ancestor: str, descendant: str) -> bool:
    """Whether ancestor is reachable from descendant."""
    return run_git(arguments=["merge-base", "--is-ancestor", ancestor, descendant]).returncode == 0


def daily_only_commit_count() -> int:
    """Count the commits daily has and origin/main lacks."""
    count_output = run_git(
        arguments=["rev-list", "--count", f"{MAIN_REMOTE_REFERENCE}..HEAD"]
    ).stdout.strip()
    return int(count_output)


def restore_daily(*, expected_head: str) -> None:
    """Put daily back where it was before the failed attempt."""
    run_git(arguments=["reset", "--hard", expected_head])


def precondition_exit_code(*, branch: str) -> int | None:
    """Refuse anything but a clean daily checkout; None means: proceed."""
    if branch != DAILY_BRANCH_NAME:
        print(
            f"Error: sync-daily runs from the {DAILY_BRANCH_NAME} checkout,"
            f" not from {branch or 'a detached head'} - it rewrites"
            f" {DAILY_BRANCH_NAME} only (ADR-0020).",
            file=sys.stderr,
        )
        return EXIT_CODE_REFUSED
    if not working_tree_is_clean():
        print(
            "Error: the working tree is not clean - commit or stash first:"
            " a rebase over a dirty tree is not honest glue (ADR-0020).",
            file=sys.stderr,
        )
        return EXIT_CODE_REFUSED
    return None


def fetch_origin() -> int:
    """Fetch the remote; stale refs are never a base for a rewrite."""
    fetch = run_git(arguments=["fetch", "origin"])
    if fetch.returncode == 0:
        return EXIT_CODE_SYNCED
    print(
        f"Error: could not fetch origin ({fetch.returncode}) - do not sync on stale references.",
        file=sys.stderr,
    )
    return EXIT_CODE_PROTOCOL_FAILURE


def push_daily(*, force: bool, previous_head: str) -> int:
    """Push daily; a refused push restores daily and fails the protocol."""
    arguments = (
        ["push", "--force-with-lease", "origin", DAILY_BRANCH_NAME]
        if force
        else ["push", "origin", DAILY_BRANCH_NAME]
    )
    pushed = run_git(arguments=arguments)
    if pushed.returncode == 0:
        return EXIT_CODE_SYNCED
    restore_daily(expected_head=previous_head)
    print(
        f"Error: the push of {DAILY_BRANCH_NAME} was refused"
        f" ({pushed.returncode}) - daily is restored locally, the remote"
        " was not touched.",
        file=sys.stderr,
    )
    return EXIT_CODE_PROTOCOL_FAILURE


def fast_forward_daily(*, previous_head: str) -> int:
    """Strictly behind: move daily to origin/main without any rewrite."""
    merged = run_git(arguments=["merge", "--ff-only", MAIN_REMOTE_REFERENCE])
    if merged.returncode != 0:
        restore_daily(expected_head=previous_head)
        print(
            "Error: the fast-forward onto origin/main failed - daily is"
            " restored, nothing was pushed.",
            file=sys.stderr,
        )
        return EXIT_CODE_PROTOCOL_FAILURE
    push_exit_code = push_daily(force=False, previous_head=previous_head)
    if push_exit_code == EXIT_CODE_SYNCED:
        print(
            f"{DAILY_BRANCH_NAME} was strictly behind: fast-forwarded onto"
            f" {MAIN_REMOTE_REFERENCE} and pushed - no commit was"
            " rewritten (ADR-0020)."
        )
    return push_exit_code


def rebase_daily_onto_main(*, previous_head: str, daily_only_before: int) -> int:
    """Diverged: replay daily onto origin/main, verify, lease-push."""
    rebased = run_git(arguments=["rebase", MAIN_REMOTE_REFERENCE])
    if rebased.returncode != 0:
        run_git(arguments=["rebase", "--abort"])
        print(
            "Error: rebasing daily onto origin/main hit a conflict - the"
            " rebase is aborted and daily is untouched. Resolving accepted"
            " main content against accepted daily work is a human decision:"
            " escalate it (needs-human), never merge it by hand (ADR-0020).",
            file=sys.stderr,
        )
        return EXIT_CODE_REFUSED
    if not is_ancestor(ancestor=MAIN_REMOTE_REFERENCE, descendant="HEAD"):
        restore_daily(expected_head=previous_head)
        print(
            "Error: the replayed daily does not contain origin/main -"
            " daily is restored, nothing was pushed.",
            file=sys.stderr,
        )
        return EXIT_CODE_PROTOCOL_FAILURE
    daily_only_after = daily_only_commit_count()
    if daily_only_after != daily_only_before:
        restore_daily(expected_head=previous_head)
        print(
            f"Error: the replay changed the daily-only commit count"
            f" ({daily_only_before} before, {daily_only_after} after) -"
            " daily is restored, nothing was pushed.",
            file=sys.stderr,
        )
        return EXIT_CODE_PROTOCOL_FAILURE
    push_exit_code = push_daily(force=True, previous_head=previous_head)
    if push_exit_code == EXIT_CODE_SYNCED:
        print(
            f"{DAILY_BRANCH_NAME} rebased onto {MAIN_REMOTE_REFERENCE}:"
            f" {daily_only_before} commit(s) replayed, pushed with"
            " --force-with-lease - main was not touched (ADR-0020)."
            " Local branches based on the old daily need a rebase before"
            " their pull request."
        )
    return push_exit_code


def main() -> int:
    """Entry point: clean daily checkout in, synced (or refused) out."""
    refusal_exit_code = precondition_exit_code(branch=current_branch())
    if refusal_exit_code is not None:
        return refusal_exit_code
    fetch_exit_code = fetch_origin()
    if fetch_exit_code != EXIT_CODE_SYNCED:
        return fetch_exit_code
    if not remote_main_exists():
        print(f"Nothing to sync: {MAIN_REMOTE_REFERENCE} does not exist on the remote yet.")
        return EXIT_CODE_SYNCED
    if is_ancestor(ancestor=MAIN_REMOTE_REFERENCE, descendant="HEAD"):
        print(f"{DAILY_BRANCH_NAME} already contains {MAIN_REMOTE_REFERENCE} - nothing to sync.")
        return EXIT_CODE_SYNCED
    previous_head = run_git(arguments=["rev-parse", "HEAD"]).stdout.strip()
    if is_ancestor(ancestor="HEAD", descendant=MAIN_REMOTE_REFERENCE):
        return fast_forward_daily(previous_head=previous_head)
    return rebase_daily_onto_main(
        previous_head=previous_head,
        daily_only_before=daily_only_commit_count(),
    )


if __name__ == "__main__":
    sys.exit(main())
