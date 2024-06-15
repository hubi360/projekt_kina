#System zarzadzania kinami

#Import bibliotek
import tkinter as tk
from tkinter import ttk, messagebox, END, ACTIVE
import requests
from bs4 import BeautifulSoup
import tkintermapview

#-----------------------------------------------------------------------------------------------------------------------

#Definiuje klasę Kino z konstruktorem inicjalizującym nazwę, lokalizację kina, pobiera współrzędne oraz ustawia znacznik na mapie
class Kino:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget_kina.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=self.nazwa)

#Definicja pobierz_wspolrzedne pobiera współrzędne geograficzne lokalizacji z Wikipedii, przetwarza je i zwraca jako listę współrzędnych
    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

#Definiuje klasę Pracownik z konstruktorem inicjalizującym imię, nazwisko, lokalizację pracownika, pobiera współrzędne oraz ustawia znacznik na mapie
class Pracownik:
    def __init__(self, imie, nazwisko, lokalizacja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget_pracownicy.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.imie} {self.nazwisko}")

    # Definicja pobierz_wspolrzedne pobiera współrzędne geograficzne lokalizacji z Wikipedii, przetwarza je i zwraca jako listę współrzędnych
    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

#Definiuje klasę Film z konstruktorem inicjalizującym tytuł, kino, lokalizację filmu, pobiera współrzędne oraz ustawia znacznik na mapie
class Film:
    def __init__(self, tytul, kino, lokalizacja):
        self.tytul = tytul
        self.kino = kino
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget_filmy.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.tytul} ({self.kino})")

    # Definicja pobierz_wspolrzedne pobiera współrzędne geograficzne lokalizacji z Wikipedii, przetwarza je i zwraca jako listę współrzędnych
    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

#Definiuje klasę Typu Filmu z konstruktorem inicjalizującym typ, kino, lokalizację filmu, pobiera współrzędne oraz ustawia znacznik na mapie
class TypFilmu:
    def __init__(self, typ, kino, lokalizacja):
        self.typ = typ
        self.kino = kino
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget_typy.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.typ} ({self.kino})")

    # Definicja pobierz_wspolrzedne pobiera współrzędne geograficzne lokalizacji z Wikipedii, przetwarza je i zwraca jako listę współrzędnych
    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

#-----------------------------------------------------------------------------------------------------------------------

#Funkcja logowanie sprawdza, czy nazwa użytkownika i hasło są poprawne.
# Jeśli tak, ukrywa ekran logowania, wyświetla główny interfejs ( dodaje początkowe kina,
# pracowników, filmy i typy filmów).
#W przeciwnym razie (przy złym wpisaniu loginu lub hasła) wyświetla komunikat o błędzie logowania
def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "admin" and haslo == "admin":
        zalogowany = True
        login_frame.grid_forget()
        notebook.grid(row=0, column=0, padx=10, pady=10)
        dodaj_poczatkowe_kina(), dodaj_poczatkowych_pracownikow(), dodaj_poczatkowe_filmy(), dodaj_poczatkowe_typ()

    else:
        messagebox.showerror("Błąd logowania", "Niepoprawna nazwa użytkownika lub hasło")

#-----------------------------------------------------------------------------------------------------------------------

#Funkcja dodaj_poczatkowe_kina dodaje początkowe kina do listy kin,
# a następnie aktualizuje wyświetlaną listę kin
def dodaj_poczatkowe_kina():
    poczatkowe_kina = [
        {"nazwa": "Kino Pieroga", "lokalizacja": "Warszawa", "tytul": "Smerfy"},
        {"nazwa": "Kino Cebularz", "lokalizacja": "Lublin", "filmy": "Smerfy"},
        {"nazwa": "Kino Obwarzanek", "lokalizacja": "Kraków", "filmy": "Smerfy"},
        {"nazwa": "Kino Krasnoludek", "lokalizacja": "Wrocław", "filmy": "Smerfy"}
    ]
    for kino in poczatkowe_kina:
        nowe_kino = Kino(kino["nazwa"], kino["lokalizacja"])
        kina.append(nowe_kino)
    lista_kin()

#Funkcja dodaj_poczatkowych_pracownikow dodaje początkowych pracowników do listy pracowników,
#a następnie aktualizuje wyświetlaną listę pracowników
def dodaj_poczatkowych_pracownikow():
    poczatkowych_pracownikow = [
        {"imie": "Mędrek", "nazwisko": "Pomarańczowy-Kubraczek", "lokalizacja": "Wrocław"},
        {"imie": "Gburek", "nazwisko": "Skwaszona-Mina", "lokalizacja": "Wrocław"},
        {"imie": "Apsik", "nazwisko": "Zadbany", "lokalizacja": "Wrocław"},
        {"imie": "Wesołek", "nazwisko": "Krzaczaste-Brw", "lokalizacja": "Wrocław"},
        {"imie": "Gapcio", "nazwisko": "Fioletowa-Czapka", "lokalizacja": "Wrocław"},
        {"imie": "Nieśmiałek", "nazwisko": "Wstydzioch", "lokalizacja": "Wrocław"}
    ]
    for pracownik in poczatkowych_pracownikow:
        nowy_pracownik = Pracownik(pracownik["imie"], pracownik["nazwisko"], pracownik["lokalizacja"])
        pracownicy.append(nowy_pracownik)
    lista_pracownikow()

#Funkcja dodaj_poczatkowe_filmy dodaje początkowe filmy do listy filmów,
# a następnie aktualizuje wyświetlaną listę filmów

