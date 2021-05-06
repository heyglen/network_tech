"""
Automated Plugin Releases

"""
import datetime
import json
import pathlib

import click
import git
import semver
from github import Github

REPO_NAME = "network_tech"


class Version:
    _setup_file_path = standard.configuration_path

    @classmethod
    def _get_config(cls):
        config = configparser.ConfigParser()
        config.read(cls._setup_file_path)
        return config

    @classmethod
    def current(cls):
        file = str(pathlib.Path() / "messages.json")
        with open(file) as open_file:
            messages_index = json.load(open_file)

        current_version = (0, 1, 0)

        for version in messages_index:
            if version == "install":
                continue
            major, minor, patch = [int(v) for v in version.split(".")]

            if major < current_version[0]:
                continue

            if minor < current_version[1]:
                continue

            if patch < current_version[2]:
                continue

            current_version = (major, minor, patch)

        return ".".join(current_version)

    @classmethod
    def major(cls):
        return cls.bump("major")

    @classmethod
    def minor(cls):
        return cls.bump("minor")

    @classmethod
    def patch(cls):
        return cls.bump("patch")

    @classmethod
    def bump(cls, part):
        part = part.lower()
        if part not in ("major", "minor", "patch"):
            raise ValueError(f'Unknown version bump "{part}"')
        current_version = cls.current()
        major, minor, patch = [int(v) for v in current_version.split(".")]
        if part == "major":
            major += 1
        elif part == "minor":
            minor += 1
        elif part == "patch":
            patch += 1
        return ".".join([major, minor, patch])


def perform_release(release_type):
    current_version = Version.current()

    new_version = getattr(Version, release_type)()
    print(current_version)
    print(new_version)
    return
    message = create_message(new_version)
    version_control(version, new_version)
    github_release(REPO_NAME, new_version, message)


def create_message(version):
    date = datetime.datetime.now().strftime("%Y.%m.%d")

    messages_directory = pathlib.Path() / "messages"
    message = (messages_directory / "head.md").read_text()

    message = message.replace("{{version}}", version)
    message = message.replace("{{date}}", date)

    (messages_directory / f"{version}.md").write_text(message)
    (messages_directory / "head.md").write_text("""# [{{version}}] - {{date}}\n\n""")

    file_name = str(pathlib.Path() / "messages.json")
    with open(file_name) as open_file:
        messages_index = json.load(open_file)

    messages_index[version] = f"messages/{version}.md"
    with open(file_name, "w") as open_file:
        json.dump(messages_index, open_file, indent=4)

    return message


def version_control(old_version, new_version):
    commit_message = f"{old_version} -> {new_version}"
    directory = str(pathlib.Path())

    repo = git.Repo(directory)
    message_path = str(pathlib.Path() / "messages" / f"{new_version}.md")

    repo.git.add(message_path)
    repo.git.commit("-a", "-m", commit_message)
    repo.create_tag(new_version)

    repo.git.push("origin", "master", tags=True)


def github_release(repo_name, version, message):

    access_token = (pathlib.Path().home() / ".github_access_token").read_text()

    github = Github(access_token)

    repo = github.get_user().get_repo(repo_name)

    repo.create_git_release(version, name=version, message=message)


release_group = click.Group("release")


@release_group.command()
def patch():
    perform_release("patch")


@release_group.command()
def minor():
    perform_release("minor")


@release_group.command()
def major():
    perform_release("major")


release_group()
