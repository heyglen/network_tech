"""
Automated Plugin Releases

"""
import datetime
import json
import pathlib

import git
import click
import semver
from github import Github


REPO_NAME = 'network_tech'


def perform_release(release_type):    
    version = current_version()

    new_version = getattr(semver, f'bump_{release_type}')(version)

    message = create_message(new_version)
    version_control(version, new_version)
    github_release(REPO_NAME, new_version, message)


def current_version():
    file = str(pathlib.Path() / 'messages.json')
    with open(file) as open_file:
        messages_index = json.load(open_file)

    current_version = '0.1.0'
    for version in messages_index:
        if version == 'install':
            continue
        current_version = semver.max_ver(current_version, version)
    return current_version


def create_message(version):
    date = datetime.datetime.now().strftime('%Y.%m.%d')

    messages_directory = pathlib.Path() / 'messages' 
    message = (messages_directory / 'head.md').read_text()

    message = message.replace('{{version}}', version)
    message = message.replace('{{date}}', date)

    (messages_directory / f'{version}.md').write_text(message)
    (messages_directory / 'head.md').write_text("""# [{{version}}] - {{date}}\n\n""")

    file_name = str(pathlib.Path() / 'messages.json')
    with open(file_name) as open_file:
        messages_index = json.load(open_file)

    messages_index[version] = f'messages/{version}.md'
    with open(file_name, "w") as open_file:
        json.dump(messages_index, open_file, indent=4)

    return message


def version_control(old_version, new_version):
    commit_message = f'{old_version} -> {new_version}'
    directory = str(pathlib.Path())

    repo = git.Repo(directory)
    message_path = str(pathlib.Path() / 'messages' / f'{new_version}.md')

    repo.git.add(message_path)
    repo.git.commit('-a', '-m', commit_message)
    repo.create_tag(new_version)

    repo.git.push('origin', 'master', tags=True)


def github_release(repo_name, version, message):

    access_token = (pathlib.Path().home() / '.github_access_token').read_text()

    github = Github(access_token)

    repo = github.get_user().get_repo(repo_name)

    repo.create_git_release(version, name=version, message=message)


release_group = click.Group('release')


@release_group.command()
def patch():
    perform_release('patch')


@release_group.command()
def minor():
    perform_release('minor')


@release_group.command()
def major():
    perform_release('major')


release_group()