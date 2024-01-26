from queue import LifoQueue


class Tabla:
    def __init__(self, tabla=None, n=0, vs=None):
        if tabla is None:
            tabla = dict()
        self.tabla = tabla
        self.velicina_table = n
        self.vrh_steka = vs # odredjuje nam koji od igraca dobija poen
                            # kada se nakon azuriranja table popuni stek do kraja

    def kreiraj_tablu(self, n):
        # proveravamo da li je velicina table paran broj,
        # da li broj figura na tabli koji se generise deljiv sa 8
        # i da je velicina table izmedju 2 i 16
        if n % 2 != 0 or (n * (n - 2) // 2) % 8 != 0 or n <= 2 or n > 16:
            print("Neispravan unos!")
            return False
        else:
            self.velicina_table = n
            self.generisi_tablu()
            self.postavi_tablu_na_pocetno_stanje()
            #self.postavi_tablu_na_pocetno_stanje_2() #debug funkcija
            return True

    def generisi_tablu(self):
        # vrste su oznacene slovima a kolone brojevima
        for i in range(self.velicina_table):
            self.tabla[chr(i + 65)] = dict()
            for j in range(self.velicina_table):
                if j % 2 == i % 2:
                    self.tabla[chr(i + 65)][j + 1] = LifoQueue(8)

    def postavi_tablu_na_pocetno_stanje(self):
        # vrste se naizmenicno popunjavaju figurama X i O (prva i poslednja vrsta se ne popunjavaju)
        for red in self.tabla.keys():
            if not (red == chr(65) or red == chr(65 + self.velicina_table - 1)):
                for kolona in self.tabla[red].items():
                    kolona[1].put("X" if kolona[0] % 2 == 0 else "O")

    def postavi_tablu_na_pocetno_stanje_2(self):
        for red in self.tabla.keys():
            if red == chr(66) or red == chr(65 + self.velicina_table - 2):
                for kolona in self.tabla[red].items():
                    kolona[1].put("X" if kolona[0] % 2 == 0 else "O")

    def azuriraj_tablu(self, src, dest, pozicija):
        stek_pom = LifoQueue(8)

        stek_src = self.tabla[src[0]][src[1]]
        stek_dest = self.tabla[dest[0]][dest[1]]

        # prebacujemo iz izvorisnog steka u pomocni stek kako bi u odredisnom steku zadrzali redosled figura
        for i in range(len(stek_src.queue) - pozicija):
            pom = stek_src.get()
            stek_pom.put(pom)

        while not stek_pom.empty():
            pom = stek_pom.get()
            stek_dest.put(pom)

        if stek_dest.full():
            self.vrh_steka = stek_dest.get()
            self.tabla[dest[0]][dest[1]] = LifoQueue(8)
        else:
            self.vrh_steka = None

    def crtaj_tablu(self):
        tablica = "   "
        for i in range(self.velicina_table):
            if i < 9:
                tablica += f"  {i + 1}  "
            else:
                tablica += f" {i + 1}  "
        print(tablica)
        for i in range(self.velicina_table):
            tablica = ""
            key1 = chr(i + 65)
            for k in range(3):
                if k == 1:
                    tablica += f" {key1} "
                else:
                    tablica += "   "
                for j in range(self.velicina_table):
                    if (i + j) % 2 == 0:
                        for l in range(3):
                            if l == 0:
                                tablica += " "
                            lista = list(self.tabla[key1][j + 1].queue)
                            index = 3 * k + l
                            tablica += lista[index] if index < len(lista) else "."
                            if l == 2:
                                tablica += " "
                    else:
                        tablica += "     "

                    if j == self.velicina_table - 1 and k != 2:
                        tablica += "\n"
            print(tablica)

    # def crtaj_tablu_old(self):
    #     tablica = "   "
    #     for i in range(self.velicina_table):
    #         if i < 9:
    #             tablica += f"  {i + 1}  "
    #         else:
    #             tablica += f" {i + 1}  "
    #     print(tablica)
    #     for i in range(self.velicina_table):
    #         tablica = ""
    #         for j in range(3):
    #             for k in range(self.velicina_table):
    #                 if k == 0:
    #                     if j == 1:
    #                         tablica += f" {chr(i + 65)} "
    #                     else:
    #                         tablica += "   "
    #                 if (i + k) % 2 == 0:
    #                     tablica += " ... "
    #                 else:
    #                     tablica += "     "
    #             if j != 2:
    #                 tablica += "\n"
    #         print(tablica)