def dodaj_poczatkowe_filmy():
    poczatkowe_filmy = [
        {"tytul": "Mission: Impossible II, Goldfinger", "kino": "Kino Pieroga", "lokalizacja": "Warszawa"},
        {"tytul": "Star Trek, Star Wars", "kino": "Kino Cebularz", "lokalizacja": "Lublin"},
        {"tytul": "Romeo i Julia, One Day", "kino": "Kino Obwarzanek", "lokalizacja": "Kraków"},
        {"tytul": "Smerfy, Królowa Śniegu", "kino": "Kino Krasnoludek", "lokalizacja": "Wrocław"}
    ]
    for film in poczatkowe_filmy:
        nowy_film = Film(film["tytul"], film["kino"], film["lokalizacja"])
        filmy.append(nowy_film)
    lista_filmow()

#Funkcja dodaj_poczatkowe_typ dodaje początkowe typy filmów do listy typów filmów,
#a następnie aktualizuje wyświetlaną listę typów filmów

def dodaj_poczatkowe_typ():
    poczatkowe_typ = [
        {"typ": "akcji", "kino": "Kino Pieroga", "lokalizacja": "Warszawa"},
        {"typ": "fantastyczny", "kino": "Kino Cebularz", "lokalizacja": "Lublin"},
        {"typ": "dramat romantyczny", "kino": "Kino Obwarzanek", "lokalizacja": "Kraków"},
        {"typ": "magiczna opowieść", "kino": "Kino Krasnoludek", "lokalizacja": "Wrocław"}
    ]
    for typfilmu in poczatkowe_typ:
        nowy_typ = TypFilmu(typfilmu["typ"], typfilmu["kino"], typfilmu["lokalizacja"])
        typy.append(nowy_typ)
    lista_typow()

#-----------------------------------------------------------------------------------------------------------------------

#Funkcja lista_kin usuwa/czysci wszystkie elementy z listy kin,
# a następnie dodaje aktualne kina do listy w GUI
def lista_kin():
    listbox_lista_kin.delete(0, END)
    for idx, kino in enumerate(kina):
        listbox_lista_kin.insert(idx, f'{kino.nazwa} {kino.lokalizacja}')

# Dodaje nowe kino do listy kin
def dodaj_kino():
    nazwa = entry_nazwa_kina.get()
    lokalizacja = entry_lokalizacja_kina.get()
    nowe_kino = Kino(nazwa, lokalizacja)
    kina.append(nowe_kino)
    lista_kin()
    entry_nazwa_kina.delete(0, END)
    entry_lokalizacja_kina.delete(0, END)
    entry_nazwa_kina.focus()

# Usuwa wybrane kino z listy kin
def usun_kino():
    i = listbox_lista_kin.index(ACTIVE)
    kina[i].marker.delete()
    kina.pop(i)
    lista_kin()

# Wyświetla szczegóły wybranego kina
def pokaz_szczegoly_kina():
    i = listbox_lista_kin.index(ACTIVE)
    nazwa = kina[i].nazwa
    lokalizacja = kina[i].lokalizacja
    wspolrzedne = kina[i].wspolrzedne
    label_nazwa_szczegoly_kina_wartosc.config(text=nazwa)
    label_lokalizacja_szczegoly_kina_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_kina_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    map_widget_kina.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget_kina.set_zoom(12)

# Edytuje wybrane kino
def edytuj_kino():
    i = listbox_lista_kin.index(ACTIVE)
    entry_nazwa_kina.insert(0, kina[i].nazwa)
    entry_lokalizacja_kina.insert(0, kina[i].lokalizacja)
    button_dodaj_kino.config(text="Zapisz zmiany", command=lambda: aktualizuj_kino(i))

# Aktualizuje wybrane kino
def aktualizuj_kino(i):
    kina[i].nazwa = entry_nazwa_kina.get()
    kina[i].lokalizacja = entry_lokalizacja_kina.get()
    kina[i].wspolrzedne = kina[i].pobierz_wspolrzedne()
    kina[i].marker.delete()
    kina[i].marker = map_widget_kina.set_marker(kina[i].wspolrzedne[0], kina[i].wspolrzedne[1], text=kina[i].nazwa)
    lista_kin()
    button_dodaj_kino.config(text="Dodaj kino", command=dodaj_kino)
    entry_nazwa_kina.delete(0, END)
    entry_lokalizacja_kina.delete(0, END)
    entry_nazwa_kina.focus()

#-----------------------------------------------------------------------------------------------------------------------

#Funkcja lista_pracowników usuwa/czysci wszystkie elementy z listy pracowników,
# a następnie dodaje aktualnych pracowników do listy w GUI

def lista_pracownikow():
    listbox_lista_pracownikow.delete(0, END)
    for idx, pracownik in enumerate(pracownicy):
        listbox_lista_pracownikow.insert(idx, f'{pracownik.imie} {pracownik.nazwisko} ({pracownik.lokalizacja})')

# Dodaje nowego pracownika do listy pracowników
def dodaj_pracownika():
    imie = entry_imie_pracownika.get()
    nazwisko = entry_nazwisko_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()
    nowy_pracownik = Pracownik(imie, nazwisko, lokalizacja)
    pracownicy.append(nowy_pracownik)
    lista_pracownikow()
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    entry_imie_pracownika.focus()

# Usuwa wybranego pracownika z listy pracowników kina
def usun_pracownika():
    i = listbox_lista_pracownikow.index(ACTIVE)
    pracownicy[i].marker.delete()
    pracownicy.pop(i)
    lista_pracownikow()

