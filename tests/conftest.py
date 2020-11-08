import pytest
from git import Repo

pytest_plugins = [
    "pytester",
]


@pytest.fixture
def make_repo(testdir):
    def make_git_repo():
        repo = Repo.init(str(testdir.tmpdir))

        file = testdir.tmpdir / "hello.txt"
        file.write_text("hello!", "utf-8")
        repo.index.add([str(file)])
        repo.index.commit("Initial commit")

        with repo.config_writer() as cw:
            cw.set_value("user", "name", "my_username")
            cw.set_value("user", "email", "my_email")

        return repo

    return make_git_repo
