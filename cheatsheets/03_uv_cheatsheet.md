Inicjalizacja projektu (`app` domyślne, `lib` dla paczki Pythonowej):
```bash
uv init [<project_name>] [--app | --lib]
```

Utworzenie nowego środowiska wirtualnego w projekcie:
```bash
uv venv --python 3.12
```

Aktywacja środowiska wirtualnego (czasami potrzeba dopisać `source`):
```bash
[source] .venv\Scripts\activate
```

Deaktywacja środowiska wirtualnego (ponoć ogólnie zalecane jest, by uv samo decydowało o tym kiedy aktywować/deaktywować środowisko wirtualne, czyli po utworzeniu nie wchodzimy do środka (lub jeżeli już weszliśmy do środka, to robimy deaktywację), i normalnie wykonujemy jakieś polecenia, np. `uv run pytest`, a uv samo będzie uruchamiało/wyłączało środowisko wirtualne):
```bash
deactivate
```

Uruchomienie programu:
```bash
uv run <path | command | ...>
```

Dodanie zależności:
```bash
uv add <package1> <package2> ... <packageN>
```

Usunięcie zależności:
```bash
uv remove <package1> <package2> ... <packageN>
```

Zsynchronizowanie zależności z plikiem `pyproject.toml`, plikiem `uv.lock` i ogólnie całym środowiskiem:
```bash
# normal dependencies + dev dependency group
uv sync

# normal dependencies + dev dependency group + other dependency group 1 + ...
uv sync --all-groups

# normal dependencies only
uv sync --no-dev

# normal dependencies + dev dependency group + chosen dependency group
uv sync --group <group_name>

# normal dependencies + dev dependency group + optional dependencies
uv sync --all-extras
```

Obecnie zainstalowane/używane zależności:
```bash
uv pip list
```

Wizualizacja najważniejszych zależności:
```bash
uv tree
```

Zainstaluj/odinstaluj zewnętrzne narzędzie Python:
```bash
uv tool (install | uninstall) <name>
```

Przetestuj narzędzia (zainstaluj w tymczasowym folderze, a następnie od razu odinstaluj):
```bash
uv tool run <tool_name>
# lub krócej
uvx <tool_name>
```

Wyświetl tymaczasowy folder, wyświetl zainstalowane narzędzia, zaaktualizuj te narzędzia:
```bash
uv tool dir
uv tool list
uv tool upgrade --all
```

Dodaj grupę zależności (np. żeby oddzielić te zależności, które są obowiązkowe (zależności produkcyjne) od tych zależności, których się używa w trakcie tworzenia oprogramowania (zależności deweloperskie, np. testowe, dokumentacyjne), opcjonalne zależności to inna sprawa):
```bash
uv add --group dev <package_name, e.g. pytest>
uv add --group docs <package_name, e.g. mkdocs>
```

Dodaj opcjonalne zależności:
```bash
uv add --optional <group_name, .e.g datascience> <package_name, e.g. numpy>
```

Zarządzanie wersjami Pythona:
```bash
uv python (install | pin | list | ...)
```

Rozwiązaywanie zależności (resolving dependencies) do pliku `uv.lock`:

```bash
uv lock
```

Budowanie source distribution (tar.gz) oraz built distribution (.whl):
```bash
uv build
```

Zarządzanie wersją (np. aktualizacja wersji):
```bash
uv version --bump (major | minor | patch | alpha | beta | rc | stable | ...)
```

Publikowanie paczki do TestPyPI (przed publikacją należy ustawić tymczasową zmienną środowiskową `UV_PUBLISH_TOKEN` tak żeby miała przypisany token (API Token wygenerowany w TestPyPI) używany do uwierzytelnienia tożsamości, taka zmienna środowiskowa powinna znikać wraz z zamknięciem danej sesji używanej konsoli):

```bash
# --dry-run symuluje wynik operacji
uv publish --index <tool_uv_index_name> [--dry-run]
```

Przetestuj paczkę z TestPyPI (komenda ta tworzy efemeryczne (tymczasowe) środowisko do uruchomienia programu, a zainstalowane dependencje są instalowane w pamięci cache uv):

```bash
uv run --with "py-playground-1086kamil[ds,plots]==0.2.0rc1" --refresh-package py-playground-1086kamil --default-index https://pypi.org/simple/ --index https://test.pypi.org/simple/ --index-strategy unsafe-best-match --no-project -- python -c "from py_playground.expense_tracker.main import main; main()"

# --index-strategy unsafe-best-match znajduje najlepsze dopasowanie zależności, zamiast ograniczać się tylko do pierwszej znalezionej, która może być zbyt przedawnioną wersją

# po tej komendzie może być potrzeba wyczyszczenia pamięci cache
uv cache dir
uv cache clean
```
