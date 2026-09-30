
print("Program motywy DNA")
print("Autor Mateusz Nowaczyk")
#zdefiniowanie funkcji do wyszukiwania zadanego fragmentu w sekwencji
def znajdz_fragment(sekwencja, fragment):
    lista_pozycji = []
    pozycja_start = sekwencja.find(fragment)
    while pozycja_start != -1:
        pozycja_stop = pozycja_start + len(fragment) - 1
        lista_pozycji.append([pozycja_start + 1, pozycja_stop + 1])
        pozycja_start = sekwencja.find(fragment,
                                       pozycja_start + 1)
    return lista_pozycji


#funkcja do wczytywania sekwencji z pliku
def wczytaj_sekwencje(nazwa_pliku):
    with open(nazwa_pliku, "r", encoding="utf-8") as plik:
        sekwencja = ""

        for linia in plik:
            if not linia.startswith(">"):
                sekwencja += linia.strip()
    return sekwencja.upper()




