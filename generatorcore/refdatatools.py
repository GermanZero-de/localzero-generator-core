"""module refdatatools -- This contains code to manage the data repo(s).

   This module is not needed to run the generator itself. In particular
   we want to avoid requiring a git installation to run the generator itself.

   It should always be sufficient to have a copy of the working directories in
   the right place.

   That said if you actually develop on the generator, you invariably will need
   git. And as you will have to carefully manage the state of 3 separate
   repositories (2 data + 1 code), we have written some code to help with that.
"""
# pyright: strict
import os.path
import subprocess
from dataclasses import dataclass
import typing

from . import refdata

MAIN_REPOS = {
    "public": "github.com/GermanZero-de/localzero-data-public",
    "proprietary": "github.com/GermanZero-de/localzero-data-proprietary",
}

PUBLIC_OR_PROPRIETARY = typing.Literal["public", "proprietary"]


def pull(datadir: str, repo: PUBLIC_OR_PROPRIETARY, pa_token: str | None = None):
    if pa_token is not None:
        url = "https://" + pa_token + "@" + MAIN_REPOS[repo]
    else:
        url = "https://" + MAIN_REPOS[repo]

    subprocess.run(
        ["git", "pull", "--ff-only", url], check=True, cwd=os.path.join(datadir, repo)
    )


def clone(
    datadir: str,
    repo: PUBLIC_OR_PROPRIETARY,
    pa_token: str | None = None,
):
    """This function assumes that there is not data repository already in the datadir."""
    if pa_token is not None:
        url = "https://" + pa_token + "@" + MAIN_REPOS[repo]
    else:
        url = "https://" + MAIN_REPOS[repo]

    subprocess.run(["git", "clone", url, repo], check=True, cwd=datadir)


def checkout(datadir: str, repo: typing.Literal["public", "proprietary"], rev: str):
    subprocess.run(
        ["git", "checkout", rev], check=True, cwd=os.path.join(datadir, repo)
    )


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


def datadir() -> str:
    """This assumes we are somewhere in the code repository, but not in either
    the data or proprietary repo.
    Given that it will return absolute path to the data directory.
    """
    return os.path.normpath(os.path.join(root_of_this_repo(), "data"))


def is_repo_clean(path_to_repo: str) -> bool:
    # the output of git status --porcelain is guaranteed to be empty if the repository is clean
    porcelain = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        check=True,
        text=True,
        cwd=path_to_repo,
    ).stdout.strip()
    return porcelain == ""


@dataclass
class WorkingDirectoryStatus:
    is_clean: bool
    rev: str

    @classmethod
    def get(cls, path_to_repo: str) -> "WorkingDirectoryStatus":
        is_clean = is_repo_clean(path_to_repo)
        rev = get_git_hash(path_to_repo)
        return cls(is_clean=is_clean, rev=rev)


@dataclass
class DataDirStatus:
    production: refdata.Version
    public_status: WorkingDirectoryStatus
    proprietary_status: WorkingDirectoryStatus

    @classmethod
    def get(cls, datadir: str) -> "DataDirStatus":
        production = refdata.Version.load("production", datadir)
        public_status = WorkingDirectoryStatus.get(
            path_to_repo=os.path.join(datadir, "public")
        )
        proprietary_status = WorkingDirectoryStatus.get(
            path_to_repo=os.path.join(datadir, "proprietary")
        )
        return DataDirStatus(
            production=production,
            public_status=public_status,
            proprietary_status=proprietary_status,
        )

    def is_good(self):
        return (
            self.public_status.is_clean
            and self.proprietary_status.is_clean
            and self.production.public == self.public_status.rev
            and self.production.proprietary == self.proprietary_status.rev
        )
