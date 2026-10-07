
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import colors


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

#wyszukiwanie ORF
def wyszukaj_ORF(sekwencja):
    lista_ORF = []
    start_ORF = 0
    stop_ORF = 0
    kodony_stop = ["TAA", "TGA", "TAG"]
    i = 0
    while i < len(sekwencja):

        if sekwencja[i:i + 3] == "ATG":
            start_ORF = i

            for j in range(i + 3, len(sekwencja), 3):
                if sekwencja[j:j + 3] in kodony_stop:
                    stop_ORF = j
                    lista_ORF.append([start_ORF + 1, stop_ORF + 3, sekwencja[start_ORF:stop_ORF + 3]])
                    i = stop_ORF + 3
                    break
            else:
                i += 1
        else:
            i += 1

    return lista_ORF



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

pozycje = znajdz_fragment(sekwencja, fragment) #szukanie fragmentu w sekwencji

if len(pozycje) == 0:
    print("Nie znaleziono podanego fragmentu.")
else:
    print(f"Liczba wystąpień: {len(pozycje)}")
    print("Pozycje wystąpień:")
    for pozycja in pozycje:
        print(f"{pozycja[0]}-{pozycja[1]}")

#tworzenie tabeli z pozycjami wystąpień
zestawienie_wystąpień = pd.DataFrame(pozycje, columns = ["Początek","Koniec"])

zestawienie_wystąpień.to_csv("Wyniki/wystąpienia_fragmentu.csv", index=False)

długość_segemntu = int(input("Podaj na jakiej długości segmenty chcesz podzielić sekwencję: "))

segmenty = podział_segmenty(sekwencja, długość_segemntu) #lista segmentów

pozycje_dla_segmentów = []
for i in segmenty:
    pozycje_seg = znajdz_fragment(i, fragment)
    pozycje_dla_segmentów.append(pozycje_seg)  #lista pozycji z fragmentem w segmentach

liczba_wystąpień = []
for i in pozycje_dla_segmentów:
    liczba_wystąpień.append(len(i)) # lista z liczbą wystąpień fragmentu dla każdego segmentu

liczba_segmentów = []
for i in range (1, len(segmenty)+1):
    liczba_segmentów.append(i)   #lista z numerami segmentów

#statystyka wystąpień
dane_statystyczne = np.array(liczba_wystąpień)
średnia_wystąpień = np.mean(dane_statystyczne)
maksimum_wystąpień = np.max(dane_statystyczne)

print("Statystyka wystąpień:")
print(f"Średnia liczba wystąpień na segment: {średnia_wystąpień:.2f}")
print(f"Maksimum wystąpień fragmentu na segment: {maksimum_wystąpień}")

#tworzenie tabeli z liczbą wystąpień fragmentu na segment do CSV
tabela = pd.DataFrame({ "Segment": liczba_segmentów,
    "Liczba wystąpień": liczba_wystąpień
})

tabela.to_csv("Wyniki/liczba_wystąpień_na_segment.csv", index=False)



#wykres słupkowy- liczba wystąpień na segemnt
plt.bar(liczba_segmentów, liczba_wystąpień)

plt.xlabel("Segment")
plt.ylabel("Liczba wystąpień")
plt.title("Liczba wystąpień fragmentu DNA w segmentach")
plt.xlim(0.5,len(liczba_segmentów) + 0.5)
plt.xticks(range(1, len(liczba_segmentów) + 1))
plt.yticks(range(max(liczba_wystąpień) + 1))
plt.show()
plt.savefig("Wyniki/wykres_segmenty.png")

#wykres wystąpienia fragmentu w obrębie sekwencji
plt.figure()

for pozycja in pozycje:
    plt.hlines(0.005, pozycja[0], pozycja[1])

plt.title("Wystąpienia fragmentu w obrębie sekwencji")
plt.xlabel("Pozycja [nt]")
plt.xlim(1, len(sekwencja))
plt.ylim(0, 0.1)
plt.gca().get_yaxis().set_visible(False) #oś Y niewidoczna
plt.show()
plt.savefig("Wyniki/wykres_pozycje")

#wyszukiwanie ORF w sekwencji i wrzucenie danych do tabeli
lista_ORF = wyszukaj_ORF(sekwencja)

print("Tabela potencjalne ORF")
df = pd.DataFrame(
    lista_ORF,
    columns=["Początek ORF", "Koniec ORF", "Sekwencja ORF"]
)

print(df)

df.to_csv("ORFs.csv", index=False)

pdfmetrics.registerFont(
    TTFont("DejaVuSans", r"Czcionki\DejaVuSans.ttf")
)

pdf = canvas.Canvas("Wyniki/raport.pdf")
pdf.setFont("DejaVuSans", 12)

pozycja_y = 800
pdf.drawString(100, pozycja_y, "Raport analizy sekwencji DNA")
pdf.drawString(100, pozycja_y - 40, f"Długość sekwencji: {len(sekwencja)} nt")
pdf.drawString(100, pozycja_y - 60, f"Szukany fragment: {fragment}")
pdf.drawString(100, pozycja_y - 80, f"Liczba wystąpień: {len(pozycje)}")
pdf.drawString(100, pozycja_y -100 , f"Pozycje wystąpień fragmentu w sekwencji: ")

pdf.drawString(100, pozycja_y -200 , f"Wybrana długość segemntów: {długość_segemntu}")
pdf.drawString(100, pozycja_y -220 , f"Liczba wystąpień fragmentu w poszczególnych segmentach")

pdf.drawString(100, pozycja_y -240 , f"Średnia liczba wystąpień fragmentu na segment: ")
pdf.drawString(100, pozycja_y -260 , f"Maksimum wystąpień fragmentu na segment: ")
pdf.drawString(100, pozycja_y -300 , f"Przewidywane ORF w sekwencji: ")

pdf.save()