## Tworzenie i aktywowanie środowiska

Aby utworzyć nowe środowisko, wystarczy polecenie:
```bash
conda create --name <nazwa_srodowiska>
```

Aby utworzyć środowisko z konkretną wersją Pythona, należy podać tę wersję jako parametr przy tworzeniu:
```bash
conda create --name <nazwa_srodowiska> python=3.8
```

Aby aktywować środowisko, należy wykonać:
```bash
conda activate <nazwa_srodowiska>
```

## Instalacja pakietów w środowisku

Instalacja pakietów jest możliwa na dwa sposoby. Jednym jest znany z venv `pip`, drugim jest natywny system zarządzania pakietami Condy. W przypadku drugiego, nie wszystkie pakiety będą dostępne, natomiast potencjalnie dostaniemy lepszy system zarządzania konfliktami i zależnościami między pakietami. Należy uważać, gdy sie miesza `pip` z natywnym systemem Condy. Ogólnie to Conda zarządza środowiskiem i pakietami; `pip` może jedynie dodatkowo instalować pakiety w środowisku.

Instalacja z użyciem Condy:
```bash
conda install <nazwa_pakietu>
```

Instalacja z użyciem `pip`:
1. Zainstaluj `pip` z wykorzystaniem Condy:
    ```bash
    conda install pip
    ```
2. Używaj `pip` jak zawsze:
    ```bash
    pip install <nazwa_pakietu>
    ```

## Usuwanie i migracja środowiska

Aby usunąć środowisko, wykonaj:
```bash
conda remove --name <nazwa_srodowiska> --all
```

Aby wyeksportować konfigurację środowiska, możesz:

1. Wyeksportować pakiety do pliku `requirements.txt`:
    ```bash
    pip list --format=freeze > requirements.txt
    ```
    a następnie w nowo utworzonym środowisku zainstalować je poleceniem:
    ```bash
    pip install -r requirements.txt
    ```

2. Wyeksportować środowisko narzędziami Condy:
    ```bash
    conda env export > environment.yaml
    ```
    a następnie odtworzyć je poleceniem:
    ```bash
    conda env create -f environment.yaml
    ```

## Inne przydatne polecenia

Poniższe polecenia wypisują przydatne informacje:
```bash
conda info
conda list
conda env list
```

Poniższe polecenie instaluje pakiet z kanału społecznościowego `conda-forge` zamiast z kanału domyślnego (kanał to tak naprawdę zwykły URL do folderu z dostępnymi pakietami):
```bash
conda install -c conda-forge <nazwa_pakietu>
```
