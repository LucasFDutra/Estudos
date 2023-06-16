import pytest


@pytest.fixture(scope='module')
def my_fixture():
    print('#### doing something in the SETUP ####')
    yield 42
    print('#### doing something in the TEARDOWN ####')


def test_my_execution_1(my_fixture):
    print('**** starting test 1 ****')
    assert my_fixture == 42
    print('**** ending test 1 ****')


def test_my_execution_2(my_fixture):
    print('**** starting test 2 ****')
    assert my_fixture == 42
    print('**** ending test 2 ****')
