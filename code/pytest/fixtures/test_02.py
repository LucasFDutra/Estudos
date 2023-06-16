import pytest


@pytest.fixture()
def my_fixture():
    print('#### doing something in the SETUP ####')
    yield 42
    print('#### doing something in the TEARDOWN ####')


def test_my_execution(my_fixture):
    print('**** starting test ****')
    assert my_fixture == 42
    print('**** ending test ****')