# Wyświetla szczegóły wybranego pracownika kina
def pokaz_szczegoly_pracownika():
    i = listbox_lista_pracownikow.index(ACTIVE)
    imie = pracownicy[i].imie
    nazwisko = pracownicy[i].nazwisko
    lokalizacja = pracownicy[i].lokalizacja
    wspolrzedne = pracownicy[i].wspolrzedne
    label_imie_szczegoly_pracownika_wartosc.config(text=imie)
    label_nazwisko_szczegoly_pracownika_wartosc.config(text=nazwisko)
    label_lokalizacja_szczegoly_pracownika_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_pracownika_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    map_widget_pracownicy.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget_pracownicy.set_zoom(12)

# Edytuje wybranego pracownika
def edytuj_pracownika():
    i = listbox_lista_pracownikow.index(ACTIVE)
    entry_imie_pracownika.insert(0, pracownicy[i].imie)
    entry_nazwisko_pracownika.insert(0, pracownicy[i].nazwisko)
    entry_lokalizacja_pracownika.insert(0, pracownicy[i].lokalizacja)
    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: aktualizuj_pracownika(i))

# Aktualizuje wybranego pracownika
def aktualizuj_pracownika(i):
    pracownicy[i].imie = entry_imie_pracownika.get()
    pracownicy[i].nazwisko = entry_nazwisko_pracownika.get()
    pracownicy[i].lokalizacja = entry_lokalizacja_pracownika.get()
    pracownicy[i].wspolrzedne = pracownicy[i].pobierz_wspolrzedne()
    pracownicy[i].marker.delete()
    pracownicy[i].marker = map_widget_pracownicy.set_marker(pracownicy[i].wspolrzedne[0], pracownicy[i].wspolrzedne[1], text=f"{pracownicy[i].imie} {pracownicy[i].nazwisko}")
    lista_pracownikow()
    button_dodaj_pracownika.config(text="Dodaj pracownika", command=dodaj_pracownika)
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    entry_imie_pracownika.focus()


#-----------------------------------------------------------------------------------------------------------------------

#Funkcja lista_filmóww usuwa/czysci wszystkie elementy z listy fil,ów,
# a następnie dodaje aktualnych filmów do listy w GUI
def lista_filmow():
    listbox_lista_filmow.delete(0, END)
    for idx, film in enumerate(filmy):
        listbox_lista_filmow.insert(idx, f'{film.tytul} ({film.kino}) {film.lokalizacja}')

# Dodaje nowy film do listy filmów
def dodaj_film():
    tytul = entry_tytul_filmu.get()
    kino = entry_kino_filmu.get()
    lokalizacja = entry_lokalizacja_filmu.get()
    nowy_film = Film(tytul, kino, lokalizacja)
    filmy.append(nowy_film)
    lista_filmow()
    entry_tytul_filmu.delete(0, END)
    entry_kino_filmu.delete(0, END)
    entry_lokalizacja_filmu.delete(0, END)
    entry_tytul_filmu.focus()

# Usuwa wybrany film z listy filmów
def usun_film():
    i = listbox_lista_filmow.index(ACTIVE)
    filmy[i].marker.delete()
    filmy.pop(i)
    lista_filmow()


# Wyświetla szczegóły wybranego filmu
def pokaz_szczegoly_filmu():
    i = listbox_lista_filmow.index(ACTIVE)
    tytul = filmy[i].tytul
    kino = filmy[i].kino
    lokalizacja = filmy[i].lokalizacja
    wspolrzedne = filmy[i].wspolrzedne
    label_tytul_szczegoly_filmu_wartosc.config(text=tytul)
    label_kino_szczegoly_filmu_wartosc.config(text=kino)
    label_lokalizacja_szczegoly_filmu_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_filmu_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    map_widget_filmy.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget_filmy.set_zoom(12)

# Edytuje wybrany film
def edytuj_film():
    i = listbox_lista_filmow.index(ACTIVE)
    entry_tytul_filmu.insert(0, filmy[i].tytul)
    entry_kino_filmu.insert(0, filmy[i].kino)
    entry_lokalizacja_filmu.insert(0, filmy[i].lokalizacja)
    button_dodaj_film.config(text="Zapisz zmiany", command=lambda: aktualizuj_film(i))

# Aktualizuje wybrany film
def aktualizuj_film(i):
    filmy[i].tytul = entry_tytul_filmu.get()
    filmy[i].kino = entry_kino_filmu.get()
    filmy[i].lokalizacja = entry_lokalizacja_filmu.get()
    filmy[i].wspolrzedne = filmy[i].pobierz_wspolrzedne()
    filmy[i].marker.delete()
    filmy[i].marker = map_widget_filmy.set_marker(filmy[i].wspolrzedne[0], filmy[i].wspolrzedne[1], text=f"{filmy[i].tytul} ({filmy[i].kino})")
    lista_filmow()
    button_dodaj_film.config(text="Dodaj film", command=dodaj_film)
    entry_tytul_filmu.delete(0, END)
    entry_kino_filmu.delete(0, END)
    entry_lokalizacja_filmu.delete(0, END)
    entry_tytul_filmu.focus()


#-----------------------------------------------------------------------------------------------------------------------

#Funkcja lista_filmóww usuwa/czysci wszystkie elementy z listy fil,ów,
# a następnie dodaje aktualnych filmów do listy w GUI
def lista_typow():
    listbox_lista_typow.delete(0, END)
    for idx, typ in enumerate(typy):
        listbox_lista_typow.insert(idx, f'{typ.typ} ({typ.kino}) {typ.lokalizacja}')

