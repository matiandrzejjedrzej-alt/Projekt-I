# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm
print("Program motywy DNA")
print("Autor Mateusz Nowaczyk")
#zdefiniowanie funkcji to wyszukiwania zadanego fragmentu w sekwencji
def znajdz_fragment(sekwencja):
    print("Program podaje koordynaty dla wszystkich wystąpień fragmentu w sekwencji.")
    print("Wyszukiwane fragmenty mogą na siebie nachodzić.")

    while True:
        lista_pozycji = []
        fragment = input("Podaj poszukiwany fragment (lub ENTER aby zakończyć): ")
        if fragment == "":  # po podaniu enter zrobi break
            break
        else:
            fragment = "".join(fragment.split())
            fragment = fragment.upper()
            pozycja_start = sekwencja.find(fragment)  # pierwsze wystąpienie fragmentu w sekwencji

            while pozycja_start != -1:  # funkcja find() zwraca -1 jeśli nie znajdzie fragmentu
                pozycja_stop = pozycja_start + len(fragment) - 1  # ustalenie pozycji końca fragmentu
                lista_pozycji.append([pozycja_start + 1, pozycja_stop + 1])  # dodaje koordynaty do listy pozycji
                pozycja_start = sekwencja.find(fragment,
                                               pozycja_start + 1)  # drugi argument funkcji mówi gdzie zacząć wyszukanie

            if len(lista_pozycji) == 0:
                print("Podany fragment nie występuje w sekwencji.")  # komunikat jeśli nie odnalazł
            else:
                print(
                    f'Wyszukiwany fragment znajduje się w analizowanej sekwencji w pozycjach: ')  # wymienia koordynaty
                for i in lista_pozycji:
                    print(f'{i[0]}-{i[1]}')