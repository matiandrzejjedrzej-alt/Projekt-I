# DNA Analyzer --- analiza motywów w sekwencjach DNA

## Opis projektu

**DNA Analyzer** to aplikacja napisana w Pythonie, służąca do
analizy sekwencji DNA. Umożliwia wczytanie sekwencji z pliku,
wyszukiwanie wskazanego motywu nukleotydowego, analizę rozmieszczenia
jego wystąpień, podział sekwencji na segmenty oraz identyfikację
potencjalnych otwartych ramek odczytu (ORF).

Aplikacja udostępnia graficzny interfejs użytkownika (GUI), prezentuje
wyniki w tabelach i na wykresach oraz zapisuje rezultaty do plików CSV,
PNG i PDF.

## 

## Najważniejsze funkcje

* Wczytywanie sekwencji DNA z plików **FASTA i TXT**.
* Podgląd wczytanej sekwencji oraz kontrola poprawności danych
wejściowych.
* Wyszukiwanie zadanego motywu DNA, z uwzględnieniem nakładających się
wystąpień.
* Wyświetlanie pozycji początku i końca każdego wystąpienia motywu.
* Podział sekwencji na segmenty o zadanej długości.
* Zliczanie wystąpień motywu w poszczególnych segmentach oraz
obliczanie podsumowujących statystyk: średniej i maksymalnej
liczby wystąpień.
* Wyszukiwanie potencjalnych ORF rozpoczynających się od kodonu `ATG`
i kończących w tej samej ramce odczytu kodonem stop (`TAA`, `TAG`
lub `TGA`).
* Prezentacja wyników w tabelach i na wykresach.
* Generowanie raportu PDF oraz eksport tabel do CSV i wykresów do PNG.
* Możliwość otwarcia wygenerowanego raportu z poziomu aplikacji.



## Technologie i biblioteki

* **Python 3.13** --- język programowania.
* **Tkinter / ttk** --- graficzny interfejs użytkownika (biblioteki
standardowe Pythona).
* **Pandas** --- przygotowanie tabel i zapis danych do CSV.
* **NumPy** --- obliczenia numeryczne.
* **Matplotlib** --- tworzenie wykresów.
* **ReportLab** --- generowanie raportu PDF.
* **pathlib** oraz **os** --- obsługa ścieżek i plików.



## Struktura projektu

Przykładowy układ katalogów:

``` text
Projekt-I/
├── gui.py
├── main.py
├── requirements.txt
├── README.md
├── SPECYFIKACJA.md
├── Sekwencje/
│   └── test.fasta
├── Czcionki/
│   └── ... pliki czcionek DejaVuSans ...
├── Wyniki/
│   └── ... pliki generowane podczas analizy ...
└── docs/
    └── zrzuty-ekranu/
        ├── x.png
        ├── y.png
        └── z.png
```

`gui.py` zawiera interfejs graficzny, a `main.py`--- pierwotny program użyty do stworzenia aplikacji. Katalog `Sekwencje` przechowuje przykładowe
pliki wejściowe, `Czcionki` --- pliki czcionek używane przy tworzeniu
PDF, a `Wyniki` jest przeznaczony na wyniki analizy. Katalog wynikowy
powinien być tworzony automatycznie, jeśli jeszcze nie istnieje.

## 

## Instalacja

### Wymagania

* Python 3.10 lub nowszy (projekt był rozwijany w Pythonie 3.13).
* `pip`.
* System z obsługą Tkinter. W standardowej instalacji Pythona dla
Windows Tkinter jest zwykle dostępny.

### 

### Kroki instalacji

1. Sklonuj repozytorium lub pobierz jego zawartość:

&#x20;   ``` bash
    git clone <URL\_REPOZYTORIUM>
    cd Projekt-I
    ```

   Zastąp `<URL\_REPOZYTORIUM>` adresem własnego repozytorium GitHub.

2. (Zalecane) Utwórz i aktywuj środowisko wirtualne:

   **Windows:**

&#x20;   ``` bash
    python -m venv .venv
    .venv\\Scripts\\activate
    ```

3. Zainstaluj zależności:

&#x20;   ``` bash
    python -m pip install -r requirements.txt
    ```

## Uruchomienie

W katalogu głównym projektu uruchom:

``` bash
python gui.py
```

Przykładowy plik wejściowy znajduje się w katalogu
`Sekwencje`.

## 

## Przykładowy przebieg analizy

1. Uruchom aplikację.
2. Wybierz plik z sekwencją DNA, np. `Sekwencje/test.fasta`.
3. Wprowadź motyw do wyszukania (np. `ATG`) oraz długość segmentu.
4. Uruchom analizę.
5. Obejrzyj pozycje wystąpień, statystyki segmentów i potencjalne ORF.
6. Przejdź do zakładek z wykresami i raportem PDF.
7. Zapisane pliki znajdziesz w katalogu `Wyniki`.





## Wykorzystanie narzędzi AI

Podczas realizacji projektu korzystałem z ChatGPT jako narzędzia
wspierającego proces programowania. AI pomagała m.in. w:

* planowaniu struktury aplikacji i elementów GUI,
* opracowaniu oraz wyjaśnianiu logiki analizy sekwencji DNA,
* analizowaniu błędów i proponowaniu poprawek,
* pracy z bibliotekami Python, takimi jak Pandas, NumPy, Matplotlib i
ReportLab,
* przygotowaniu dokumentacji projektu.

Kod był uruchamiany i sprawdzany w środowisku programistycznym, a
proponowane rozwiązania były weryfikowane w toku pracy. 



## Autor

**Autor:** Mateusz Nowaczyk