# Dodaje nowy typ filmu do listy typów filmów
def dodaj_typ():
    typ = entry_typ_filmu.get()
    kino = entry_kino_typu.get()
    lokalizacja = entry_lokalizacja_typu.get()
    nowy_typ = TypFilmu(typ, kino, lokalizacja)
    typy.append(nowy_typ)
    lista_typow()
    entry_typ_filmu.delete(0, END)
    entry_kino_typu.delete(0, END)
    entry_lokalizacja_typu.delete(0, END)
    entry_typ_filmu.focus()

# Usuwa wybrany gatunek filum z listy gatunków filmów
def usun_typ():
    i = listbox_lista_typow.index(ACTIVE)
    typy[i].marker.delete()
    typy.pop(i)
    lista_typow()

# Wyświetla szczegóły wybranego gatunku filmu
def pokaz_szczegoly_typu():
    i = listbox_lista_typow.index(ACTIVE)
    typ = typy[i].typ
    kino = typy[i].kino
    lokalizacja = typy[i].lokalizacja
    wspolrzedne = typy[i].wspolrzedne
    label_typ_szczegoly_typu_wartosc.config(text=typ)
    label_kino_szczegoly_typu_wartosc.config(text=kino)
    label_lokalizacja_szczegoly_typu_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_typu_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    map_widget_typy.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget_typy.set_zoom(12)

# Edytuje wybrany gatunek filmu
def edytuj_typ():
    i = listbox_lista_typow.index(ACTIVE)
    entry_typ_filmu.insert(0, typy[i].typ)
    entry_kino_typu.insert(0, typy[i].kino)
    entry_lokalizacja_typu.insert(0, typy[i].lokalizacja)
    button_dodaj_typ.config(text="Zapisz zmiany", command=lambda: aktualizuj_typ(i))

# Aktualizuje wybrany typ filmu
def aktualizuj_typ(i):
    typy[i].typ = entry_typ_filmu.get()
    typy[i].kino = entry_kino_typu.get()
    typy[i].lokalizacja = entry_lokalizacja_typu.get()
    typy[i].wspolrzedne = typy[i].pobierz_wspolrzedne()
    typy[i].marker.delete()
    typy[i].marker = map_widget_typy.set_marker(typy[i].wspolrzedne[0], typy[i].wspolrzedne[1], text=f"{typy[i].typ} ({typy[i].kino})")
    lista_typow()
    button_dodaj_typ.config(text="Dodaj typ", command=dodaj_typ)
    entry_typ_filmu.delete(0, END)
    entry_kino_typu.delete(0, END)
    entry_lokalizacja_typu.delete(0, END)
    entry_typ_filmu.focus()

#-----------------------------------------------------------------------------------------------------------------------

#Tworzy główne okno aplikacji i ustawia jego tytuł na "System zarządzania kinami"

root = tk.Tk()
root.title("SYSTEM ZARZADZANIA KINAMI")
root.geometry("1500x900")

#Tworzy ramke do logowania
login_frame = tk.Frame(root)
login_frame.grid(row=0, column=0, padx=10, pady=10)

# Tworzy miejsce do wpisania nazwy użytkownika
label_nazwa_uzytkownika = tk.Label(login_frame, text="Nazwa użytkownika")
label_nazwa_uzytkownika.grid(row=0, column=0, padx=10, pady=5)
entry_nazwa_uzytkownika = tk.Entry(login_frame)
entry_nazwa_uzytkownika.grid(row=0, column=1, padx=10, pady=5)

# Tworzy miejsce do wpisania hasła
label_haslo = tk.Label(login_frame, text="Hasło")
label_haslo.grid(row=1, column=0, padx=10, pady=5)
entry_haslo = tk.Entry(login_frame, show="*")
entry_haslo.grid(row=1, column=1, padx=10, pady=5)

# Tworzy przycisk zaloguj
button_zaloguj = tk.Button(login_frame, text="Zaloguj", command=logowanie)
button_zaloguj.grid(row=2, column=0, columnspan=2, pady=10)

# Tworzy notebooka w którym będą zakładki Kina, Pracownicy, Filmy i Typy filmów
notebook = ttk.Notebook(root)

frame_kina = ttk.Frame(notebook)
frame_pracownicy = ttk.Frame(notebook)
frame_filmy = ttk.Frame(notebook)
frame_typy = ttk.Frame(notebook)

notebook.add(frame_kina, text="Kina")
notebook.add(frame_pracownicy, text="Pracownicy")
notebook.add(frame_filmy, text="Filmy")
notebook.add(frame_typy, text="Typy filmów")

#-----------------------------------------------------------------------------------------------------------------------
# Kina

#Lista Kin
# Kina

#Lista Kin
kina = []

#Tworzy trzy ramki Liste, Formularz do edycji lub dodawania i szczegóły wybranego obiektu z listy wzraz mapą

ramka_lista_kin = ttk.Frame(frame_kina)
ramka_formularz = ttk.Frame(frame_kina)
ramka_szczegoly_kina = ttk.Frame(frame_kina)

ramka_lista_kin.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_kina.grid(row=1, column=0, columnspan=2, padx=50, pady=20)


#Tworzy napis, a podnapsiem listboxa
label_lista_kin = tk.Label(ramka_lista_kin, text="Lista kin")
listbox_lista_kin = tk.Listbox(ramka_lista_kin)

#klikanie na szczegoly kina - dzieki dwu-kliku można wyświetlic szczegóły
listbox_lista_kin.bind('<Double-Button-1>', lambda e: pokaz_szczegoly_kina())

#Tworzy przycisk usun wybrane kino i przycisk edytuj wybrane kino
button_usun_kino = tk.Button(ramka_lista_kin, text="Usuń kino", command=usun_kino)
button_edytuj_kino = tk.Button(ramka_lista_kin, text="Edytuj kino", command=edytuj_kino)

