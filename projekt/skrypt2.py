from tkinter import *
from tkinter import messagebox
import requests
import tkintermapview
from bs4 import BeautifulSoup

# ustawienia
kina = []
zalogowany = False

class Kino:
    def __init__(self, nazwa, lokalizacja, pracownicy):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.pracownicy = pracownicy
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.nazwa} ({self.pracownicy} pracowników)")

    def pobierz_wspolrzedne(self):
        url = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]

def lista_kin():
    listbox_lista_kin.delete(0, END)
    for idx, kino in enumerate(kina):
        listbox_lista_kin.insert(idx, f'{kino.nazwa} {kino.lokalizacja} ({kino.pracownicy} pracowników)')

def dodaj_kino():
    nazwa = entry_nazwa.get()
    lokalizacja = entry_lokalizacja.get()
    pracownicy = int(entry_pracownicy.get())
    nowe_kino = Kino(nazwa, lokalizacja, pracownicy)
    kina.append(nowe_kino)
    lista_kin()
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_pracownicy.delete(0, END)
    entry_nazwa.focus()

def usun_kino():
    i = listbox_lista_kin.index(ACTIVE)
    kina[i].marker.delete()
    kina.pop(i)
    lista_kin()

def pokaz_szczegoly_kina():
    i = listbox_lista_kin.index(ACTIVE)
    nazwa = kina[i].nazwa
    lokalizacja = kina[i].lokalizacja
    wspolrzedne = kina[i].wspolrzedne
    pracownicy = kina[i].pracownicy
    label_nazwa_szczegoly_kina_wartosc.config(text=nazwa)
    label_lokalizacja_szczegoly_kina_wartosc.config(text=lokalizacja)
    label_wspolrzedne_szczegoly_kina_wartosc.config(text=f"{wspolrzedne[0]:.2f}, {wspolrzedne[1]:.2f}")
    label_pracownicy_szczegoly_kina_wartosc.config(text=pracownicy)
    map_widget.set_position(wspolrzedne[0], wspolrzedne[1])
    map_widget.set_zoom(12)

def edytuj_kino():
    i = listbox_lista_kin.index(ACTIVE)
    entry_nazwa.insert(0, kina[i].nazwa)
    entry_lokalizacja.insert(0, kina[i].lokalizacja)
    entry_pracownicy.insert(0, kina[i].pracownicy)
    button_dodaj_kino.config(text="Zapisz zmiany", command=lambda: aktualizuj_kino(i))

def aktualizuj_kino(i):
    kina[i].nazwa = entry_nazwa.get()
    kina[i].lokalizacja = entry_lokalizacja.get()
    kina[i].pracownicy = int(entry_pracownicy.get())
    kina[i].wspolrzedne = kina[i].pobierz_wspolrzedne()
    kina[i].marker.delete()
    kina[i].marker = map_widget.set_marker(kina[i].wspolrzedne[0], kina[i].wspolrzedne[1], text=f"{kina[i].nazwa} ({kina[i].pracownicy} pracowników)")
    lista_kin()
    button_dodaj_kino.config(text="Dodaj kino", command=dodaj_kino)
    entry_nazwa.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_pracownicy.delete(0, END)
    entry_nazwa.focus()

def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "admin" and haslo == "admin":
        zalogowany = True
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0, padx=50)
        dodaj_poczatkowe_kina()
    else:
        messagebox.showerror("Błąd logowania", "Niepoprawna nazwa użytkownika lub hasło")

def dodaj_poczatkowe_kina():
    poczatkowe_kina = [
        {"nazwa": "Kino Pieroga", "lokalizacja": "Warszawa", "pracownicy": 13},
        {"nazwa": "Kino Cebularz", "lokalizacja": "Lublin", "pracownicy": 6},
        {"nazwa": "Kino Obwarzanek", "lokalizacja": "Kraków", "pracownicy": 10},
        {"nazwa": "Kino Krasnoludek", "lokalizacja": "Wrocław", "pracownicy": 7}
    ]
    for kino in poczatkowe_kina:
        nowe_kino = Kino(kino["nazwa"], kino["lokalizacja"], kino["pracownicy"])
        kina.append(nowe_kino)
    lista_kin()

# GUI
root = Tk()
root.title("MapBook")
root.geometry("1100x900")

# Login ramkaa
login_frame = Frame(root)
label_nazwa_uzytkownika = Label(login_frame, text="Nazwa użytkownika:")
entry_nazwa_uzytkownika = Entry(login_frame)
label_haslo = Label(login_frame, text="Hasło:")
entry_haslo = Entry(login_frame, show="*")
button_login = Button(login_frame, text="Zaloguj się", command=logowanie)

