
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
import os

matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from reportlab.platypus import PageBreak
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4

# Kolory aplikacji DNA Analyzer
KOLOR_TLA = "#F4F7FB"
KOLOR_PANELU = "#FFFFFF"
KOLOR_GRANATOWY = "#17365D"
KOLOR_TURKUSOWY = "#159A9C"
KOLOR_TURKUS_HOVER = "#117C80"
KOLOR_TEKSTU = "#263445"
KOLOR_POMOCNICZY = "#64748B"
KOLOR_RAMKI = "#DCE4ED"

# Czcionki
CZCIONKA_GLOWNA = ("Segoe UI", 10)
CZCIONKA_NAGLOWKA = ("Segoe UI", 17, "bold")
CZCIONKA_SEKCJI = ("Segoe UI", 11, "bold")



# =========================================================
# ŚCIEŻKI DO FOLDERÓW
# =========================================================

KATALOG_PROJEKTU = Path(__file__).resolve().parent
KATALOG_WYNIKOW = KATALOG_PROJEKTU / "Wyniki"
KATALOG_WYNIKOW.mkdir(parents=True, exist_ok=True)


# =========================================================
# FUNKCJE ANALIZY DNA
# =========================================================

def znajdz_fragment(sekwencja, fragment):
    lista_pozycji = []
    pozycja_start = sekwencja.find(fragment)

    while pozycja_start != -1:
        pozycja_stop = pozycja_start + len(fragment) - 1

        lista_pozycji.append([
            pozycja_start + 1,
            pozycja_stop + 1
        ])

        # +1 umożliwia znalezienie nakładających się wystąpień
        pozycja_start = sekwencja.find(
            fragment, pozycja_start + 1
        )

    return lista_pozycji


def wczytaj_sekwencje(nazwa_pliku):
    with open(nazwa_pliku, "r", encoding="utf-8-sig") as plik:
        fragmenty_sekwencji = []

        for linia in plik:
            linia = linia.strip()

            if not linia or linia.startswith(">"):
                continue

            fragmenty_sekwencji.append("".join(linia.split()))

    return "".join(fragmenty_sekwencji).upper()


def sprawdz_fragment(fragment):
    if not fragment:
        return False

    return all(nukleotyd in "ATGC" for nukleotyd in fragment)


def podzial_segmenty(sekwencja, dlugosc_segmentu):
    return [
        sekwencja[i:i + dlugosc_segmentu]
        for i in range(0, len(sekwencja), dlugosc_segmentu)
    ]


def wyszukaj_ORF(sekwencja):
    lista_ORF = []
    kodony_stop = ["TAA", "TGA", "TAG"]
    i = 0

    while i < len(sekwencja):
        if sekwencja[i:i + 3] == "ATG":
            start_ORF = i

            for j in range(i + 3, len(sekwencja), 3):
                if sekwencja[j:j + 3] in kodony_stop:
                    lista_ORF.append([
                        start_ORF + 1,
                        j + 3,
                        sekwencja[start_ORF:j + 3]
                    ])

                    i = j + 3
                    break
            else:
                i += 1
        else:
            i += 1

    return lista_ORF


# =========================================================
# ZAPIS WYNIKÓW I RAPORTU
# =========================================================

