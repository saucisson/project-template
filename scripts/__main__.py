"""Command-line entry point: ``python -m scripts <command>`` (ADR-0021).

Make stays THE agent surface: every subcommand below matches a make
target one-to-one (ADR-0021). This dispatcher only wires the
subcommands to their domain modules; it owns no protocol of its own.
"""

import argparse
import sys
from typing import TYPE_CHECKING

from scripts import ci, claims, day, merge, night, pulls, review, session
from scripts._shared import load_environment_file

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

COMMAND_MODULES = (claims, pulls, merge, ci, review, session, day, night)


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the CLI: one subparser per driver subcommand."""
    argument_parser = argparse.ArgumentParser(
        prog="scripts",
        description="Project drivers: one subcommand per make target (ADR-0021).",
    )
    subparsers = argument_parser.add_subparsers(dest="command", required=True)
    for module in COMMAND_MODULES:
        module.register(subparsers)
    return argument_parser


def main(*, command_line_arguments: Sequence[str]) -> int:
    """Entry point: environment loaded once, subcommand dispatched."""
    load_environment_file()
    arguments = build_argument_parser().parse_args(command_line_arguments)
    runner: Callable[[argparse.Namespace], int] = arguments.runner
    return runner(arguments)


if __name__ == "__main__":
    sys.exit(main(command_line_arguments=sys.argv[1:]))