label_nazwa_uzytkownika.grid(row=5, column=5, sticky=W)
entry_nazwa_uzytkownika.grid(row=5, column=6)
label_haslo.grid(row=6, column=5, sticky=W)
entry_haslo.grid(row=6, column=6)
button_login.grid(row=7, column=5, columnspan=2)

login_frame.grid(row=5, column=5, padx=400, pady=100)

#Główna ramkkaa
main_frame = Frame(root)
main_frame.grid_forget()

# ramka do organizowania struktury
ramka_lista_kin = Frame(main_frame)
ramka_formularz = Frame(main_frame)
ramka_szczegoly_kina = Frame(main_frame)

ramka_lista_kin.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_kina.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

# lista kin
label_lista_kin = Label(ramka_lista_kin, text="Lista kin: ")
listbox_lista_kin = Listbox(ramka_lista_kin, width=50)
button_pokaz_szczegoly = Button(ramka_lista_kin, text="Pokaż szczegóły", command=pokaz_szczegoly_kina)
button_usun_kino = Button(ramka_lista_kin, text="Usuń kino", command=usun_kino)
button_edytuj_kino = Button(ramka_lista_kin, text="Edytuj kino", command=edytuj_kino)

label_lista_kin.grid(row=0, column=0, columnspan=3)
listbox_lista_kin.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_kino.grid(row=2, column=1)
button_edytuj_kino.grid(row=2, column=2)

# formularz
label_formularz = Label(ramka_formularz, text="Formularz")
label_nazwa = Label(ramka_formularz, text="Nazwa kina: ")
label_lokalizacja = Label(ramka_formularz, text="Lokalizacja kina: ")
label_pracownicy = Label(ramka_formularz, text="Liczba pracowników: ")

entry_nazwa = Entry(ramka_formularz)
entry_lokalizacja = Entry(ramka_formularz)
entry_pracownicy = Entry(ramka_formularz)

label_formularz.grid(row=0, column=0, columnspan=2)
label_nazwa.grid(row=1, column=0, sticky=W)
label_lokalizacja.grid(row=2, column=0, sticky=W)
label_pracownicy.grid(row=3, column=0, sticky=W)

entry_nazwa.grid(row=1, column=1)
entry_lokalizacja.grid(row=2, column=1)
entry_pracownicy.grid(row=3, column=1)

button_dodaj_kino = Button(ramka_formularz, text="Dodaj kino", command=dodaj_kino)
button_dodaj_kino.grid(row=4, column=1, columnspan=2)

# szczegóły kin
label_szczegoly_kina = Label(ramka_szczegoly_kina, text="Szczegóły kina: ")
label_nazwa_szczegoly_kina = Label(ramka_szczegoly_kina, text="Nazwa: ")
label_lokalizacja_szczegoly_kina = Label(ramka_szczegoly_kina, text="Lokalizacja: ")
label_wspolrzedne_szczegoly_kina = Label(ramka_szczegoly_kina, text="Współrzędne: ")
label_pracownicy_szczegoly_kina = Label(ramka_szczegoly_kina, text="Liczba pracowników: ")

label_nazwa_szczegoly_kina_wartosc = Label(ramka_szczegoly_kina, text="...", width=30)
label_lokalizacja_szczegoly_kina_wartosc = Label(ramka_szczegoly_kina, text="...", width=20)
label_wspolrzedne_szczegoly_kina_wartosc = Label(ramka_szczegoly_kina, text="...", width=20)
label_pracownicy_szczegoly_kina_wartosc = Label(ramka_szczegoly_kina, text="...", width=20)

label_szczegoly_kina.grid(row=0, column=0, sticky=W)
label_nazwa_szczegoly_kina.grid(row=1, column=0, sticky=W)
label_nazwa_szczegoly_kina_wartosc.grid(row=1, column=1)
label_lokalizacja_szczegoly_kina.grid(row=1, column=2)
label_lokalizacja_szczegoly_kina_wartosc.grid(row=1, column=3)
label_wspolrzedne_szczegoly_kina.grid(row=1, column=4)
label_wspolrzedne_szczegoly_kina_wartosc.grid(row=1, column=5)
label_pracownicy_szczegoly_kina.grid(row=1, column=6)
label_pracownicy_szczegoly_kina_wartosc.grid(row=1, column=7)

map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_kina, width=900, height=500)
map_widget.set_position(52.2, 21.0)
map_widget.set_zoom(8)

map_widget.grid(row=2, column=0, columnspan=8)

root.mainloop()