# Lokalizacja w ramka_lista_kin: przysików, listboxa, czy nazwy okna
label_lista_kin.grid(row=0, column=0, padx=10, pady=5)
listbox_lista_kin.grid(row=1, column=0, rowspan=6, padx=10, pady=5)
button_usun_kino.grid(row=1, column=1, padx=10, pady=5)
button_edytuj_kino.grid(row=2, column=1, padx=10, pady=5)


#Tworzy formularz (ramka_formularz) w którym jest okna do wpisania lub edycji nazwy kina i lokalizacji kina

# Etykiety
label_formularz = tk.Label(ramka_formularz, text="Formularz")
label_nazwa = tk.Label(ramka_formularz, text="Nazwa kina: ")
label_lokalizacja = tk.Label(ramka_formularz, text="Lokalizacja kina: ")

# Tworzy okna do wpisywania
entry_nazwa_kina = tk.Entry(ramka_formularz)
entry_lokalizacja_kina = tk.Entry(ramka_formularz)

#Tworzy przycisk dodwania kina
button_dodaj_kino = tk.Button(ramka_formularz, text="Dodaj kino", command=dodaj_kino)

# Lokalizacja w ramka_formularz: przysiku, okien do wpisywania, nazw okien (Etykiety)
label_formularz.grid(row=2, column=1)
label_nazwa.grid(row=3, column=0, padx=10, pady=5)
entry_nazwa_kina.grid(row=3, column=1, padx=50, pady=40)
label_lokalizacja.grid(row=4, column=0, padx=10, pady=5)
entry_lokalizacja_kina.grid(row=4, column=1, padx=10, pady=5)
button_dodaj_kino.grid(row=5, column=1, padx=10, pady=5)


#Wyświetlenie szegółów wybranego kina w ramce - ramka_szczegoly_kina
#Etykiety
label_szczegoly_kina = tk.Label(ramka_szczegoly_kina, text="Szczegóły kina")
label_nazwa_szczegoly_kina = tk.Label(ramka_szczegoly_kina, text="Nazwa Kina:")
label_nazwa_szczegoly_kina_wartosc = tk.Label(ramka_szczegoly_kina, text="...")
label_lokalizacja_szczegoly_kina = tk.Label(ramka_szczegoly_kina, text="Lokalizacja Kina:")
label_lokalizacja_szczegoly_kina_wartosc = tk.Label(ramka_szczegoly_kina, text="...")
label_wspolrzedne_szczegoly_kina = tk.Label(ramka_szczegoly_kina, text="Współrzędne kina:")
label_wspolrzedne_szczegoly_kina_wartosc = tk.Label(ramka_szczegoly_kina, text="...")

#Lokalizacja Etykiet oraz wartosci pojwiających się w ramka_szczegoly_kina
label_szczegoly_kina.grid(row=6, column=0, columnspan=2)
label_nazwa_szczegoly_kina.grid(row=7, column=0, sticky='e')
label_nazwa_szczegoly_kina_wartosc.grid(row=7, column=1, sticky='w')
label_lokalizacja_szczegoly_kina.grid(row=8, column=0, sticky='e')
label_lokalizacja_szczegoly_kina_wartosc.grid(row=8, column=1, sticky='w')
label_wspolrzedne_szczegoly_kina.grid(row=9, column=0, sticky='e')
label_wspolrzedne_szczegoly_kina_wartosc.grid(row=9, column=1, sticky='w')

#Tworzy pod szczegółami mape która będzie wyśrodkowana na Warszawie z zoomem 7
map_widget_kina = tkintermapview.TkinterMapView(ramka_szczegoly_kina, width=1000, height=400)
map_widget_kina.grid(row=10, column=0, columnspan=2)
map_widget_kina.set_position(52.2, 21.0)
map_widget_kina.set_zoom(7)


#-----------------------------------------------------------------------------------------------------------------------
# Pracownicy

#Lista pracowników
pracownicy = []

#Tworzy trzy ramki Liste, Formularz do edycji lub dodawania i szczegóły wybranego obiektu z listy wzraz mapą

ramka_lista_pracownikow = ttk.Frame(frame_pracownicy)
ramka_formularz_pracownikow = ttk.Frame(frame_pracownicy)
ramka_szczegoly_pracownikow = ttk.Frame(frame_pracownicy)

ramka_lista_pracownikow.grid(row=0, column=0, padx=50)
ramka_formularz_pracownikow.grid(row=0, column=1)
ramka_szczegoly_pracownikow.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

#Tworzy napis, a podnapsiem listboxa
label_lista_pracownikow = tk.Label(ramka_lista_pracownikow, text="Lista pracowników")
listbox_lista_pracownikow = tk.Listbox(ramka_lista_pracownikow)

#klikanie na szczegoly pracownika - dzieki dwu-kliku można wyświetlic szczegóły
listbox_lista_pracownikow.bind('<Double-Button-1>', lambda e: pokaz_szczegoly_pracownika())
#Tworzy przycisk usun wybrane kino i przycisk edytuj wybranego pracownika
button_usun_pracownika = tk.Button(ramka_lista_pracownikow, text="Usuń pracownika", command=usun_pracownika)
button_edytuj_pracownika = tk.Button(ramka_lista_pracownikow, text="Edytuj pracownika", command=edytuj_pracownika)

# Lokalizacja w ramka_lista_pracownikow: przysików, listboxa, czy nazwy okna
label_lista_pracownikow.grid(row=0, column=0, padx=10, pady=5)
listbox_lista_pracownikow.grid(row=1, column=0, rowspan=4, padx=10, pady=5)
button_usun_pracownika.grid(row=1, column=1, padx=10, pady=5)
button_edytuj_pracownika.grid(row=2, column=1, padx=10, pady=5)