def utworz_raport(
    sekwencja, fragment, pozycje, dlugosc_segmentu,
    liczba_segmentow, liczba_wystapien, srednia,
    maksimum, tabela_orfow
):
    sciezka_pdf = KATALOG_WYNIKOW / "raport.pdf"

    # Obsługa polskich znaków w PDF, jeśli czcionki są dostępne.
    czcionka = "Helvetica"
    czcionka_bold = "Helvetica-Bold"

    sciezka_fontu = KATALOG_PROJEKTU / "Czcionki"

    plik_zwykly = sciezka_fontu / "DejaVuSans.ttf"
    plik_pogrubiony = sciezka_fontu / "DejaVuSans-Bold.ttf"

    if plik_zwykly.exists() and plik_pogrubiony.exists():
        pdfmetrics.registerFont(
            TTFont("DejaVuSansGUI", str(plik_zwykly))
        )
        pdfmetrics.registerFont(
            TTFont("DejaVuSansBoldGUI", str(plik_pogrubiony))
        )
        czcionka = "DejaVuSansGUI"
        czcionka_bold = "DejaVuSansBoldGUI"

    dokument = SimpleDocTemplate(
        str(sciezka_pdf),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    style = getSampleStyleSheet()

    style.add(ParagraphStyle(
        name="TytulDNA",
        parent=style["Title"],
        fontName=czcionka_bold
    ))

    style["Normal"].fontName = czcionka
    style["Heading2"].fontName = czcionka_bold

    elementy = [
        Paragraph("Raport analizy sekwencji DNA", style["TytulDNA"]),
        Spacer(1, 12),
        Paragraph(f"Długość sekwencji: {len(sekwencja)} nt",
                  style["Normal"]),
        Paragraph(f"Szukany motyw: {fragment}", style["Normal"]),
        Paragraph(f"Liczba wystąpień: {len(pozycje)}",
                  style["Normal"]),
        Spacer(1, 12),
        Paragraph("Pozycje wystąpień motywu", style["Heading2"])
    ]

    dane_pozycji = [["Początek", "Koniec"]] + pozycje

    tabela_pozycji = Table(
        dane_pozycji,
        repeatRows=1,
        colWidths=[150, 150]
    )

    tabela_pozycji.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), czcionka),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    elementy.append(tabela_pozycji)
    elementy.append(Spacer(1, 18))
    elementy.append(Paragraph("Statystyka segmentów", style["Heading2"]))
    elementy.append(Paragraph(
        f"Długość segmentu: {dlugosc_segmentu} nt",
        style["Normal"]
    ))
    elementy.append(Paragraph(
        f"Liczba segmentów: {len(liczba_segmentow)}",
        style["Normal"]
    ))
    elementy.append(Paragraph(
        f"Średnia liczba wystąpień: {srednia:.2f}",
        style["Normal"]
    ))
    elementy.append(Paragraph(
        f"Maksimum wystąpień w segmencie: {maksimum}",
        style["Normal"]
    ))

    elementy.append(Spacer(1, 12))
    elementy.append(Paragraph("Liczba wystąpień w segmentach",
                              style["Heading2"]))

    sciezka_wykresu = KATALOG_WYNIKOW / "wykres_segmenty.png"

    if sciezka_wykresu.exists():
        elementy.append(Image(
            str(sciezka_wykresu),
            width=480,
            height=260,
            kind="proportional"
        ))
    elementy.append(PageBreak())
    elementy.append(Spacer(1, 12))
    elementy.append(Paragraph(
        "Pozycje motywu i potencjalnych ORF-ów",
        style["Heading2"]
    ))

    sciezka_pozycji = KATALOG_WYNIKOW / "wykres_pozycje.png"

    if sciezka_pozycji.exists():
        elementy.append(Image(
            str(sciezka_pozycji),
            width=480,
            height=260,
            kind="proportional"
        ))

    elementy.append(Spacer(1, 12))
    elementy.append(Paragraph("Potencjalne ORF-y", style["Heading2"]))

    dane_orf = [
        ["Początek ORF", "Koniec ORF", "Sekwencja ORF"]
    ] + tabela_orfow

    tabela_orf = Table(
        dane_orf,
        repeatRows=1,
        colWidths=[75, 75, 330]
    )

    tabela_orf.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), czcionka),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    elementy.append(tabela_orf)
    dokument.build(elementy)


# =========================================================
# GŁÓWNA FUNKCJA ANALIZY
# =========================================================
def otworz_raport():
    sciezka_raportu = KATALOG_WYNIKOW / "raport.pdf"

    if not sciezka_raportu.exists():
        messagebox.showwarning(
            "Brak raportu",
            "Najpierw wykonaj analizę, aby wygenerować raport PDF."
        )
        return

    try:
        os.startfile(str(sciezka_raportu))
    except OSError as blad:
        messagebox.showerror(
            "Błąd otwierania raportu",
            f"Nie udało się otworzyć raportu.\n{blad}"
        )

