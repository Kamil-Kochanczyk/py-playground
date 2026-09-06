# Overview

```
                    Python ecosystem
                            │
        ┌───────────────────┼──────────────────┐
        │                   │                  │
   Python itself      Environments        Packages
        │                   |                  |
        │                   |                  |
        └───────────────────┼──────────────────┘
                            │
                    Project management
                            │
                            │
                            ▼
                    pyproject.toml
                            │
                            ▼
                          Build
                            │
                            ▼
                          PyPI
```

# Main tools (cheatsheets-worthy)
| Tool           | Main purpose                                          | Subjective importance                    |
| -------------- | ----------------------------------------------------- | --------------------------------------- |
| **pip**        | Install Python packages                               | ⭐⭐⭐⭐⭐                               |
| **venv**       | Create virtual environments                           | ⭐⭐⭐⭐⭐                               |
| **uv**         | Modern all-in-one Python/project manager              | ⭐⭐⭐⭐⭐                               |
| **conda**      | Environment + packages, including non-Python software | ⭐⭐⭐⭐⭐                         |

# Other tools
Other tools which are useful to know/understand/remember:
- **pipx** - installs CLI programs in their own, separate environments, not in the environments that one uses for their projects
- **virtualenv** - richer version of **venv** (**venv** is a subset of **virtualenv**)
- **Poetry**, **PDM** - roughly serve the same purposes as **uv**
- **Hatch** - another Python/project manager, also a build manager, contains **Hatchling** which is a build backend
- **pipenv** - another managment tool, combines **pip** and **venv**, manages dependencies, etc.
- **pip-tools** - e.g. **pip-compile** or **pip-sync**, set of tools used in the following workflow: `dependency specification (numpy>=2.5.0, pandas^2.0, etc.) -> dependency resolution (going through the dependency graph and resolving version conflicts) -> locked dependencies (numpy=2.5.3, pandas=2.2.2, etc.)`
- **build** - build frontend, command **python -m build**, orders **sdists** and/or **wheels** from build backends
- **Hatchling** - build backend
- **setuptools** - build backend
- **Twine** - tool that publishes packages to PyPI
- **Flit** - tool that publishes packages to PyPI
- **pyenv** - tool for managing Python versions in your projects

