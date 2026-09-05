# Overview

```
             / \
            /   \
           / E2E \
          /-------\
         /         \
        /Integration\
       /-------------\
      /               \
     /       Unit      \
    /___________________\
```

```
many unit tests
      ↓
fewer integration tests
      ↓
very few E2E tests
```

- **unit tests** - test relatively small, isolated features/behaviours of the program, e.g. one function
- **integration tests** - test different components working together, e.g. `object -> serializatoin -> storage -> deserialization -> object`
- **end-to-end tests (E2E)** - test the program as if it was a real user, e.g. `start -> enter data -> edit data -> save data -> close -> start again -> load data -> verify data`

We focus mainly on `pytest` here.

# Fixtures

- constant data shared across tests or, more generally, anything a test needs
- can depend on other fixtures
- have a lifetime scope which defines how long they live
  - by default a fixture is created when first requested and destroyed when a function (a single test) ends
  - a fixture with a longer lifetime can be used e.g. to represent a constant connection with a database, which is difficult to constantly open and close for each test
- can perform cleanup with `yield`, the general concepts is: `set up -> test runs -> yield -> test runs -> test ends -> cleanup`, and the code inside fixture is for example: `db.create -> yield db -> db.close`

# conftest.py

File used to store common fixtures so that they aren't duplicated in different testing modules. Discovered automatically (no need to import). Has a hierarchy. For example, in the structure below `conftest.py` in the `tests\` directory is visible everywhere below, but `conftest.py` in the `unit\` directory is not visible in the `integration\` directory.

```
tests/
├── conftest.py
│
├── unit/
│   ├── conftest.py
│   └── test_operations.py
│
└── integration/
    ├── conftest.py
    └── test_storage.py
```

# Other

- provides `tmp_path` for temporary directory, useful for tests involving files and not messing with the actual data
- if there are many tests, we can mark certain tests with our custom label (marker), e.g. we mark integration tests with `@pytest.mark.integration`, and when we want to run only the tests marked with this marker, we run `pytest -m integration`

# Stubs and mocks

The general idea is that sometimes a test depends on external services (e.g. API, database, network latency, etc.) which are unpredictable and can cause the tests to fail even though everything is correct. Instead of using the real, external services, **fake**/**dummy** objects are used to replace them and give the tests everything they need. We can say that those replacement object "mock" or "pretend to be" the real objects and hence the general term "mocking". The more expensive, external, nondeterministic, or uncontrollable the dependency is, the stronger the case for mocking.

- **stub** - simple dummy object that provides deterministic, constant, simplified data to the test, e.g. `return 200` instead of `return http.code`
- **mock** - dummy object that focuses on interactions instead of data, it can for example record what functions were called, with what arguments, etc., to verify the behavior is correct
- **Mock** - class from Python's standard library, `from unittest.mock import Mock`, creates a dummy object which can pretend to be anything, can also record mocking data, you can for example assign arbitrarily named functions to this object and specify what they should return, in general it's preferred to use **MagicMock** instead of **Mock**
- **MagicMock** - subclass of **Mock**, has predefined behaviour for dunder (magic) methods, like `len()`, `mock[0]`, `for item in mock`, etc.
- **patch** - context manager, it temporarily replaces an object with another object, typically it replaces a real function with a mocking function, it can automatically undo the patch once it exits its local scope, it can also be expressed as a function/class decorator, works closely with **Mock**
- **The Golden Rule of Patching**
  - in Python everything is basically a reference, so when you patch a function you essentialy temporarily change the reference to this function, or what the reference to this function points to
  - moreover, each module has its own local namespace scope
  - for example, a file `file.py` can do `import database; database.get_user()` and in this case `get_user()` is stored using its own reference `file.database.get_user`
  - similarly, `file.py` can do `from database import get_user; get_user()` and in this case `get_user()` is stored using its own reference `file.get_user`
  - this means that we can differentiate between the true reference to the `get_user()` function (place where the function `get_user()` is defined), i.e. that in the `database.py` module, from the reference/place where `get_user()` function is accessed/used, i.e. that in the `file.py` module
  - the golden rule is to patch where the function is used, not where the function is defined
  - in this example this means that patch should be done using `file.database.get_user` or `file.get_user`, not on `database.get_user`
  - this is because doing a patch on the true, original reference to the function can have unexpected consequences
  - TLDR: patch where it is used, not where it is defined, because this is how Python works
- **monkeypatch** - similar to **patch** but it is a built in pytest feature, does not work as context manager but with `set_` methods, it temporarily replaces values during tests
