import pathlib
import py
import pytest
from _pytest import fixtures


class PytestGramModule(pytest.Module):
    def get_test_functions(self):
        return [
            getattr(self.module, attr)
            for attr in dir(self.module)
            if attr.startswith("test_")
        ]


class PytestGramFunction(pytest.Function):
    def runtest(self) -> None:
        fm = getattr(self.session, "_fixturemanager")
        fixture_info = fm.getfixtureinfo(
            node=self,
            func=self.function,
            cls=None,
        )

        fixture_request = fixtures.FixtureRequest(self)
        fixture_request._fillfixtures()  # noqa

        params = {arg: self.funcargs[arg] for arg in fixture_info.argnames}
        self.function(**params)

    def reportinfo(self):
        fspath, line, name = super().reportinfo()
        return fspath, line, f"[pytest-gram] {name}"


def collect_tests(session, config):
    plugin_path = pathlib.Path(__file__).parent.absolute()
    tests_path = py.path.local(plugin_path) / config.pytest_gram_tests
    module = PytestGramModule.from_parent(parent=session, fspath=tests_path)

    return [
        PytestGramFunction.from_parent(
            parent=module,
            name=test_func.__name__,
            callobj=test_func,
        )
        for test_func in module.get_test_functions()
    ]
