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
