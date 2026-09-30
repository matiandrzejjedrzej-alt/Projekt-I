
import matplotlib.pyplot as plt

#Funkcje++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#funkcja do wyszukiwania zadanego fragmentu w sekwencji
def znajdz_fragment(sekwencja, fragment):
    lista_pozycji = []
    pozycja_start = sekwencja.find(fragment)
    while pozycja_start != -1:
        pozycja_stop = pozycja_start + len(fragment) - 1
        lista_pozycji.append([pozycja_start + 1, pozycja_stop + 1])
        pozycja_start = sekwencja.find(fragment, pozycja_start + 1)

    return lista_pozycji


#funkcja do wczytywania sekwencji z pliku
def wczytaj_sekwencje(nazwa_pliku):
    with open(nazwa_pliku, "r", encoding="utf-8") as plik:
        sekwencja = ""

        for linia in plik:
            if not linia.startswith(">"):
                sekwencja += linia.strip()
    return sekwencja.upper()

#funkcja do sprawdzenia podanego fragmentu
def sprawdz_fragment(fragment):
    if fragment == "":
        return False

    for n in fragment:
        if n not in "ATGC":
            return False
    return True

#funkcja do sprawdzenia pliku i sekwencji
def sprawdzenie_sekwencji(sekwencja):
    while True:
        if sekwencja == "":
            print("Plik jest pusty")
        for n in sekwencja:
            if n not in "ATGC":
                return False
        return True

#funkcja podział sekwencji na segemnty
def podział_segmenty (sekwencja, długość_segmentu):
    segmenty = []
    for i in range(0, len(sekwencja), długość_segmentu):
        segment = sekwencja[i:i + długość_segmentu]
        segmenty.append(segment)
    return segmenty


#Program++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("Program motywy DNA")
print("Autor Mateusz Nowaczyk")
while True: #podanie nazwy pliku
    print("Plik z sekwencją do analizy umieść w folderze 'Sekwencje'.")
    nazwa_pliku = input("Podaj nazwę pliku za nazwą folderu wraz z jego rozszerzeniem, np. Sekwencje/test.fasta: ")

    try:
        sekwencja = wczytaj_sekwencje(nazwa_pliku)

    except FileNotFoundError:
        print("Nie znaleziono pliku. Wpisz poprawną nazwę i spróbuj ponownie.")
        continue

    poprawna_sekwencja = True
    for n in sekwencja:
        if n not in "ACTG":
            poprawna_sekwencja = False
            break
    if not poprawna_sekwencja == True:
        print("Sekwencja zawiera błędne znaki.")
        continue

    break

while True: #sprawdzenie, czy fragment składa się z ACGT
    fragment = input("Podaj szukany fragment DNA: ")
    fragment = "".join(fragment.split()).upper()

    if sprawdz_fragment(fragment):
        break
    else:
        print("Nieprawidłowa sekwencja. Dozwolone znaki to A, T, G i C.")

pozycje = znajdz_fragment(sekwencja, fragment)

print()

if len(pozycje) == 0:

    print("Nie znaleziono podanego fragmentu.")

else:

    print(f"Liczba wystąpień: {len(pozycje)}")

    print("Pozycje wystąpień:")

    for pozycja in pozycje:
        print(f"{pozycja[0]}-{pozycja[1]}")

długość_segemntu = int(input("Podaj na jakiej długości segmenty chcesz podzielić sekwencję: "))

segmenty = podział_segmenty(sekwencja, długość_segemntu) #lista segmentów

pozycje_dla_segmentów = []
for i in segmenty:
    pozycje = znajdz_fragment(i, fragment)
    pozycje_dla_segmentów.append(pozycje)  #lista pozycji z fragmentem w segmentach

liczba_wystąpień = []
for i in pozycje_dla_segmentów:
    liczba_wystąpień.append(len(i)) # lista z liczbą wystąpień fragmentu dla każdego segmentu

print(liczba_wystąpień)
liczba_segmentów = []
for i in range (1, len(segmenty)+1):
    liczba_segmentów.append(i)   #lista z numerami segmentów
print(liczba_segmentów)

#wykres słupkowy- liczba wystąpień na segemnt
plt.bar(liczba_segmentów, liczba_wystąpień)

plt.xlabel("Segment")
plt.ylabel("Liczba wystąpień")
plt.title("Liczba wystąpień fragmentu DNA w segmentach")
plt.xlim(1,len(liczba_segmentów))
plt.yticks(range(max(liczba_wystąpień) + 1))
plt.show()


