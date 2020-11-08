from pytest_gram.plugin import collect_tests


def pytest_addoption(parser):
    parser.addini(
        name="feature_commit_msg_template",
        help="Regex string that feature commit message should be matched. "
        "For example: 'SV-[\\d{4}] [\\s\\S]*'",
        default="",
    )


def pytest_configure(config):
    # set module name with test functions
    config.pytest_gram_tests = "tests.py"


def pytest_collection_modifyitems(session, config, items):
    tests = collect_tests(session, config)
    items.extend(tests)