def wykonaj_analize():
    global ostatnia_sekwencja, ostatni_motyw

    if not sciezka_pliku.get():
        messagebox.showwarning(
            "Brak pliku", "Najpierw wybierz plik z sekwencją DNA."
        )
        return

    fragment = pole_motywu.get().strip().upper()
    fragment = "".join(fragment.split())

    if not sprawdz_fragment(fragment):
        messagebox.showerror(
            "Nieprawidłowy motyw",
            "Motyw musi zawierać co najmniej jeden nukleotyd A, T, G lub C."
        )
        return

    try:
        dlugosc_segmentu = int(pole_segmentu.get())

        if dlugosc_segmentu <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Nieprawidłowa długość",
            "Długość segmentu musi być dodatnią liczbą całkowitą."
        )
        return

    try:
        sekwencja = wczytaj_sekwencje(sciezka_pliku.get())
    except (OSError, UnicodeError) as blad:
        messagebox.showerror("Błąd odczytu pliku", str(blad))
        return

    if not sekwencja:
        messagebox.showerror(
            "Pusta sekwencja", "Wybrany plik nie zawiera sekwencji DNA."
        )
        return

    if not all(nukleotyd in "ATGC" for nukleotyd in sekwencja):
        messagebox.showerror(
            "Błędna sekwencja",
            "Sekwencja zawiera znaki inne niż A, T, G i C."
        )
        return

    # Wyszukiwanie motywu
    pozycje = znajdz_fragment(sekwencja, fragment)

    # Analiza segmentów
    segmenty = podzial_segmenty(sekwencja, dlugosc_segmentu)

    liczba_wystapien = [
        len(znajdz_fragment(segment, fragment))
        for segment in segmenty
    ]

    liczba_segmentow = list(range(1, len(segmenty) + 1))

    srednia = float(np.mean(liczba_wystapien))
    maksimum = int(np.max(liczba_wystapien))

    # Tabele wynikowe
    df_pozycje = pd.DataFrame(
        pozycje, columns=["Początek", "Koniec"]
    )

    df_segmenty = pd.DataFrame({
        "Segment": liczba_segmentow,
        "Liczba wystąpień": liczba_wystapien
    })

    lista_orfow = wyszukaj_ORF(sekwencja)

    df_orf = pd.DataFrame(
        lista_orfow,
        columns=["Początek ORF", "Koniec ORF", "Sekwencja ORF"]
    )

    # Zapis CSV
    df_pozycje.to_csv(
        KATALOG_WYNIKOW / "wystąpienia_fragmentu.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_segmenty.to_csv(
        KATALOG_WYNIKOW / "liczba_wystąpień_na_segment.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_orf.to_csv(
        KATALOG_WYNIKOW / "ORFs.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # Wykres słupkowy
    figura_segmenty = Figure(figsize=(7, 4), dpi=100)
    os_segmenty = figura_segmenty.add_subplot(111)

    os_segmenty.bar(liczba_segmentow, liczba_wystapien)
    os_segmenty.set_xlabel("Segment")
    os_segmenty.set_ylabel("Liczba wystąpień")
    os_segmenty.set_title("Liczba wystąpień motywu w segmentach")
    os_segmenty.set_xlim(0.5, len(liczba_segmentow) + 0.5)

    # Ograniczenie liczby etykiet na osi X dla długich sekwencji
    if len(liczba_segmentow) <= 40:
        os_segmenty.set_xticks(liczba_segmentow)

    figura_segmenty.tight_layout()
    figura_segmenty.savefig(
        KATALOG_WYNIKOW / "wykres_segmenty.png",
        bbox_inches="tight"
    )

    # Wykres pozycji motywu i ORF-ów
    figura_pozycje = Figure(figsize=(7, 4), dpi=100)
    os_pozycje = figura_pozycje.add_subplot(111)

    # Wystąpienia motywu DNA – górny tor
    for poczatek, koniec in pozycje:
        os_pozycje.hlines(
            1, poczatek, koniec,
            color="blue", linewidth=2
        )

    # Potencjalne ORF-y – dolny tor
    for poczatek, koniec, _ in lista_orfow:
        os_pozycje.hlines(
            0, poczatek, koniec,
            color="red", linewidth=2
        )

    os_pozycje.set_title(
        "Pozycje wystąpień motywu DNA i potencjalnych ORF-ów"
    )
    os_pozycje.set_xlabel("Pozycja w sekwencji [nt]")
    os_pozycje.set_xlim(1, max(2, len(sekwencja)))

    os_pozycje.set_ylim(-0.5, 1.5)
    os_pozycje.set_yticks([0, 1])
    os_pozycje.set_yticklabels(["ORF-y", "Motyw DNA"])

    os_pozycje.grid(axis="x", linestyle="--", alpha=0.3)

    figura_pozycje.tight_layout()
    figura_pozycje.savefig(
        KATALOG_WYNIKOW / "wykres_pozycje.png",
        bbox_inches="tight"
    )

    # Raport PDF
    utworz_raport(
        sekwencja, fragment, pozycje, dlugosc_segmentu,
        liczba_segmentow, liczba_wystapien, srednia,
        maksimum, lista_orfow
    )

    # Podgląd sekwencji
    pole_podgladu.config(state="normal")
    pole_podgladu.delete("1.0", tk.END)
    pole_podgladu.insert(
        tk.END,
        f"Długość sekwencji: {len(sekwencja)} nt\n\n"
        + "\n".join(
            sekwencja[i:i + 60]
            for i in range(0, len(sekwencja), 60)
        )
    )
    pole_podgladu.config(state="disabled")

    # Aktualizacja tabel
    wypelnij_tabele(tabela_pozycji, pozycje)
    wypelnij_tabele(tabela_orfow, lista_orfow)

    etykieta_liczba_orfow.config(
        text=f"Liczba znalezionych ORF-ów: {len(lista_orfow)}"
    )

    # Aktualizacja wykresów w GUI
    for widget in ramka_wykresow.winfo_children():
        widget.destroy()

    for figura in [figura_segmenty, figura_pozycje]:
        widok = FigureCanvasTkAgg(figura, master=ramka_wykresow)
        widok.draw()
        widok.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        podlacz_przewijanie(widok.get_tk_widget())

    # Informacje o wynikach
    etykieta_wynikow.config(
        text=(
            f"Długość sekwencji: {len(sekwencja)} nt\n"
            f"Motyw: {fragment}\n"
            f"Liczba wystąpień: {len(pozycje)}\n"
            f"Średnia liczba wystąpień na segment: {srednia:.2f}\n"
            f"Maksimum w segmencie: {maksimum}\n"
        )
    )

    etykieta_raportu.config(
        text=(
            f"Wyniki zapisano w folderze:\n{KATALOG_WYNIKOW}\n\n"
            "• wystąpienia_fragmentu.csv\n"
            "• liczba_wystąpień_na_segment.csv\n"
            "• ORFs.csv\n"
            "• wykres_segmenty.png\n"
            "• wykres_pozycje.png\n"
            "• raport.pdf"
        )
    )

    ostatnia_sekwencja = sekwencja
    ostatni_motyw = fragment

    zakladki.select(zakladka_wystapienia)

    messagebox.showinfo(
        "Analiza zakończona",
        "Analiza DNA została zakończona.\n"
        f"Liczba wystąpień motywu: {len(pozycje)}\n"
        f"Liczba ORF-ów: {len(lista_orfow)}\n\n"
        f"Wyniki zapisano w:\n{KATALOG_WYNIKOW}"
    )


# =========================================================
# FUNKCJE OBSŁUGI INTERFEJSU
# =========================================================

def wybierz_plik():
    plik = filedialog.askopenfilename(
        title="Wybierz sekwencję DNA",
        initialdir=str(KATALOG_PROJEKTU / "Sekwencje"),
        filetypes=[
            ("Pliki sekwencji", "*.fasta *.fa *.txt"),
            ("Wszystkie pliki", "*.*")
        ]
    )

    if plik:
        sciezka_pliku.set(plik)
        nazwa_pliku.config(text=Path(plik).name)


def wypelnij_tabele(tabela, dane):
    tabela.delete(*tabela.get_children())

    for wiersz in dane:
        tabela.insert("", tk.END, values=wiersz)


# =========================================================
# TWORZENIE OKNA GUI
# =========================================================

root = tk.Tk()
root.title("Analiza sekwencji DNA")
root.geometry("1000x750")
root.minsize(800, 600)

# Ustawienia wyglądu aplikacji
root.configure(bg=KOLOR_TLA)

styl = ttk.Style()
styl.theme_use("clam")

styl.configure(".", font=CZCIONKA_GLOWNA)

styl.configure(
    "TNotebook",
    background=KOLOR_TLA,
    borderwidth=0
)

styl.configure(
    "TNotebook.Tab",
    background="#E5ECF4",
    foreground=KOLOR_GRANATOWY,
    padding=(16, 9),
    font=("Segoe UI", 10, "bold")
)

styl.map(
    "TNotebook.Tab",
    background=[("selected", KOLOR_PANELU)],
    foreground=[("selected", KOLOR_TURKUSOWY)]
)

styl.configure(
    "Treeview",
    background=KOLOR_PANELU,
    foreground=KOLOR_TEKSTU,
    fieldbackground=KOLOR_PANELU,
    rowheight=27,
    borderwidth=0,
    font=CZCIONKA_GLOWNA
)

styl.configure(
    "Treeview.Heading",
    background=KOLOR_GRANATOWY,
    foreground=KOLOR_PANELU,
    font=("Segoe UI", 10, "bold"),
    padding=7
)

styl.map(
    "Treeview",
    background=[("selected", "#CDEFEF")],
    foreground=[("selected", KOLOR_GRANATOWY)]
)

styl.configure("TEntry", padding=6)
styl.configure("TButton", padding=(12, 7), font=("Segoe UI", 10))

styl.configure(
    "Accent.TButton",
    background=KOLOR_TURKUSOWY,
    foreground=KOLOR_PANELU,
    padding=(14, 9),
    font=("Segoe UI", 10, "bold"),
    borderwidth=0
)

styl.configure(
    "Wykresy.TFrame",
    background=KOLOR_TLA
)

styl.map(
    "Accent.TButton",
    background=[
        ("active", KOLOR_TURKUS_HOVER),
        ("pressed", KOLOR_TURKUS_HOVER)
    ],
    foreground=[("active", KOLOR_PANELU)]
)

styl = ttk.Style(root)
styl.configure("TButton", padding=6)
styl.configure("TNotebook.Tab", padding=(12, 7))

sciezka_pliku = tk.StringVar()
pole_motywu = tk.StringVar(value="CAG")
pole_segmentu = tk.StringVar(value="100")

ostatnia_sekwencja = ""
ostatni_motyw = ""

naglowek = ttk.Frame(root, padding=12)
naglowek.pack(fill="x")

ttk.Label(
    naglowek,
    text="ANALIZA SEKWENCJI DNA",
    font=("Arial", 17, "bold")
).pack(anchor="w")

ttk.Label(
    naglowek,
    text="Wyszukiwanie motywów, analiza segmentów i ORF-ów"
).pack(anchor="w", pady=(3, 0))


# Panel ustawień
panel = ttk.LabelFrame(root, text="Parametry analizy", padding=10)
panel.pack(fill="x", padx=12, pady=5)

ttk.Button(
    panel,
    text="Wybierz plik DNA",
    style="Accent.TButton",
    command=wybierz_plik
).grid(row=0, column=0, padx=5, pady=5, sticky="w")

nazwa_pliku = ttk.Label(panel, text="Nie wybrano pliku")
nazwa_pliku.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

ttk.Label(panel, text="Motyw DNA:").grid(
    row=1, column=0, sticky="w", padx=5, pady=5
)

ttk.Entry(
    panel, textvariable=pole_motywu, width=20
).grid(row=1, column=1, sticky="w", padx=5, pady=5)

ttk.Label(panel, text="Długość segmentu [nt]:").grid(
    row=1, column=2, sticky="w", padx=5, pady=5
)

ttk.Entry(
    panel, textvariable=pole_segmentu, width=12
).grid(row=1, column=3, sticky="w", padx=5, pady=5)

ttk.Button(
    panel,
    text="URUCHOM ANALIZĘ",
    command=wykonaj_analize,
    style="Accent.TButton"
).grid(row=2, column=0, columnspan=4, pady=10)


# Nagłówek główny aplikacji
ramka_naglowka = tk.Frame(root, bg=KOLOR_TLA)
ramka_naglowka.pack(fill="x", padx=20, pady=(16, 8))

tk.Label(
    ramka_naglowka,
    text="DNA Analyzer",
    font=CZCIONKA_NAGLOWKA,
    fg=KOLOR_GRANATOWY,
    bg=KOLOR_TLA
).pack(anchor="w")

tk.Label(
    ramka_naglowka,
    text="Analiza sekwencji DNA, wyszukiwanie motywów i potencjalnych ORF-ów",
    font=CZCIONKA_GLOWNA,
    fg=KOLOR_POMOCNICZY,
    bg=KOLOR_TLA
).pack(anchor="w", pady=(2, 0))

# Zakładki
zakladki = ttk.Notebook(root)
zakladki.pack(fill="both", expand=True, padx=12, pady=(0, 10))

zakladka_analiza = ttk.Frame(zakladki, padding=10)
zakladka_wystapienia = ttk.Frame(zakladki, padding=10)
zakladka_orf = ttk.Frame(zakladki, padding=10)
zakladka_wykresy = ttk.Frame(zakladki, padding=10)
zakladka_raporty = ttk.Frame(zakladki, padding=10)

ttk.Button(
    zakladka_raporty,
    text="Otwórz raport",
    command=otworz_raport
).pack(pady=10)

zakladki.add(zakladka_analiza, text="Analiza")
zakladki.add(zakladka_wystapienia, text="Wystąpienia")
zakladki.add(zakladka_orf, text="ORF-y")
zakladki.add(zakladka_wykresy, text="Wykresy")
zakladki.add(zakladka_raporty, text="Raporty")


# Zakładka Analiza
ttk.Label(
    zakladka_analiza,
    text="Podgląd wczytanej sekwencji DNA",
    font=("Arial", 11, "bold")
).pack(anchor="w", pady=(0, 6))

ramka_podgladu = ttk.Frame(zakladka_analiza)
ramka_podgladu.pack(fill="both", expand=True)

pole_podgladu = tk.Text(
    ramka_podgladu,
    wrap="none",
    height=20,
    font=("Consolas", 11),
    state="disabled",
    bg=KOLOR_PANELU,
    fg=KOLOR_TEKSTU,
    insertbackground=KOLOR_TURKUSOWY,
    selectbackground="#CDEFEF",
    selectforeground=KOLOR_GRANATOWY,
    relief="flat",
    borderwidth=1,
    highlightthickness=1,
    highlightbackground=KOLOR_RAMKI,
    highlightcolor=KOLOR_TURKUSOWY,
    padx=10,
    pady=10
)

przewijanie_y = ttk.Scrollbar(
    ramka_podgladu, orient="vertical", command=pole_podgladu.yview
)

przewijanie_x = ttk.Scrollbar(
    zakladka_analiza, orient="horizontal",
    command=pole_podgladu.xview
)

pole_podgladu.configure(
    yscrollcommand=przewijanie_y.set,
    xscrollcommand=przewijanie_x.set
)

pole_podgladu.pack(side="left", fill="both", expand=True)
przewijanie_y.pack(side="right", fill="y")
przewijanie_x.pack(fill="x")


# Zakładka Wystąpienia
etykieta_wynikow = ttk.Label(
    zakladka_wystapienia,
    text="Wybierz plik i uruchom analizę.",
    justify="left"
)
etykieta_wynikow.pack(anchor="w", pady=(0, 10))

tabela_pozycji = ttk.Treeview(
    zakladka_wystapienia,
    columns=("Początek", "Koniec"),
    show="headings"
)

for kolumna in ("Początek", "Koniec"):
    tabela_pozycji.heading(kolumna, text=kolumna)
    tabela_pozycji.column(
        kolumna,
        width=180,
        minwidth=120,
        anchor="center",
        stretch=True
    )

tabela_pozycji.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


# Zakładka ORF-y
etykieta_liczba_orfow = ttk.Label(
    zakladka_orf,
    text="Liczba znalezionych ORF-ów: 0",
    font=CZCIONKA_SEKCJI
)
etykieta_liczba_orfow.pack(anchor="w", pady=(0, 10))

tabela_orfow = ttk.Treeview(
    zakladka_orf,
    columns=("Początek ORF", "Koniec ORF", "Sekwencja ORF"),
    show="headings"
)

tabela_orfow.heading("Początek ORF", text="Początek ORF")
tabela_orfow.heading("Koniec ORF", text="Koniec ORF")
tabela_orfow.heading("Sekwencja ORF", text="Sekwencja ORF")

tabela_orfow.column(
    "Początek ORF",
    width=130,
    minwidth=110,
    anchor="center",
    stretch=False
)

tabela_orfow.column(
    "Koniec ORF",
    width=130,
    minwidth=110,
    anchor="center",
    stretch=False
)

tabela_orfow.column(
    "Sekwencja ORF",
    width=600,
    minwidth=250,
    anchor="w",
    stretch=True
)

przewijanie_orf = ttk.Scrollbar(
    zakladka_orf, orient="vertical", command=tabela_orfow.yview
)
tabela_orfow.configure(yscrollcommand=przewijanie_orf.set)

tabela_orfow.pack(side="left", fill="both", expand=True)
przewijanie_orf.pack(side="right", fill="y")


# Zakładka Wykresy
canvas_wykresow = tk.Canvas(
    zakladka_wykresy,
    highlightthickness=0,
    background=KOLOR_TLA
)

przewijanie_wykresow = ttk.Scrollbar(
    zakladka_wykresy,
    orient="vertical",
    command=canvas_wykresow.yview
)

canvas_wykresow.configure(
    yscrollcommand=przewijanie_wykresow.set
)

przewijanie_wykresow.pack(side="right", fill="y")
canvas_wykresow.pack(side="left", fill="both", expand=True)

ramka_wykresow = ttk.Frame(
    canvas_wykresow,
    style="Wykresy.TFrame"
)

okno_wykresow = canvas_wykresow.create_window(
    (0, 0),
    window=ramka_wykresow,
    anchor="nw"
)

def aktualizuj_obszar_przewijania(event=None):
    canvas_wykresow.configure(
        scrollregion=canvas_wykresow.bbox("all")
    )

def dopasuj_szerokosc_wykresow(event):
    canvas_wykresow.itemconfigure(
        okno_wykresow,
        width=event.width
    )

ramka_wykresow.bind(
    "<Configure>",
    aktualizuj_obszar_przewijania
)

canvas_wykresow.bind(
    "<Configure>",
    dopasuj_szerokosc_wykresow
)

def przewijaj_kolkiem(event):
    canvas_wykresow.yview_scroll(
        -1 * (event.delta // 120),
        "units"
    )
    return "break"


def podlacz_przewijanie(widget):
    widget.bind("<MouseWheel>", przewijaj_kolkiem)

    for element in widget.winfo_children():
        podlacz_przewijanie(element)

# Zakładka Raporty
etykieta_raportu = ttk.Label(
    zakladka_raporty,
    text="Po uruchomieniu analizy tutaj pojawi się lista plików.",
    justify="left"
)
etykieta_raportu.pack(anchor="nw", pady=10)


# Uruchomienie aplikacji
root.mainloop()
