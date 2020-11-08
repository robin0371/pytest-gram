import pytest


@pytest.fixture
def repo_path(pytestconfig):
    return pytestconfig.rootdir


@pytest.fixture
def feature_commit_msg_template(pytestconfig):
    pattern = pytestconfig.getini("feature_commit_msg_template")
    return f"^{pattern}$"
