import pytest


@pytest.fixture()
def my_fixture():
    print('#### running my fixture ####')
    return 42


def test_my_execution(my_fixture):
    print('**** starting test ****')
    assert my_fixture == 42
