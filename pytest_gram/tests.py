import re

from git import Repo


def test_commit_message_is_matched(feature_commit_msg_template, repo_path):
    repo = Repo(str(repo_path))
    head_commit = repo.head.commit
    message = head_commit.message

    pattern = re.compile(feature_commit_msg_template)
    match = pattern.match(message)

    assert bool(match) is True  # nosec
