from tkinter import *
from tkinter import messagebox


zalogowany = False
# Lista pracowników
pracownicy = [
    {"nazwa": "Mędrek Pomarańczowy-Kubraczek", "wspolrzedne": (50.0, 20.0)},
    {"nazwa": "Gburek Skwaszona-Mina", "wspolrzedne": (51.0, 21.0)},
    {"nazwa": "Apsik Zadbany", "wspolrzedne": (52.0, 22.0)},
    {"nazwa": "Wesołek Krzaczaste-Brwi", "wspolrzedne": (53.0, 23.0)},
    {"nazwa": "Śpioszek Zielona-Czapka", "wspolrzedne": (54.0, 24.0)},
    {"nazwa": "Gapcio Fioletowa-Czapka", "wspolrzedne": (55.0, 25.0)},
    {"nazwa": "Nieśmiałek Wstydzioch", "wspolrzedne": (56.0, 26.0)}
]

def logowanie():
    global zalogowany
    nazwa_uzytkownika = entry_nazwa_uzytkownika.get()
    haslo = entry_haslo.get()
    if nazwa_uzytkownika == "admin" and haslo == "admin":
        zalogowany = True
        login_frame.grid_forget()
        main_frame.grid(row=0, column=0, padx=50)
        lista_pracownikow()
    else:
        messagebox.showerror("Błąd logowania", "Niepoprawna nazwa użytkownika lub hasło")

# Funkcje CRUD
def lista_pracownikow():
    listbox_lista_pracownikow.delete(0, END)
    for idx, pracownik in enumerate(pracownicy):
        listbox_lista_pracownikow.insert(idx, f"{pracownik['nazwa']} ({pracownik['wspolrzedne'][0]}, {pracownik['wspolrzedne'][1]})")

def dodaj_pracownika():
    nazwa = entry_nazwa.get()
    wsp_x = entry_wsp_x.get()
    wsp_y = entry_wsp_y.get()
    wspolrzedne = (float(wsp_x), float(wsp_y))
    nowy_pracownik = {"nazwa": nazwa, "wspolrzedne": wspolrzedne}
    pracownicy.append(nowy_pracownik)
    lista_pracownikow()
    entry_nazwa.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_nazwa.focus()

def usun_pracownika():
    listbox_lista_pracownikow.curselection()
    i = listbox_lista_pracownikow.curselection()[0]
    pracownicy.pop(i)
    lista_pracownikow()

def pokaz_szczegoly_pracownika():
    listbox_lista_pracownikow.curselection()
    i = listbox_lista_pracownikow.curselection()[0]
    pracownik = pracownicy[i]
    label_nazwa_szczegoly.config(text=pracownik['nazwa'])
    label_wspolrzedne_szczegoly.config(text=f"{pracownik['wspolrzedne'][0]}, {pracownik['wspolrzedne'][1]}")


def edytuj_pracownika():
    listbox_lista_pracownikow.curselection()
    i = listbox_lista_pracownikow.curselection()[0]
    entry_nazwa.insert(0, pracownicy[i]['nazwa'])
    entry_wsp_x.insert(0, pracownicy[i]['wspolrzedne'][0])
    entry_wsp_y.insert(0, pracownicy[i]['wspolrzedne'][1])
    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: aktualizuj_pracownika(i))


def aktualizuj_pracownika(i):
    pracownicy[i]['nazwa'] = entry_nazwa.get()
    pracownicy[i]['wspolrzedne'] = (float(entry_wsp_x.get()), float(entry_wsp_y.get()))
    lista_pracownikow()
    button_dodaj_pracownika.config(text="Dodaj pracownika", command=dodaj_pracownika)
    entry_nazwa.delete(0, END)
    entry_wsp_x.delete(0, END)
    entry_wsp_y.delete(0, END)
    entry_nazwa.focus()


# GUI
root = Tk()
root.title("MapBook")
root.geometry("800x600")

# Login frame
login_frame = Frame(root)
label_nazwa_uzytkownika = Label(login_frame, text="Nazwa użytkownika:")
entry_nazwa_uzytkownika = Entry(login_frame)
label_haslo = Label(login_frame, text="Hasło:")
entry_haslo = Entry(login_frame, show="*")
button_login = Button(login_frame, text="Zaloguj się", command=logowanie)

label_nazwa_uzytkownika.grid(row=0, column=0, sticky=W)
entry_nazwa_uzytkownika.grid(row=0, column=1)
label_haslo.grid(row=1, column=0, sticky=W)
entry_haslo.grid(row=1, column=1)
button_login.grid(row=2, column=0, columnspan=2)

login_frame.grid(row=0, column=0, padx=200, pady=100)

# Main frame
main_frame = Frame(root)
main_frame.grid_forget()

# Lista pracowników
label_lista_pracownikow = Label(main_frame, text="Lista pracowników Kina Krasnoludek:")
label_lista_pracownikow.grid(row=0, column=0, columnspan=3)
listbox_lista_pracownikow = Listbox(main_frame, width=50)
listbox_lista_pracownikow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly = Button(main_frame, text="Pokaż szczegóły", command=pokaz_szczegoly_pracownika)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_pracownika = Button(main_frame, text="Usuń pracownika", command=usun_pracownika)
button_usun_pracownika.grid(row=2, column=1)
button_edytuj_pracownika = Button(main_frame, text="Edytuj pracownika", command=edytuj_pracownika)
button_edytuj_pracownika.grid(row=2, column=2)

# Formularz
label_formularz = Label(main_frame, text="Formularz")
label_formularz.grid(row=3, column=0, columnspan=2)
label_nazwa = Label(main_frame, text="Nazwa pracownika:")
label_nazwa.grid(row=4, column=0, sticky=W)
label_wsp_x = Label(main_frame, text="Współrzędne X:")
label_wsp_x.grid(row=5, column=0, sticky=W)
label_wsp_y = Label(main_frame, text="Współrzędne Y:")
label_wsp_y.grid(row=6, column=0, sticky=W)

entry_nazwa = Entry(main_frame)
entry_nazwa.grid(row=4, column=1)
entry_wsp_x = Entry(main_frame)
entry_wsp_x.grid(row=5, column=1)
entry_wsp_y = Entry(main_frame)
entry_wsp_y.grid(row=6, column=1)

button_dodaj_pracownika = Button(main_frame, text="Dodaj pracownika", command=dodaj_pracownika)
button_dodaj_pracownika.grid(row=7, column=0, columnspan=2)

# Szczegóły pracownika
label_szczegoly = Label(main_frame, text="Szczegóły pracownika:")
label_szczegoly.grid(row=8, column=0, sticky=W)
label_nazwa_szczegoly = Label(main_frame, text="Nazwa: ...")
label_nazwa_szczegoly.grid(row=9, column=0, sticky=W)
label_wspolrzedne_szczegoly = Label(main_frame, text="Współrzędne: ...")
label_wspolrzedne_szczegoly.grid(row=10, column=0, sticky=W)

#wolanie funkcji
lista_pracownikow()

root.mainloop()
