from sys import maxsize

INFINITY = maxsize


class Ponasanje:
    def __init__(self):
        self.moguci_smerovi = ["GL", "GD", "DL", "DD"]

    def moguci_potezi_za_igru(self, tabla, igrac):
        moguci_potezi = self.proveri_validnost_poteza(tabla, igrac)

        # proverava da li igrac moze odigrati neki potez
        # ako ne moze, onda se njegov potez preskace
        postoji_potez = False
        for polje, potezi in moguci_potezi.items():
            if len(potezi) > 0:
                postoji_potez = True
                break

        if not postoji_potez:
            return None

        return moguci_potezi

    def proveri_validnost_poteza(self, tabla, igrac):
        redovi = [chr(x + 65) for x in range(tabla.velicina_table)]
        kolone = [y + 1 for y in range(tabla.velicina_table)]

        moguci_potezi = {(red, kolona): [] for red in redovi for kolona in kolone if
                         (ord(red) % 2 == 1 and kolone.index(kolona) % 2 == 0) or
                         (ord(red) % 2 == 0 and kolone.index(kolona) % 2 == 1)}

        for red in tabla.tabla.keys():
            for kolona in tabla.tabla[red].keys():
                if len(tabla.tabla[red][kolona].queue) == 0:
                    continue

                for pozicija in range(7):
                    if len(tabla.tabla[red][kolona].queue) <= pozicija:
                        break

                    unos = [red, kolona, pozicija]
                    temp = self.svi_validni_potezi(tabla, unos, igrac)
                    moguci_potezi[(red, kolona)] += temp[(red, kolona)]

        #print(moguci_potezi)
        return moguci_potezi

        #uneti_potez = moguci_potezi[unos[3]]
        #if uneti_potez is None:
        #    return False
        #if not self.validan_broj_figura(tabla, unos, uneti_potez):
        #    return False

    def svi_validni_potezi(self, tabla, unos, igrac): # unos = [red, kolona, pozicija]
        svi_potezi = [
            [unos[0], unos[1], unos[2], "GL"],  # GL
            [unos[0], unos[1], unos[2], "GD"],  # GD
            [unos[0], unos[1], unos[2], "DL"],  # DL
            [unos[0], unos[1], unos[2], "DD"]   # DD
        ]

        sva_odredista = [
            (chr(ord(unos[0]) - 1), unos[1] - 1),  # GL
            (chr(ord(unos[0]) - 1), unos[1] + 1),  # GD
            (chr(ord(unos[0]) + 1), unos[1] - 1),  # DL
            (chr(ord(unos[0]) + 1), unos[1] + 1)   # DD
        ]

        # proveravamo da li su susedna polja prezna
        prazna_polja = [self.prazno_polje(tabla, x) for x in sva_odredista]
        #print(prazna_polja)

        sva_polja_prazna = True
        for x in prazna_polja:
            if x is None:
                continue
            if x is False:
                sva_polja_prazna = False
                break

        if not sva_polja_prazna:
            #print("Postoji susedno polje koje nije prazno")
            potez_odrediste = [(potez, odrediste) for potez, odrediste, prazno in
                               zip(svi_potezi, sva_odredista, prazna_polja) if prazno is False]
            validni_potezi = {(unos[0], unos[1]): [potez for potez in potez_odrediste
                                                   if self.validan_potez(tabla, potez)]}

            validni_potezi_sa_pozicijom = {(unos[0], unos[1]): [potez for potez in validni_potezi[(unos[0], unos[1])] if
                                                                self.validan_broj_figura(tabla, potez[0], potez[1],
                                                                                         igrac)]}
            #print(validni_potezi)
            #print(validni_potezi_sa_pozicijom)
            return validni_potezi_sa_pozicijom

        else:
            #print("Sva susedna polja su prazna!")
            potez_odrediste = [(potez, odrediste) for potez, odrediste, prazno in
                               zip(svi_potezi, sva_odredista, prazna_polja)
                               if prazno is True and potez[2] == 0 and
                               tabla.tabla[potez[0]][potez[1]].queue[0] == igrac.znak]
            startni_cvor = (unos[0], unos[1])
            putanje_do_ciljnog_cvora = [self.pronadji_najblizi_ciljni_cvor(tabla, startni_cvor, put)
                                        for put in sva_odredista if self.validno_polje(tabla, put)]
            # x = (path, node, g[node]) - putanja, ciljni cvor i heuristika
            min_putanja = min(putanje_do_ciljnog_cvora, key=lambda x: x[2] if x is not None else INFINITY)
            najkrace_putanje_do_ciljnog_cvora = [x[0] for x in putanje_do_ciljnog_cvora
                                                 if x is not None and x[2] == min_putanja[2]]
            validni_potezi = {(unos[0], unos[1]): [potez for potez in potez_odrediste
                                                   if najkrace_putanje_do_ciljnog_cvora.__contains__(potez[1])]}

            #print(validni_potezi)
            return validni_potezi

        #return {(unos[0], unos[1]): [polje for polje in sva_polja if self.validan_potez(tabla, polje)]}
        #return [polje for polje in sva_polja if self.validan_potez(tabla, polje)]
        #return {smer: polje if self.validan_potez(tabla, polje) else None
                #for smer, polje in zip(self.moguci_smerovi, sva_polja)}

    def validan_potez(self, tabla, unos):
        dest = unos[1]
        return self.validno_polje(tabla, dest)

    def validno_polje(self, tabla, polje):
        if polje[0] < 'A' or polje[0] > chr(65 + tabla.velicina_table - 1):
            return False
        if polje[1] < 1 or polje[1] > tabla.velicina_table:
            return False

        return True

    def prazno_polje(self, tabla, dest):
        if self.validno_polje(tabla, dest):
            polje = tabla.tabla[dest[0]][dest[1]].queue
            return len(polje) == 0
        else:
            return None

    def validan_broj_figura(self, tabla, unos, dest, igrac):
        src = (unos[0], unos[1])
        stek_src = tabla.tabla[src[0]][src[1]].queue
        stek_dest = tabla.tabla[dest[0]][dest[1]].queue

        #print(f"Izabrani stek: {(src[0], src[1])} - {stek_src}")
        #print(f"Odredisni stek: {(dest[0], dest[1])} - {stek_dest}")

        if stek_src[unos[2]] != igrac.znak:
            #print("Figura na toj poziciji ne pripada igracu na potezu")
            return False
        if len(stek_dest) <= unos[2]:
            #print("Figura koja se pomera na susedno polje mora se na steku "
            #      "naci na visini koja je veca od "
            #      "trenutne visine na steku na trenutnom polju")
            return False
        if len(stek_src) - unos[2] + len(stek_dest) > 8:
            #print("Ukupan broj figura na odredisnom steku ne sme biti veci od 8")
            return False

        return True

    def get_destination(self, tabla, unos):
        sva_odredista = [
            (chr(ord(unos[0]) - 1), unos[1] - 1),  # GL
            (chr(ord(unos[0]) - 1), unos[1] + 1),  # GD
            (chr(ord(unos[0]) + 1), unos[1] - 1),  # DL
            (chr(ord(unos[0]) + 1), unos[1] + 1)   # DD
        ]

        return list(x for x in sva_odredista if self.validno_polje(tabla, x))

    def pronadji_najblizi_ciljni_cvor(self, tabla, start, path):
        found_end = False
        open_set = set()
        closed_set = set()
        g = {} # heuristika (duzina puta od pocetka do cilja)
        prev_nodes = {}
        g[start] = 0 # udaljenost od pocetka je 0
        g[path] = 1 # udaljenost od pocetka je 1 (susedno polje)
        prev_nodes[start] = None
        prev_nodes[path] = start
        closed_set.add(start)
        open_set.add(path)

        while len(open_set) > 0 and (not found_end):
            node = None
            for next_node in open_set:
                if node is None or g[next_node] < g[node]:
                    node = next_node

            if not self.prazno_polje(tabla, node):
                return path, node, g[node]

            destinations = self.get_destination(tabla, node)
            for destination in destinations:
                if destination not in closed_set:
                    if destination not in open_set:
                        open_set.add(destination)
                        prev_nodes[destination] = node
                        g[destination] = g[node] + 1
                    else:
                        if g[destination] > g[node] + 1:
                            g[destination] = g[node] + 1
                            prev_nodes[destination] = node
                            if destination in closed_set:
                                closed_set.remove(destination)
                                open_set.add(destination)

            open_set.remove(node)
            closed_set.add(node)

        return None