#Tworzy formularz (ramka_formularz) w którym jest okna do wpisania lub edycji imienia, nazwiska i lokalizacji pracownika
#Etykiety
label_formularz_pracownikow = tk.Label(ramka_formularz_pracownikow, text="Formularz pracowników")
label_imie_pracownika = tk.Label(ramka_formularz_pracownikow, text="Imie pracownika kina: ")
label_mazwisko_pracownika = tk.Label(ramka_formularz_pracownikow, text="Nazwisko pracownika kina: ")
label_lokalizacja_pracownika = tk.Label(ramka_formularz_pracownikow, text="Lokalizacja pracownika kina: ")
#Pola gdzie pojawi się do edycji pracownika lub do wpisania nowego pracownika
entry_imie_pracownika = tk.Entry(ramka_formularz_pracownikow)
entry_nazwisko_pracownika = tk.Entry(ramka_formularz_pracownikow)
entry_lokalizacja_pracownika = tk.Entry(ramka_formularz_pracownikow)
#Przycisk dodaj
button_dodaj_pracownika = tk.Button(ramka_formularz_pracownikow, text="Dodaj pracownika", command=dodaj_pracownika)

# Lokalizacja w ramka_formularz_pracownikow: przysików, listboxa, czy nazwy okna
label_formularz_pracownikow.grid(row=2, column=1)
label_imie_pracownika.grid(row=3, column=0, padx=10, pady=5)
entry_imie_pracownika.grid(row=3, column=1, padx=10, pady=5)
label_mazwisko_pracownika.grid(row=4, column=0, padx=10, pady=5)
entry_nazwisko_pracownika.grid(row=4, column=1, padx=10, pady=5)
label_lokalizacja_pracownika.grid(row=5, column=0, padx=10, pady=5)
entry_lokalizacja_pracownika.grid(row=5, column=1, padx=10, pady=5)
button_dodaj_pracownika.grid(row=6, column=1, padx=10, pady=5)

#Wyświetlenie szczegółów wybranego pracownika w ramce - ramka_szczegoly
#Etykiety
label_szczegoly_pracownika = tk.Label(ramka_szczegoly_pracownikow, text="Szczegóły pracownika")
label_imie_szczegoly_pracownika = tk.Label(ramka_szczegoly_pracownikow, text="Imię:")
label_imie_szczegoly_pracownika_wartosc = tk.Label(ramka_szczegoly_pracownikow, text="...")
label_nazwisko_szczegoly_pracownika = tk.Label(ramka_szczegoly_pracownikow, text="Nazwisko:")
label_nazwisko_szczegoly_pracownika_wartosc = tk.Label(ramka_szczegoly_pracownikow, text="...")
label_lokalizacja_szczegoly_pracownika = tk.Label(ramka_szczegoly_pracownikow, text="Lokalizacja:")
label_lokalizacja_szczegoly_pracownika_wartosc = tk.Label(ramka_szczegoly_pracownikow, text="...")
label_wspolrzedne_szczegoly_pracownika = tk.Label(ramka_szczegoly_pracownikow, text="Współrzędne:")
label_wspolrzedne_szczegoly_pracownika_wartosc = tk.Label(ramka_szczegoly_pracownikow, text="...")

#Lokalizacja Etykiet oraz wartosci pojwiających się w ramka_szczegoly_pracownikow
label_szczegoly_pracownika.grid(row=7, column=0, columnspan=2)
label_imie_szczegoly_pracownika.grid(row=8, column=0, sticky='e')
label_imie_szczegoly_pracownika_wartosc.grid(row=8, column=1, sticky='w')
label_nazwisko_szczegoly_pracownika.grid(row=9, column=0, sticky='e')
label_nazwisko_szczegoly_pracownika_wartosc.grid(row=9, column=1, sticky='w')
label_lokalizacja_szczegoly_pracownika.grid(row=10, column=0, sticky='e')
label_lokalizacja_szczegoly_pracownika_wartosc.grid(row=10, column=1, sticky='w')
label_wspolrzedne_szczegoly_pracownika.grid(row=11, column=0, sticky='e')
label_wspolrzedne_szczegoly_pracownika_wartosc.grid(row=11, column=1, sticky='w')

#Tworzy pod szczegółami mape która będzie wyśrodkowana na Wrocław z zoomem 7
map_widget_pracownicy = tkintermapview.TkinterMapView(ramka_szczegoly_pracownikow, width=1000, height=400)
map_widget_pracownicy.grid(row=12, column=0, columnspan=2)
map_widget_pracownicy.set_position(51.1, 17.0)
map_widget_pracownicy.set_zoom(7)

#-----------------------------------------------------------------------------------------------------------------------
# Filmy

#Lista filmy
filmy = []

#Tworzy trzy ramki Liste, Formularz do edycji lub dodawania i szczegóły wybranego obiektu z listy wzraz mapą

ramka_lista_filmow = ttk.Frame(frame_filmy)
ramka_formularz_filmow = ttk.Frame(frame_filmy)
ramka_szczegoly_filmow = ttk.Frame(frame_filmy)

ramka_lista_filmow.grid(row=0, column=0, padx=50)
ramka_formularz_filmow.grid(row=0, column=1)
ramka_szczegoly_filmow.grid(row=1, column=0, columnspan=2, padx=50, pady=20)


#Tworzy napis, a podnapsiem listboxa
label_lista_filmow = tk.Label(ramka_lista_filmow, text="Lista filmów")
listbox_lista_filmow = tk.Listbox(ramka_lista_filmow)
#klikanie na szczegoly filmu - dzieki dwu-kliku można wyświetlic szczegóły
listbox_lista_filmow.bind('<Double-Button-1>', lambda e: pokaz_szczegoly_filmu())

