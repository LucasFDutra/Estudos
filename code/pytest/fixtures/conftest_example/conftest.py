import pytest


@pytest.fixture()
def my_fixture():
    print('#### running my fixture ####')
    return 42
