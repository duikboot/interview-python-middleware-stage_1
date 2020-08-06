from functools import partial
from itertools import chain

from invoke import task

pprint = partial(print, "-" * 3)


LINE_LENGTH = "90"

CODE = ["."]
TESTS = ["tests"]
ADDITIONAL = []


def apply_paths(*args):
    return " ".join(chain.from_iterable(args))


@task
def sort_imports(c, check=False):
    """
    Sort imports.
    """
    ISORT_CMD = (
        f"isort {apply_paths(CODE, TESTS, ADDITIONAL)} "
        f"--recursive --atomic --quiet --apply --line-width {LINE_LENGTH}"
    )
    if check:
        result = c.run(ISORT_CMD + " --check")
        if result.stdout.startswith("ERROR"):
            exit(1)
    else:
        c.run(ISORT_CMD)


@task
def format_code(c, check=False):
    """Format code"""
    BLACK_CMD = (
        f"black {apply_paths(CODE, TESTS, ADDITIONAL)} " f"--line-length {LINE_LENGTH}"
    )
    if check:
        result = c.run(BLACK_CMD + " --check")
        if result.return_code != 0:
            exit(1)
    else:
        c.run(BLACK_CMD)


@task
def format(c, check=False):
    pprint("SORT IMPORTS:")
    sort_imports(c, check)

    pprint("FORMAT CODE:")
    format_code(c, check)
