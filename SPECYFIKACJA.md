# Specyfikacja aplikacji --- DNA Analyzer

## 1\. Informacje ogólne

**Nazwa aplikacji:** DNA Analyzer --- analiza motywów w sekwencjach DNA  
**Typ aplikacji:** desktopowa aplikacja z graficznym interfejsem
użytkownika (GUI)  
**Język programowania:** Python  
**Główne biblioteki:** Tkinter/ttk, Pandas, NumPy, Matplotlib,
ReportLab  
**Przeznaczenie:** analiza sekwencji DNA wczytanych z plików FASTA, FA
lub TXT.

## 2\. Cel projektu

Celem aplikacji jest udostępnienie prostego narzędzia do analizy
sekwencji DNA bez konieczności wykonywania poleceń w konsoli. Użytkownik
może wskazać plik wejściowy, określić motyw nukleotydowy oraz długość
segmentu, a następnie przeprowadzić analizę, przeglądać wyniki,
wizualizować ich rozmieszczenie i wyeksportować raport.

Aplikacja realizuje temat „Analiza motywów w DNA" poprzez wyszukiwanie
motywów, określanie pozycji ich wystąpień, analizę częstości w
segmentach oraz wykrywanie potencjalnych ORF.

## 3\. Zakres funkcjonalny

### 3.1. Wczytywanie i walidacja danych

* Użytkownik wybiera plik z poziomu okna dialogowego.
* Obsługiwane formaty wejściowe to FASTA, FA i TXT.
* W przypadku pliku FASTA nagłówki rekordów są pomijane podczas
odczytu sekwencji.
* Aplikacja prezentuje podgląd wczytanej sekwencji.
* Dane wejściowe są sprawdzane przed rozpoczęciem analizy; niepoprawne
lub puste dane powinny skutkować komunikatem dla użytkownika.

### 3.2. Parametry analizy

Użytkownik może ustawić: - motyw nukleotydowy do wyszukania, np. `ATG`,
`TATA` lub `CGCG`, - długość segmentu, na które dzielona jest sekwencja.

Przed uruchomieniem obliczeń aplikacja powinna sprawdzić, czy motyw nie
jest pusty i czy długość segmentu jest dodatnią liczbą całkowitą.

### 3.3. Wyszukiwanie motywów

* Program przeszukuje sekwencję pod kątem wystąpień zadanego motywu.
* Wynik obejmuje pozycję początkową i końcową każdego wystąpienia.
* Numeracja pozycji w prezentowanych wynikach jest liczona od 1.
* Wyszukiwanie uwzględnia nakładające się wystąpienia, tj. po
znalezieniu motywu kolejne wyszukiwanie rozpoczyna się od następnego
nukleotydu, a nie dopiero za końcem znalezionego motywu.
* Lista wystąpień może być eksportowana do CSV.

### 3.4. Podział na segmenty i statystyki

* Sekwencja jest dzielona na kolejne fragmenty o zadanej długości;
ostatni segment może być krótszy.
* Program oblicza liczbę wystąpień motywu w każdym segmencie.
* Wyniki są prezentowane tabelarycznie i zapisywane do CSV.
* Aplikacja oblicza statystyki podsumowujące, w tym średnią i
maksymalną liczbę wystąpień na segment, jeśli te miary są dostępne w
aktualnej implementacji.

### 3.5. Wyszukiwanie potencjalnych ORF

Program wyszukuje potencjalne otwarte ramki odczytu (ORF) w analizowanej
sekwencji: - kodon start: `ATG`, - kodony stop: `TAA`, `TAG`, `TGA`, -
kodon stop musi występować w tej samej ramce odczytu co kodon start.

Dla wykrytego ORF program zapisuje pozycję początku, pozycję końca oraz
sekwencję fragmentu, zgodnie z aktualną implementacją. Pozycje są
prezentowane w numeracji rozpoczynającej się od 1.

Wyniki są zapisywane do pliku CSV. ORF-y należy interpretować jako
kandydatów do dalszej analizy, a nie jako potwierdzone geny.

### 3.6. Wizualizacja

Aplikacja generuje wykresy: - liczby wystąpień motywu w kolejnych
segmentach, - położenia wystąpień motywu w sekwencji, z uwzględnieniem
potencjalnych ORF, jeśli ta warstwa jest dostępna w danej wersji.

Wykresy są tworzone z wykorzystaniem Matplotlib i zapisywane jako pliki
PNG. Są również dostępne w odpowiedniej części GUI, jeśli aktualna
wersja aplikacji wyświetla je w zakładce wykresów.

### 3.7. Raport i eksport

Aplikacja generuje: - plik CSV z pozycjami wystąpień motywu, - plik CSV
ze statystykami segmentów, - plik CSV z potencjalnymi ORF, - pliki PNG z
wykresami, - raport PDF zawierający wyniki i podsumowanie analizy.

Raport PDF wykorzystuje czcionki DejaVuSans umieszczone w katalogu
`Czcionki`, aby zapewnić obsługę polskich znaków. Z poziomu GUI
użytkownik może otworzyć wygenerowany raport, jeśli funkcja ta jest
dostępna w aktualnej wersji programu.

## 4\. Projekt interfejsu graficznego

Interfejs został zbudowany z użyciem Tkinter i ttk. Zastosowano
zakładki, aby rozdzielić ustawienia analizy od wyników i raportowania.

