import re
import logging

from git import Repo

LOGGER = logging.getLogger(__name__)


def test_commit_messages_are_matched(feature_commit_msg_template, repo_path):
    repo = Repo(str(repo_path))
    pattern = re.compile(feature_commit_msg_template)
    commit_prefix = "commit: "

    commit_messages = [
        log.message[len(commit_prefix):]
        for log in repo.active_branch.log()
        if log.message.startswith(commit_prefix)
    ]
    for message in commit_messages:
        match = bool(pattern.match(message))
        if not match:
            LOGGER.error(
                f"Commit message \"{message}\" not matched to "
                f"\"{feature_commit_msg_template}\""
            )
        assert match is True  # nosec
