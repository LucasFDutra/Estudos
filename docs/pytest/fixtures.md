# Fixtures

Fixtures are functions that we run before and sometimes after a test. We usually use fixtures to encapsulate logic that we need all the time. For example, we can use fixtures to: 

- Open and close a database connection.
- Open and close a file.
- Generate dammy data.
- Get system information.
- And many more things

The advantage of using fixtures is that we can reuse this logic across multiple tests.

## Getting Start

To declare a function as a fixture, you need to decorate the fixture with the `@pytest.fixture` decorator. Then, you pass the fixture function's name as a parameter to the test function.

```{.py  linenums="1" .copy}
import pytest

@pytest.fixture()
def my_fixture():
    print('#### running my fixture ####')
    return 42

def test_my_execution(my_fixture):
    print('**** starting test ****')
    assert my_fixture == 42
```

Running pytest with the `-s` flag to show the prints. We observe the following output:

```{.bash title="Running Test"}
❯❯ pytest -sv
========================= test session starts ==========================
code/pytest/fixtures/test_01.py::test_my_execution 

#### running my fixture ####
**** starting test ****

PASSED
========================== 1 passed in 0.01s ===========================
```

By observing the prints, we can see that the fixture executes first, followed by the test function `test_my_execution`.

When running the test, it passes successfully, indicating that the value of the parameter `my_fixture` matches the expected value of 42. 

From this example, we can conclude that when a function is declared as a fixture, it runs at the beginning of the test execution and the returned value of the fixture is accessible in the test function by defining a parameter with the same name as the fixture.

## Setup and Teardown

As the name suggests, the `setup` in a test refers to the preparation phase before performing a task. For exemple, connecting to a database and inserting some dummy data that is needed for the test.

And the `teardown` is the phase where you undo or clean up what was done during the setup. Following the previous example, it will delete the dummy data and disconnecting from the database, ensuring a clean state for the next test.

To use a fixture with this two parts, we can't use the `return`, instead, we need to use the `yield`.
See the example to understand how to use this.


```{.py  linenums="1" .copy}
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
```

```{.bash title="Running Test"}
❯❯ pytest -sv code/pytest/fixtures/test_02.py 
========================= test session starts ==========================
code/pytest/fixtures/test_02.py::test_my_execution 

#### doing something in the SETUP ####

**** starting test ****
**** ending test ****

PASSED
#### doing something in the TEARDOWN ####
========================== 1 passed in 0.01s ===========================
```

By observing the prints, we can see that the setup part of the fixture executes first, followed by the test function `test_my_execution`, and at the end of the test execution, the teardown part of the fixture was executed.


## Scopes

The scope of a fixture determines when the setup and teardown will be executed. The default scope is function, which means that the fixture's setup will run before each test function, and the teardown will run after each test function.


The scope of a fixture determines when the setup and teardown will be executed. The default scope is `function`, which means that the fixture's setup will run before each test function, and the teardown will run after each test function.

```{.py  linenums="1" .copy}
import pytest

@pytest.fixture()
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
```

```{.bash title="Running Test"}
❯❯ pytest -sv code/pytest/fixtures/test_03.py
========================= test session starts ==========================
code/pytest/fixtures/test_03.py::test_my_execution_1 

#### doing something in the SETUP ####

**** starting test 1 ****
**** ending test 1 ****

PASSED
#### doing something in the TEARDOWN ####

code/pytest/fixtures/test_03.py::test_my_execution_2 

#### doing something in the SETUP ####

**** starting test 2 ****
**** ending test 2 ****

PASSED
#### doing something in the TEARDOWN ####
========================== 2 passed in 0.02s ===========================
```

Observing the prints, it's possible to see the behavior of a function-scoped fixture. It executes the setup and teardown twice, once for each test that utilizes the fixture.

However, if I change the scope to `module` by adding scope='module' as a parameter in the fixture decorator, the fixture will run only once.


```{.py  linenums="1" .copy}
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

```

```{.bash title="Running Test"}
❯❯ pytest -sv code/pytest/fixtures/test_04.py
========================= test session starts ==========================
code/pytest/fixtures/test_04.py::test_my_execution_1 

#### doing something in the SETUP ####

**** starting test 1 ****
**** ending test 1 ****

PASSED

code/pytest/fixtures/test_04.py::test_my_execution_2 

**** starting test 2 ****
**** ending test 2 ****

PASSED

#### doing something in the TEARDOWN ####
========================== 2 passed in 0.01s ===========================
```

Notice that the setup only runs at the beginning of the execution (before test one) and the teardown runs only at the end of the execution (after test two).

All fixture scopes are:

- function (default): Runs once per test function. The setup portion is executed before each test that uses the fixture, and the teardown portion is executed after each test that uses the fixture.
- class: Runs once per test class.
- module: Runs once per module.
- package: Runs once per package, or test directory.
- session: Runs once per session, meaning it executes once for each pytest execution. This scope is useful for tasks like opening and closing database connections.


## Using fixtures in `conftest.py`

The `conftest.py` file is a special file in pytest. Its contents are automatically loaded into memory and don't need to be imported into other files.

It's loaded according to the folder in which it's located. Let's imagine the following file structure:

```bash
tests
├── tests_module_1
│   ├── conftest.py
│   ├── test_1.py
│   └── test_2.py
└── tests_module_2
    ├── conftest.py
    ├── test_3.py
    └── test_4.py
```

The `test_1.py` and `test_2.py` files can access the contents of the `conftest.py` file in the same folder (`tests_module_1`), but they cannot access the other `conftest.py` file in the `tests_module_2` folder. This other `conftest.py` is associated with `test_3.py` and `tests_4.py`.

So, one conftest is shared among all the files within the same directory.

One useful practice is to place fixtures in the `conftest.py` file and share them across multiple tests. For example, if you have a fixture that generates data, you can define this fixture in the conftest and use it in all the tests within that folder.

See the example:

```{.py  linenums="1" title="tests/tests_module_1/conftest.py" .copy}
import pytest

@pytest.fixture()
def my_fixture():
    print('#### running my fixture ####')
    return 42
```

```{.py  linenums="1" title="tests/tests_module_1/test_1.py" .copy}
def test_my_execution_1(my_fixture):
    print('**** starting test 1 ****')
    assert my_fixture == 42
```

```{.py  linenums="1" title="tests/tests_module_1/test_2.py" .copy}
def test_my_execution_2(my_fixture):
    print('**** starting test 2 ****')
    assert my_fixture == 42
```

```{.bash title="Running Test"}
❯❯ pytest -sv code/pytest/fixtures/conftest_example
========================= test session starts ==========================
code/pytest/fixtures/conftest_example/tests_module_1/test_1.py::test_my_execution_1 

#### running my fixture ####

**** starting test 1 ****

PASSED

code/pytest/fixtures/conftest_example/tests_module_1/test_2.py::test_my_execution_2 

#### running my fixture ####

**** starting test 2 ****

PASSED
========================== 2 passed in 0.02s ===========================
```

See that the fixture was declared in the `conftest.py`, but it was used in both test files without needing to be imported.