#Tworzy przycisk usun wybrane kino i przycisk edytuj wybrany film
button_usun_film = tk.Button(ramka_lista_filmow, text="Usuń film", command=usun_film)
button_edytuj_film = tk.Button(ramka_lista_filmow, text="Edytuj film", command=edytuj_film)

# Lokalizacja w ramka_lista_filmow: przysików, listboxa, czy nazwy okna
label_lista_filmow.grid(row=0, column=0, padx=10, pady=5)
listbox_lista_filmow.grid(row=1, column=0, rowspan=4, padx=10, pady=5)
button_usun_film.grid(row=1, column=1, padx=10, pady=5)
button_edytuj_film.grid(row=2, column=1, padx=10, pady=5)

#Tworzy formularz (ramka_formularz) w którym jest okna do wpisania lub edycji Tytuł filmu,
# kino w którym gra film i lokalizacji kina
#etykiety
label_formularz_filmow = tk.Label(ramka_formularz_filmow, text="Formularz filmów")
label_tytul_filmu = tk.Label(ramka_formularz_filmow, text="Tytuł filmu: ")
label_kino_filmu = tk.Label(ramka_formularz_filmow, text="Kino w którym gra film: ")
label_lokalizacja_filmu = tk.Label(ramka_formularz_filmow, text="Lokalizacka kina w którym gra film: ")

# Tworzy okna do wpisywania
entry_tytul_filmu = tk.Entry(ramka_formularz_filmow)
entry_kino_filmu = tk.Entry(ramka_formularz_filmow)
entry_lokalizacja_filmu = tk.Entry(ramka_formularz_filmow)
#Tworzy przycisk dodawania filmu
button_dodaj_film = tk.Button(ramka_formularz_filmow, text="Dodaj film", command=dodaj_film)

# Lokalizacja w ramka_formularz_filmow: przysiku, okien do wpisywania, nazw okien (Etykiety)
label_formularz_filmow.grid(row=2, column=1)
label_tytul_filmu.grid(row=3, column=0, padx=10, pady=5)
entry_tytul_filmu.grid(row=3, column=1, padx=10, pady=5)
label_kino_filmu.grid(row=4, column=0, padx=10, pady=5)
entry_kino_filmu.grid(row=4, column=1, padx=10, pady=5)
label_lokalizacja_filmu.grid(row=5, column=0, padx=10, pady=5)
entry_lokalizacja_filmu.grid(row=5, column=1, padx=10, pady=5)
button_dodaj_film.grid(row=6, column=1, padx=10, pady=5)

#Wyświetlenie szczegółów wybranego filmu w ramce - ramka_szczegoly_kin
#Etykiety
label_szczegoly_filmu = tk.Label(ramka_szczegoly_filmow , text="Szczegóły filmu")
label_tytul_szczegoly_filmu = tk.Label(ramka_szczegoly_filmow, text="Tytuł:")
label_tytul_szczegoly_filmu_wartosc = tk.Label(ramka_szczegoly_filmow, text="...")
label_kino_szczegoly_filmu = tk.Label(ramka_szczegoly_filmow, text="Kino:")
label_kino_szczegoly_filmu_wartosc = tk.Label(ramka_szczegoly_filmow, text="...")
label_lokalizacja_szczegoly_filmu = tk.Label(ramka_szczegoly_filmow, text="Lokalizacja:")
label_lokalizacja_szczegoly_filmu_wartosc = tk.Label(ramka_szczegoly_filmow, text="...")
label_wspolrzedne_szczegoly_filmu = tk.Label(ramka_szczegoly_filmow, text="Współrzędne:")
label_wspolrzedne_szczegoly_filmu_wartosc = tk.Label(ramka_szczegoly_filmow, text="...")

#Lokalizacja Etykiet oraz wartosci pojwiających się w ramka_szczegoly_filmow
label_szczegoly_filmu.grid(row=7, column=0, columnspan=2)
label_tytul_szczegoly_filmu.grid(row=8, column=0, sticky='e')
label_tytul_szczegoly_filmu_wartosc.grid(row=8, column=1, sticky='w')
label_kino_szczegoly_filmu.grid(row=9, column=0, sticky='e')
label_kino_szczegoly_filmu_wartosc.grid(row=9, column=1, sticky='w')
label_lokalizacja_szczegoly_filmu.grid(row=10, column=0, sticky='e')
label_lokalizacja_szczegoly_filmu_wartosc.grid(row=10, column=1, sticky='w')
label_wspolrzedne_szczegoly_filmu.grid(row=11, column=0, sticky='e')
label_wspolrzedne_szczegoly_filmu_wartosc.grid(row=11, column=1, sticky='w')

#Tworzy pod szczegółami mape która będzie wyśrodkowana na Warszawie z zoomem 7
map_widget_filmy = tkintermapview.TkinterMapView(ramka_szczegoly_filmow, width=1000, height=400)
map_widget_filmy.grid(row=12, column=0, columnspan=2)
map_widget_filmy.set_position(52.2, 21.0)
map_widget_filmy.set_zoom(7)

#-----------------------------------------------------------------------------------------------------------------------
# Typy filmów

#Lista typów filmów
typy = []

#Tworzy trzy ramki Liste, Formularz do edycji lub dodawania i szczegóły wybranego obiektu z listy wzraz mapą
ramka_lista_typ = ttk.Frame(frame_typy)
ramka_formularz_typ = ttk.Frame(frame_typy)
ramka_szczegoly_typ = ttk.Frame(frame_typy)

