from Tabla import Tabla
from Igrac import Igrac
from Ponasanje import Ponasanje
from MinMaxAlphaBeta import MinMaxAlphaBeta


class Game:
    def __init__(self):
        self.tabla = Tabla()
        self.ponasanje = Ponasanje()
        self.broj_figura = 0
        self.uslov_za_pobedu = 0
        self.igrac_X = None
        self.igrac_O = None
        self.igrac_na_potezu = None
        self.minmax = None

    def unesi_parametre(self):
        while True:
            try:
                n = int(input("Unesi velicinu table: "))
                if self.tabla.kreiraj_tablu(n):
                    self.broj_figura = (n * (n - 2) // 2)
                    br_steka = self.broj_figura // 8
                    self.uslov_za_pobedu = br_steka // 2 + 1
                    break
            except:
                print("Neispravan unos!")
                continue

        return True

    def covek_ili_racunar(self):
        while True:
            izbor = input("Da li zelite igrati protiv racunara? (Y/N): ").upper()
            if izbor == "Y":
                return True
            elif izbor == "N":
                return False
            else:
                print("Neispravan unos!")

    def ko_igra_prvi(self):
        while True:
            izbor = input("Da li zelite da igrate prvi? (Y/N): ").upper()
            if izbor == "Y":
                self.generisi_igrace(
                    Igrac("X", False),
                    Igrac("O", True)
                )
                break
            elif izbor == "N":
                self.generisi_igrace(
                    Igrac("X", True),
                    Igrac("O", False)
                )
                break
            else:
                print("Neispravan unos!")

        return True

    def generisi_igrace(self, igrac_X, igrac_O):
        self.igrac_X = igrac_X
        self.igrac_O = igrac_O
        self.igrac_na_potezu = self.igrac_X

    def unesi_potez(self):
        moguci_potezi = self.ponasanje.moguci_potezi_za_igru(self.tabla, self.igrac_na_potezu)

        if moguci_potezi is None:
            print(f"Preskace se potez igraca {self.igrac_na_potezu.znak} jer nema validnih poteza za unos!")
            return

        while True:
            try:
                red = input(f"Izaberite vrstu (A-{chr(65 + self.tabla.velicina_table - 1)}): ").upper()
                if not self.tabla.tabla.keys().__contains__(red):
                    print("Neispravan unos!")
                    continue

                kolona = int(input(f"Izaberite kolonu (1-{self.tabla.velicina_table}): "))
                if not self.tabla.tabla[red].keys().__contains__(kolona):
                    print("Neispravan unos!")
                    continue

                lista = self.tabla.tabla[red][kolona].queue
                if len(lista) == 0:
                    print("Ne postoje figure na ovom polju!")
                    continue

                pozicija = int(input("Unesite poziciju sa steka (0-7): "))
                if not pozicija < len(lista):
                    print("Figura na toj poziciji ne postoji!")
                    continue
                if lista[pozicija] != self.igrac_na_potezu.znak:
                    print("Ne mozete uzimati tudje figure!")
                    continue

                smer = input("Unesite smer (GL, GD, DL, DD): ").upper()
                if not self.ponasanje.moguci_smerovi.__contains__(smer):
                    print("Neispravan unos!")
                    continue

                potez = [red, kolona, pozicija, smer]
                print(f"Uneti potez igraca {self.igrac_na_potezu.znak}: {potez}")

                src = (red, kolona)
                dest = next((x[1] for x in moguci_potezi[src] if potez == x[0]), None)

                if dest is None:
                    print("Potez nije validan!")
                    continue

                print("Potez je ispravno unet!")
                self.tabla.azuriraj_tablu(src, dest, pozicija)
            except:
                print("Neispravan unos!")
                continue

            break

    def unesi_potez_ai(self):
        moguci_potezi = self.ponasanje.moguci_potezi_za_igru(self.tabla, self.igrac_na_potezu)

        if moguci_potezi is None:
            print(f"Preskace se potez racunara {self.igrac_na_potezu.znak} jer nema validnih poteza za unos!")
            return

        stanje = (self.tabla, moguci_potezi)
        unos = self.minmax.minimax(stanje, 3, self.igrac_na_potezu.ai)

        potez = unos[0]
        print(f"Uneti potez racunara {self.igrac_na_potezu.znak}: {potez}")

        src = (potez[0], potez[1])
        dest = next((x[1] for x in moguci_potezi[src] if potez == x[0]), None)
        if dest is None:
            print("Greska prilikom odredjivanja poteza")
        else:
            self.tabla.azuriraj_tablu(src, dest, potez[2])

    def dodeli_poen(self):
        if self.tabla.vrh_steka == "X":
            print("Igrac X je dobio poen!")
            self.igrac_X.rezultat += 1
        elif self.tabla.vrh_steka == "O":
            print("Igrac O je dobio poen!")
            self.igrac_O.rezultat += 1

        if self.tabla.vrh_steka is not None:
            self.broj_figura -= 8

    def promeni_igraca_na_potezu(self):
        if self.igrac_na_potezu == self.igrac_X:
            self.igrac_na_potezu = self.igrac_O
        else:
            self.igrac_na_potezu = self.igrac_X

    def igraj_igru(self):
        self.minmax = MinMaxAlphaBeta(self.igrac_X, self.igrac_O)

        while not self.kraj_igre():
            self.tabla.crtaj_tablu()
            print(f"Trenutni rezultat: X - {self.igrac_X.rezultat} : {self.igrac_O.rezultat} - O")
            print(f"Trenutno igra {self.igrac_na_potezu.znak} ({"AI" if self.igrac_na_potezu.ai else "Igrac"})")
            if not self.igrac_na_potezu.ai:
                self.unesi_potez()
            else:
                self.unesi_potez_ai()

            self.dodeli_poen()
            self.promeni_igraca_na_potezu()

        if self.igrac_X.rezultat == self.uslov_za_pobedu:
            print("Igrac X je pobednik!")
        elif self.igrac_O.rezultat == self.uslov_za_pobedu:
            print("Igrac O je pobednik!")
        else:
            print("Nereseno")

    def kraj_igre(self):
        return (self.igrac_X.rezultat == self.uslov_za_pobedu or
                self.igrac_O.rezultat == self.uslov_za_pobedu or
                self.broj_figura == 0)


if __name__ == '__main__':
    igra = Game()
    if igra.unesi_parametre():
        if igra.covek_ili_racunar():
            igra.ko_igra_prvi()
        else:
            igra.generisi_igrace(
                Igrac("X", False),
                Igrac("O", False)
            )
        igra.igraj_igru()