# Glossary
- **PyPA** - Python Packagin Authority, a working group that maintains core software tools and standards for packaging and distributing Python code
- **PyPI** - Python Package Index, the main public repository where those software packages are stored and downloaded
- **Test PyPI** - separate instance of **PyPI** that allows you to try out the distribution tools and process without worrying about affecting the real index
- **pyproject.toml** - file with project metadata, dependencies, configs, etc.
- **dependency group** - a named collection of related software packages grouped together in a project's configuration file to streamline (optimize, make faster and easier to manage) environment management and installation
- **development dependencies** - software packages required solely for developing, testing, or building a project, but omitted when running the application in a production environment
- **optional/extra dependencies** - non-essential packages that unlock additional features or capabilities in a project, which users can choose to install alongside the core package
- **dependency graph** - graph that represents the network of all dependencies used in the project, the main dependencies are usually connected to their subdependencies (requirements), i.e. there are **direct dependencies** and **transitive dependencies**
- **dependency resolution** - algorithm that traverses the dependency graph and finds the package versions that do not conflict with one another (e.g. one subdependency may require `numpy>=2.2.2` while some other may require `numpy<2.2.2` and then the resolution fails)
- **lock file** - file containing the output of the dependency resolution phase, i.e. specific versions of packages possible to easily reproduce on any machine
- **application** vs **package**/**library** - a Python application is a standalone, executable program designed to be run directly by end-users to perform specific tasks, whereas a Python package or library is a reusable collection of code meant to be imported and used by other programs
- **building** - turning the source code into another form that can be easily distributed and installed on the machines
- **build frontend** - tool that the user interacts with when they want to create a package, its job is to invoke the backend in an isolated environment and drive the build process
- **build backend** - underlying Python library that actually reads your code, compiles extension modules (like C/C++), generates metadata, and bundles everything into installable archives, does the actual work, produces **distributions**
- **distribution** - archives created by backends, can be uploaded to PyPI, two types: **sdist** or **wheel**
- **sdist** - **source distribution**, .tar.gz, uncompiled source code and raw files, installation slow (requires building step to produce **wheel** and only then installs), platform independent
- **wheel** - **build distribution**, .whl, pre-compiled code (ready-to-use), installation fast (requires only unzipping and copying to the target directory to install), can be platform dependent (e.g. if C/C++ code was also compiled)
- **semantic versioning** - meaning of `x.y.z` version numbers, e.g. in version `1.2.3`: `1` is the major version, `2` is the minor verision and `3` is the patch
- **plugin** - software component that adds new features or specific capabilities to an existing host program without changing its core code
- `PYTHONPATH` - environment variable which stores all paths that the interpreter will check to try to find the **modules** to import into your scripts
- **module** - single `.py` file, imported through one of `PYTHONPATH` paths, creates a unique namespace scope for its members
- **package** - group of modules, defines the namespace scope for them
- **subpackage** - package inside another package, or simply: child directory (containing `.py` files) inside parent directory
- **\_\_init\_\_.py** - special file inside a package, it is invoked when the package or a module in the package is imported, can be used to initialize some global data or to define modules/subpackages automatically imported when `import <package_name>` is invoked, not mandatory (if omitted in the package, the package becomes the so-called **implicit namespace package**)
- **\_\_main\_\_.py** - another special file inside a package, when it is defined the package can be run as a command, e.g. `python -m package_name`, and the code that will be executed in such case will be the code defined in **\_\_main\_\_.py**
- **\_\_all\_\_** - by convention it is a list (a variable referencing a list) of names used to control what is imported from a module or from a package when `import *` is invoked, not mandatory
  - when not specified:
    - (1) `import *` for a module imports everything except protected variables
    - (2) `import *` for a package doesn't import anything
- **absolute import** - used in sibling packages (child subpackages on the same hierarchy level inside some parent package), e.g. inside `pkg.sub_pkg2.module2` we can write `from pkg.sub_pkg1.module1 import function1` as an absolute path
- **realtive import** - also used in sibling packages, in general not recommended, `.` means current package, `..` means parent package, etc., e.g. inside `pkg.sub_pkg2.module2` we can write `from .. import sub_pkg1` or `from ..sub_pkg1.module1 import function1` and `..` here means `pkg`
- **implicit namespace package** - package without `__init__.py`, the namespace of this package is not defined and not limited by the parent directory and its name, one such package doesn't really work differently from a "normal" package, to see benefits at least two such packages are needed because then those packages can be grouped together to use the same namespace even though they are in different places/directories/machines
  - for example, we have a namespace package called `my_ns_pkg` (and so we say that `my_ns_pkg` is our common namespace), let's also assume we have `module1` and `module2` which were created in completely different and separate projects/machines/etc., with namespace package we can still write `from my_ns_pkg import module1, module2` as if `module1` and `module2` were in the same place (inside `my_ns_pkg`), the only condition is that `module1` and `module2` must correctly mirror the appropriate directory structure, i.e. their corresponding parent directories have to be named `my_ns_pkg`, other than that we can put them in completely differernt projects, e.g. `my_ns_pkg_proj1` and `my_ns_pkg_proj2`, that live on separate machines, and still after `pip install my_ns_pkg` both `module1` and `module2` will be available inside `my_ns_pkg` (provided `module1` and `module2` are published to an index) thanks to native Python import system

# Utils
- license texts: https://choosealicense.com/
- valid licenses for `pyproject.toml`: https://spdx.org/licenses/
- valid classifiers for `pyproject.toml`: https://pypi.org/classifiers/
