from sys import maxsize
from Tabla import Tabla
from Ponasanje import Ponasanje
from queue import LifoQueue

POSITIVE_INFINITY = maxsize
NEGATIVE_INFINITY = -maxsize


class MinMaxAlphaBeta:
    def __init__(self, igrac_X, igrac_O):
        self.ponasanje = Ponasanje()
        self.igrac_max = igrac_X if igrac_X.ai else igrac_O
        self.igrac_min = igrac_O if igrac_X.ai else igrac_X
        self.igrac_na_potezu = self.igrac_max

    def kopiraj_tablu(self, tabla, n):
        nova_tabla = dict()

        for i in range(n):
            nova_tabla[chr(i + 65)] = dict()
            for j in range(n):
                if j % 2 == i % 2:
                    nova_tabla[chr(i + 65)][j + 1] = LifoQueue(8)
                    lista = tabla[chr(i + 65)][j + 1].queue
                    for x in lista:
                        nova_tabla[chr(i + 65)][j + 1].put(x)

        return nova_tabla

    def promeni_igraca_na_potezu(self):
        if self.igrac_na_potezu == self.igrac_max:
            self.igrac_na_potezu = self.igrac_min
        else:
            self.igrac_na_potezu = self.igrac_max

    def minimax(self, stanje, dubina, moj_potez, alpha=(None, NEGATIVE_INFINITY), beta=(None, POSITIVE_INFINITY)):
        #self.igrac_na_potezu = self.igrac_max
        self.promeni_igraca_na_potezu()
        if moj_potez:
            return self.max_value(stanje, dubina, alpha, beta)
        else:
            return self.min_value(stanje, dubina, alpha, beta)

    def nova_stanja(self, stanje): # tabla, moguci_potezi
        #stablo = {} # placeholder funkcija
        #return stablo[stanje] if stanje in stablo else None

        pocetna_tabla = self.kopiraj_tablu(stanje[0].tabla, stanje[0].velicina_table)

        tabla = Tabla(self.kopiraj_tablu(pocetna_tabla, stanje[0].velicina_table),
                      stanje[0].velicina_table,
                      stanje[0].vrh_steka)
        moguci_potezi = stanje[1]
        #moguci_potezi = None

        if moguci_potezi is not None:
            stablo = {tuple(potez[0]): [] for vrednosti in moguci_potezi.values() for potez in vrednosti if potez}

            for potezi in moguci_potezi.values():
                for potez in potezi:
                    key = tuple(potez[0])
                    src = (key[0], key[1])
                    dest = potez[1]
                    pos = key[2]

                    tabla.azuriraj_tablu(src, dest, pos)

                    self.promeni_igraca_na_potezu()
                    novi_moguci_potezi = self.ponasanje.moguci_potezi_za_igru(tabla, self.igrac_na_potezu)
                    self.promeni_igraca_na_potezu()

                    nova_tabla = Tabla(self.kopiraj_tablu(tabla.tabla, tabla.velicina_table),
                                       tabla.velicina_table,
                                       tabla.vrh_steka)
                    temp = (nova_tabla, novi_moguci_potezi)
                    stablo[key] += temp

                    tabla = Tabla(self.kopiraj_tablu(pocetna_tabla, stanje[0].velicina_table),
                                  stanje[0].velicina_table,
                                  stanje[0].vrh_steka)

            return stablo
        else:
            return None

    def proceni_stanje(self, stanje):
        #procena = {} # placeholder funkcija
        #return procena[stanje] if stanje in procena else 0

        redovi = [chr(x + 65) for x in range(stanje[0].velicina_table)]
        kolone = [y + 1 for y in range(stanje[0].velicina_table)]

        sva_polja = [(red, kolona) for red in redovi for kolona in kolone if
                     (ord(red) % 2 == 1 and kolone.index(kolona) % 2 == 0) or
                     (ord(red) % 2 == 0 and kolone.index(kolona) % 2 == 1)]

        tabla = stanje[0].tabla

        rezultat = 0
        if stanje[0].vrh_steka is not None:
            if stanje[0].vrh_steka == self.igrac_na_potezu.znak:
                rezultat += 8
            else:
                rezultat -= 8

        for vrsta, kolona in sva_polja:
            stek = tabla[vrsta][kolona].queue
            broj_figura = len(stek)
            if broj_figura > 0:
                if stek[broj_figura - 1] == self.igrac_na_potezu.znak:
                    rezultat += broj_figura
                else:
                    rezultat -= broj_figura

        #print(f"Procenjeni rezultat: {rezultat}")
        #stanje[0].crtaj_tablu()
        return rezultat

    def max_value(self, stanje, dubina, alpha, beta, potez=None):
        self.promeni_igraca_na_potezu()
        #print(f"max_value - trenutni potez igraca {self.igrac_na_potezu.znak}, dubina={dubina}")

        lista_novih_stanja = self.nova_stanja(stanje)
        #self.promeni_igraca_na_potezu()

        if dubina == 0 or lista_novih_stanja is None:
            #print(f"Potez za koji se procenjuje stanje: {potez}")

            self.promeni_igraca_na_potezu()
            heuristika = self.proceni_stanje(stanje)

            #print(f"rezultat={heuristika}, alpha={alpha[1]}, beta={beta[1]}")
            #self.promeni_igraca_na_potezu()
            return potez, heuristika
        else:
            for novi_potez in lista_novih_stanja.keys():
                #print(f"Potez {self.igrac_na_potezu.znak} koji se obradjuje: {list(novi_potez)}")
                novo_stanje = tuple(lista_novih_stanja[novi_potez])

                alpha = max(alpha,
                            self.min_value(novo_stanje, dubina - 1, alpha, beta, list(novi_potez)
                            if potez is None else potez),
                            key=lambda x: x[1])
                #print(f"alpha={alpha}, beta={beta}")
                if alpha[1] >= beta[1]:
                    #print("alpha >= beta")
                    self.promeni_igraca_na_potezu()
                    return beta

        self.promeni_igraca_na_potezu()
        return alpha

    def min_value(self, stanje, dubina, alpha, beta, potez=None):
        self.promeni_igraca_na_potezu()
        #print(f"min_value - trenutni potez igraca {self.igrac_na_potezu.znak}, dubina={dubina}")

        lista_novih_stanja = self.nova_stanja(stanje)
        #self.promeni_igraca_na_potezu()

        if dubina == 0 or lista_novih_stanja is None:
            #print(f"Potez za koji se procenjuje stanje: {potez}")

            self.promeni_igraca_na_potezu()
            heuristika = self.proceni_stanje(stanje)

            #print(f"rezultat={heuristika}, alpha={alpha[1]}, beta={beta[1]}")
            #self.promeni_igraca_na_potezu()
            return potez, heuristika
        else:
            for novi_potez in lista_novih_stanja.keys():
                #print(f"Potez {self.igrac_na_potezu.znak} koji se obradjuje: {list(novi_potez)}")
                novo_stanje = tuple(lista_novih_stanja[novi_potez])

                beta = min(beta,
                           self.max_value(novo_stanje, dubina - 1, alpha, beta, list(novi_potez)
                           if potez is None else potez),
                           key=lambda x: x[1])
                #print(f"alpha={alpha}, beta={beta}")
                if beta[1] <= alpha[1]:
                    #print("beta <= alpha")
                    self.promeni_igraca_na_potezu()
                    return alpha

        self.promeni_igraca_na_potezu()
        return beta