### 4.1. Zakładka „Analiza"

Przeznaczenie: wskazanie danych wejściowych i parametrów analizy.

Elementy: - przycisk wyboru pliku, - pole lub etykieta z nazwą wybranego
pliku, - podgląd wczytanej sekwencji, - pole tekstowe na motyw DNA, -
pole liczbowe na długość segmentu, - przycisk uruchamiający analizę, -
komunikaty walidacyjne i podsumowanie wykonanej analizy.

### 4.2. Zakładka „Wystąpienia"

Przeznaczenie: przegląd wyników wyszukiwania motywu.

Elementy: - tabela z pozycjami wystąpień, - informacje o liczbie
znalezionych wystąpień, - dane możliwe do zapisania do pliku CSV.

### 4.3. Zakładka „ORF-y"

Przeznaczenie: przegląd potencjalnych otwartych ramek odczytu.

Elementy: - tabela wykrytych ORF, - pozycje początku i końca oraz
sekwencje ORF, zależnie od formatu tabeli, - liczba wykrytych ORF w
podsumowaniu, jeśli jest wyświetlana w aktualnej wersji.

### 4.4. Zakładka „Wykresy"

Przeznaczenie: graficzna prezentacja rezultatów.

Elementy: - wykres liczby wystąpień w segmentach, - wykres położenia
motywu i potencjalnych ORF, - osie, tytuły i opisy umożliwiające
interpretację danych.

### 4.5. Zakładka „Raporty" / „Raport"

Przeznaczenie: dostęp do raportu PDF i plików wynikowych.

Elementy: - informacja o wygenerowaniu raportu, - przycisk otwierający
raport PDF, jeśli jest dostępny w bieżącej wersji, - komunikaty
informujące o powodzeniu lub błędzie zapisu.

## 5\. Przepływ działania aplikacji

1. Użytkownik uruchamia `gui.py`.
2. Wskazuje plik zawierający sekwencję.
3. Aplikacja odczytuje i waliduje dane.
4. Użytkownik podaje motyw i długość segmentu.
5. Program wyszukuje wystąpienia motywu, dzieli sekwencję na segmenty i
oblicza statystyki.
6. Program wykrywa potencjalne ORF.
7. Wyniki są prezentowane w tabelach i na wykresach.
8. Program zapisuje pliki wynikowe w katalogu `Wyniki` i generuje
raport PDF.
9. Użytkownik przegląda wyniki i może otworzyć raport.

## 6\. Pliki i katalogi



`gui.py`             Kod interfejsu graficznego
`main.py`            Funkcje logiki analizy
`requirements.txt`   Lista zewnętrznych zależności Pythona
`Sekwencje/`         Przykładowe pliki wejściowe
`Czcionki/`          Czcionki wykorzystywane przy generowaniu PDF
`Wyniki/`            Pliki wynikowe tworzone podczas analizy

`docs/`              Zrzuty ekranu z użycia aplikacji
`README.md`          Instrukcja użytkowania i opis projektu
`SPECYFIKACJA.md`    Niniejszy opis wymagań i zachowania aplikacji



## 7\. Technologie i zależności

* Python 3.13 (środowisko, w którym rozwijano projekt).
* Tkinter/ttk --- GUI.
* Pandas --- tabele danych i eksport CSV.
* NumPy --- obliczenia numeryczne.
* Matplotlib --- wykresy.
* ReportLab --- raport PDF.
* Biblioteki standardowe, m.in. `pathlib` i `os`.

Dokładne wersje pakietów powinny być określone w `requirements.txt`.

## 8\. Walidacja i obsługa błędów

Aplikacja powinna obsługiwać co najmniej następujące sytuacje: - brak
wybranego pliku, - nieobsługiwane rozszerzenie lub problem z odczytem
pliku, - pusta sekwencja, - pusty motyw, - nieprawidłowa długość
segmentu, - brak katalogu wynikowego, - błąd zapisu CSV, PNG lub PDF.

Komunikaty powinny wskazywać problem i --- jeśli to możliwe --- sposób
jego rozwiązania. Katalog `Wyniki` powinien być tworzony przed zapisem
plików, jeżeli nie istnieje.

## 9\. Założenia i ograniczenia

* Aplikacja pracuje na sekwencji dostarczonej przez użytkownika;
pobieranie sekwencji z NCBI/GenBank nie jest deklarowane jako
funkcja, dopóki nie zostanie wdrożone.
* Wyszukiwanie motywu nie uwzględnia automatycznie odwrotnej nici
komplementarnej.
* Analiza ORF ma charakter podstawowy i nie zastępuje pełnej anotacji
genomu.
* Wyniki zależą od jakości danych wejściowych i parametrów wybranych
przez użytkownika.
* Statystyki opisują badaną sekwencję i nie stanowią samodzielnego
dowodu funkcji biologicznej analizowanych fragmentów.

## 10\. Wykorzystanie AI

ChatGPT było wykorzystywane jako narzędzie pomocnicze w planowaniu GUI,
objaśnianiu działania kodu, opracowywaniu i poprawianiu logiki analizy,
diagnozowaniu błędów oraz przygotowaniu dokumentacji. Działanie programu
było sprawdzane przez uruchamianie aplikacji i testowanie jej na
przykładowych sekwencjach. Autor projektu odpowiada za weryfikację
końcowego kodu i umiejętność wyjaśnienia działania jego poszczególnych
elementów.

## 

