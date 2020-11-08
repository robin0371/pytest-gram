import pytest


class TestMatchPattern:
    def test_no_repo(self, testdir, monkeypatch, make_repo):
        monkeypatch.chdir(testdir.tmpdir)

        testdir.makefile(
            ".ini", pytest="[pytest]\nfeature_commit_msg_template=PR-\\d{4}\n"
        )
        testdir.plugins = ["pytest_gram"]
        result = testdir.runpytest(plugins=["pytest_gram"])

        assert result.ret == pytest.ExitCode.TESTS_FAILED
        result.stdout.fnmatch_lines([
            f"*git.exc.InvalidGitRepositoryError: {testdir.tmpdir}*",
            "*1 failed*",
        ])

    def test_no_commits(self, testdir, monkeypatch, make_repo):
        monkeypatch.chdir(testdir.tmpdir)
        make_repo()

        testdir.makefile(
            ".ini", pytest="[pytest]\nfeature_commit_msg_template=PR-\\d{4}\n"
        )
        testdir.plugins = ["pytest_gram"]
        result = testdir.runpytest(plugins=["pytest_gram"])

        assert result.ret == pytest.ExitCode.OK

    def tests_matched(self, testdir, monkeypatch, make_repo):
        monkeypatch.chdir(testdir.tmpdir)
        repo = make_repo()

        file = testdir.tmpdir / "bye.txt"
        file.write_text("bye!", "utf-8")
        repo.index.add([str(file)])
        repo.index.commit("commit: PR-1234")

        testdir.makefile(
            ".ini", pytest="[pytest]\nfeature_commit_msg_template=PR-\\d{4}\n"
        )
        testdir.plugins = ["pytest_gram"]
        result = testdir.runpytest(plugins=["pytest_gram"])

        assert result.ret == pytest.ExitCode.OK

    def tests_not_matched(self, testdir, monkeypatch, make_repo):
        monkeypatch.chdir(testdir.tmpdir)
        repo = make_repo()

        file = testdir.tmpdir / "bye.txt"
        file.write_text("bye!", "utf-8")
        repo.index.add([str(file)])
        repo.index.commit("commit: not_matched")

        testdir.makefile(
            ".ini", pytest="[pytest]\nfeature_commit_msg_template=PR-\\d{4}\n"
        )
        testdir.plugins = ["pytest_gram"]
        result = testdir.runpytest(plugins=["pytest_gram"])

        assert result.ret == pytest.ExitCode.TESTS_FAILED
        result.stdout.fnmatch_lines([
            "*Commit message \"not_matched\" not matched to \"^PR-\\d{4}$\"*",
            '*1 failed*',
        ])
