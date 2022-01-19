"""This is a simplistic regression test framework for the generator."""
import subprocess
import os
from generatorcore.generator import Generator

CURRENT_PUBLIC_DATA_HASH = "c64c73ff852777ba0fdab2e9a6d7b44eca847af6"

CURRENT_PROPRIETARY_DATA_HASH = "b8dc6c23d1bf7372693887ea0856cd74d8bfc263"


def get_git_hash(path_to_repo: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
        cwd=path_to_repo,
    ).stdout.strip()


def root_of_this_repo() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout.strip()


def test_public_repo_has_not_been_changed():
    hash = get_git_hash(os.path.join(root_of_this_repo(), "data", "public"))
    assert (
        hash == CURRENT_PUBLIC_DATA_HASH
    ), "Have you changed the public data repository on purpose? If so update the hash above."


def test_private_repo_has_not_been_changed():
    hash = get_git_hash(os.path.join(root_of_this_repo(), "data", "proprietary"))
    assert (
        hash == CURRENT_PROPRIETARY_DATA_HASH
    ), "Have you changed the proprietary data repository on purpose? If so update the hash above."


def test_end_to_end_goettingen():
    g = Generator()
    # TODO: Check that the code produces the same result as a previos run