ramka_lista_typ.grid(row=0, column=0, padx=50)
ramka_formularz_typ.grid(row=0, column=1)
ramka_szczegoly_typ.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

#Tworzy napis, a podnapsiem listboxa
label_lista_typow = tk.Label(ramka_lista_typ, text="Lista typów filmów")
listbox_lista_typow = tk.Listbox(ramka_lista_typ)
#klikanie na szczegoly typu - dzieki dwu-kliku można wyświetlic szczegóły
listbox_lista_typow.bind('<Double-Button-1>', lambda e: pokaz_szczegoly_typu())
#Tworzy przycisk usun wybrane kino i przycisk edytuj wybranego typu
button_usun_typ = tk.Button(ramka_lista_typ, text="Usuń typ", command=usun_typ)
button_edytuj_typ = tk.Button(ramka_lista_typ, text="Edytuj typ", command=edytuj_typ)

# Lokalizacja w ramka_lista_typ: przysików, listboxa, czy nazwy okna
label_lista_typow.grid(row=0, column=0, padx=10, pady=5)
listbox_lista_typow.grid(row=1, column=0, rowspan=4, padx=10, pady=5)
button_usun_typ.grid(row=1, column=1, padx=10, pady=5)
button_edytuj_typ.grid(row=2, column=1, padx=10, pady=5)


#Tworzy formularz (ramka_formularz) w którym jest okna do wpisania lub edycji
# Typ lub typy filmów, nazwy kina i lokalizacji kina
#Etykiety
label_formularz_typ = tk.Label(ramka_formularz_typ, text="Formularz typów filmów granym w danym kinie")
label_typ_filmu = tk.Label(ramka_formularz_typ, text="Typ lub typy filmów: ")
label_kino_typu = tk.Label(ramka_formularz_typ, text="Nazwa kina: ")
label_lokalizacja_typu = tk.Label(ramka_formularz_typ, text="Lokalizacja kina: ")

# Tworzy okna do wpisywania
entry_typ_filmu = tk.Entry(ramka_formularz_typ)
entry_kino_typu = tk.Entry(ramka_formularz_typ)
entry_lokalizacja_typu = tk.Entry(ramka_formularz_typ)
#Tworzy przycisk dodwania typu
button_dodaj_typ = tk.Button(ramka_formularz_typ, text="Dodaj typ", command=dodaj_typ)

# Lokalizacja w ramka_formularz_typ: przysiku, okien do wpisywania, nazw okien (Etykiety)
label_formularz_typ.grid(row=2, column=1)
label_typ_filmu.grid(row=3, column=0, padx=10, pady=5)
entry_typ_filmu.grid(row=3, column=1, padx=10, pady=5)
label_kino_typu.grid(row=4, column=0, padx=10, pady=5)
entry_kino_typu.grid(row=4, column=1, padx=10, pady=5)
label_lokalizacja_typu.grid(row=5, column=0, padx=10, pady=5)
entry_lokalizacja_typu.grid(row=5, column=1, padx=10, pady=5)
button_dodaj_typ.grid(row=6, column=1, padx=10, pady=5)

#Wyświetlenie szczegółów wybranego gratunku filmu w ramce - ramka_szczegoly
#Etykiety
label_szczegoly_typu = tk.Label(ramka_szczegoly_typ, text="Szczegóły typu filmu")
label_typ_szczegoly_typu = tk.Label(ramka_szczegoly_typ, text="Typ:")
label_typ_szczegoly_typu_wartosc = tk.Label(ramka_szczegoly_typ, text="...")
label_kino_szczegoly_typu = tk.Label(ramka_szczegoly_typ, text="Kino:")
label_kino_szczegoly_typu_wartosc = tk.Label(ramka_szczegoly_typ, text="...")
label_lokalizacja_szczegoly_typu = tk.Label(ramka_szczegoly_typ, text="Lokalizacja:")
label_lokalizacja_szczegoly_typu_wartosc = tk.Label(ramka_szczegoly_typ, text="...")
label_wspolrzedne_szczegoly_typu = tk.Label(ramka_szczegoly_typ, text="Współrzędne:")
label_wspolrzedne_szczegoly_typu_wartosc = tk.Label(ramka_szczegoly_typ, text="...")

#Lokalizacja Etykiet oraz wartosci pojwiających się w ramka_szczegoly_typ
label_szczegoly_typu.grid(row=7, column=0, columnspan=2)
label_typ_szczegoly_typu.grid(row=8, column=0, sticky='e')
label_typ_szczegoly_typu_wartosc.grid(row=8, column=1, sticky='w')
label_kino_szczegoly_typu.grid(row=9, column=0, sticky='e')
label_kino_szczegoly_typu_wartosc.grid(row=9, column=1, sticky='w')
label_lokalizacja_szczegoly_typu.grid(row=10, column=0, sticky='e')
label_lokalizacja_szczegoly_typu_wartosc.grid(row=10, column=1, sticky='w')
label_wspolrzedne_szczegoly_typu.grid(row=11, column=0, sticky='e')
label_wspolrzedne_szczegoly_typu_wartosc.grid(row=11, column=1, sticky='w')


#Tworzy pod szczegółami mape która będzie wyśrodkowana na Warszawie z zoomem 7
map_widget_typy = tkintermapview.TkinterMapView(ramka_szczegoly_typ, width=1000, height=400)
map_widget_typy.grid(row=12, column=0, columnspan=2)
map_widget_typy.set_position(52.2, 21.0)
map_widget_typy.set_zoom(7)

#-----------------------------------------------------------------------------------------------------------------------

#Zamykanie okna
root.mainloop()
