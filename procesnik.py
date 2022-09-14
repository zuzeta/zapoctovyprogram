import copy
import os
from playsound import playsound
from random import randint, seed
from queue import Queue

def pytaj_se():
    """uzivatel si voli, ci chce zadat vlastnu tabulku, alebo chce,
    aby mu program vygeneroval nahodnu tabulku pozadovanej velkosti.
    Dalej si moze urcit "obtiaznost" nahodne vygenerovanej
    tabulky - moze tak urobit tym, ze urci, kolko krat sa ma tabulka zamisat"""
    os.system("CLS")
    print(bcolors.OKCYAN + "Vítejte ve hře (n×n - 1)! Po vyplnění pole, prosím, stiskněte ENTER. " + bcolors.ENDC)
    print(bcolors.WARNING + """Napište: "1", jestli si přejete tabulku vygenerovat, "2", jestli chcete zadat vlastní tabulku""" + bcolors.ENDC)
    odpoved = int(input())
    if odpoved == 1:
        mam_vygenerovat_tabulku = True
        print("Zadejte n: ")
        n = int(input())
        print("Kolikrát si přejete kostičky zamíchat?: ")
        shuffle_magnitude = int(input())
    elif odpoved == 2:
        mam_vygenerovat_tabulku = False
        print("Zadejte rozměry vaší tabulky (musí být tvaru n×n): ")
        n = int(input())
        shuffle_magnitude = 0
    else:
        print("nedělej si legraci")
    riadky = n
    stlpce = n
    return mam_vygenerovat_tabulku, shuffle_magnitude, n, riadky, stlpce

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Board:
    """touto clasou bude tvorena tabulka s cislami"""
    def __init__(self, mam_vygenerovat_tabulku, shuffle_magnitude, n, riadky, stlpce):
        self.shuffle_magnitude = shuffle_magnitude
        self.n = n
        self.riadky = riadky
        self.stlpce = stlpce

        """dva krat ulozena tabulka - jedna, s ktorou hybem, a ta, ktora je uz zoradena"""
        """vyriesena tabulka bude rovnaka pre oba pripady. Tabulka, s ktorou hybem, bude nahodne vygenerovana  
        (tak, ze bude riesitelna) pre uzivatelovu volbu "1" a importovana priamo zo vstupu pri volbe "2" """
        if mam_vygenerovat_tabulku == True:
            items = [i + 1 for i in range(self.n * self.n - 1)]
            items.append(0)
            def split(list_a, chunk_size):
                for i in range(0, len(list_a), self.n):
                    yield list_a[i:i + chunk_size]
        elif mam_vygenerovat_tabulku == False:
            print("Zadejte postupně prvky vaší tabulky (vypište n×n-1, mezera bude na konci): ")
            items = list(map(int, input().split()))
            items.append(0)
            def split(items, chunk_size):
                for i in range(0, len(items), self.n):
                   yield items[i:i + chunk_size]
        chunk_size = self.n
        rucne_zadana_tabulka = list(split(items, chunk_size))
        self.tabulka = rucne_zadana_tabulka
        """vytvaram cielovu tabulku - so spravne usporiadanymi cislami"""
        my_list = [i + 1 for i in range(self.n * self.n - 1)]
        my_list.append(0)
        baskets = list(split(my_list, chunk_size))
        self.goal = baskets
        """tu sa odohraje rozlisenie medzi dvoma typmi hybacich tabuliek (podla volby uzivatela)"""
        if mam_vygenerovat_tabulku == True:
            """hybaciu tabulku beriem ako kopiu spravne usporiadanej tabulky"""
            self.board = copy.deepcopy(self.goal)
        elif mam_vygenerovat_tabulku == False:
            """hybaciu tabulku beriem zo kopiu vstupu od uzivatela"""
            self.board = copy.deepcopy(self.tabulka)
        self.prazdne_miesto = [self.riadky - 1, self.stlpce - 1]
        """slovnik obsahujuci druhy krokov, ktore mozeme vykonat s prazdnym miestom"""
        self.moves = {0: self.move_up, 1: self.move_right, 2: self.move_down, 3: self.move_left}

        """kontrolujem riesitelnost tabulky zadanej uzivatelom"""
        def getInvCount(arr):
            arr1 = []
            for y in arr:
                for x in y:
                    arr1.append(x)
            arr = arr1
            inv_count = 0
            for i in range(self.n * self.n - 1):
                for j in range(i + 1, self.n * self.n):
                    if (arr[j] and arr[i] and arr[i] > arr[j]):
                        inv_count += 1
            return inv_count

        def findXPosition(puzzle):
            """funkcia sluziaca na najdenie prazdneho miesta v uzivatelom zadanej tabulke -
                    prazdne miesto bude oznacene nulou"""
            for i in range(self.n - 1, -1, -1):
                for j in range(self.n - 1, -1, -1):
                    if (puzzle[i][j] == 0):
                        return self.n - i

        def isSolvable(puzzle):
            invCount = getInvCount(puzzle)
            """riesitelnost pre neparne n, potom pre parne n"""
            if (self.n & 1):
                return ~(invCount & 1)
            else:
                pos = findXPosition(puzzle)
                if (pos & 1):
                    return ~(invCount & 1)
                else:
                    return invCount & 1
        if isSolvable(rucne_zadana_tabulka) == -1:
            print("Tabulka je řešitelná")
            self.isSolvable = True
        if isSolvable(rucne_zadana_tabulka) == -2:
            print("Tabulka není řešitelná")
            print("pro navrácení do hry stiskněte kláves ENTER")
            self.isSolvable = False

    def __repr__(self):
        """funkcia na reprezentaciu tabulky, vytlaci prvky pekne zarovnane"""
        for i in range(self.riadky):
            for j in range(self.stlpce):
                print('%-2d ' % self.board[i][j], end = " ")
            print()
        return ""

    def refresh(self):
        os.system("CLS")
        print("Přejeme hodně štěstí!")
        print(bcolors.WARNING + "Pro získání nápovědy stiskněte SPACE.\n" + bcolors.ENDC)
        print(self)
        if self.board == self.goal:
            print(bcolors.OKCYAN + "Gratulujeme, vyhráli jste!\n \n \n \n \n \n \n" + bcolors.ENDC)
            playsound(os.path.join(".", "goodresult-82807.mp3"))
            return True
        else:
            return False

    def shuffle(self):
        """vykoná sériu nádodných legálnych krokov, teda tabuľka bude riešiteľná"""
        seed()
        """vygeneruje jeden z krokov ulozenych v slovniku, dany krok potom vykona"""
        for i in range(self.shuffle_magnitude):
            m = randint(0, 3)
            self.moves[m](self.board, self.prazdne_miesto)
        """vykona vsetky kroky potrebne nato, aby sa prazdne miesto urcite dostalo do praveho dolneho rohu"""
        for i in range(self.riadky):
            self.moves[2](self.board, self.prazdne_miesto)
        for i in range(self.stlpce):
            self.moves[1](self.board, self.prazdne_miesto)

    def move(self, board, prazdne_miesto, x, y):
        """obmedzenie pohybu prazdneho miesta"""
        if prazdne_miesto[0] + x < 0 or prazdne_miesto[0] + x > self.n -1 or \
                prazdne_miesto[1] + y < 0 or prazdne_miesto[1] + y > self.n -1 :
            return board, prazdne_miesto
        board[prazdne_miesto[0]][prazdne_miesto[1]], board[prazdne_miesto[0] + x][prazdne_miesto[1] + y] = \
            board[prazdne_miesto[0] + x][prazdne_miesto[1] + y], board[prazdne_miesto[0]][prazdne_miesto[1]]
        prazdne_miesto[0] += x
        prazdne_miesto[1] += y
        return board, prazdne_miesto

    def move_up(self, board, empty_space_loc):
        return self.move(board, empty_space_loc, -1, 0)

    def move_down(self, board, prazdne_miesto):
        return self.move(board, prazdne_miesto, 1, 0)

    def move_right(self, board, prazdne_miesto):
        return self.move(board, prazdne_miesto, 0, 1)

    def move_left(self, board, prazdne_miesto):
        return self.move(board, prazdne_miesto, 0, -1)

    def solve(self):
        """implementovany algoritmus na riesenie hry"""
        """pouzijeme BFB algoritmus """

        def successors(board, prazdne_miesto):
            b_lst = [copy.deepcopy(board), copy.deepcopy(board), copy.deepcopy(board), copy.deepcopy(board)]
            e_loc_lst = [list(prazdne_miesto), list(prazdne_miesto), list(prazdne_miesto), list(prazdne_miesto)]
            b_lst[0], e_loc_lst[0] = self.move_up(b_lst[0], e_loc_lst[0])
            b_lst[1], e_loc_lst[1] = self.move_right(b_lst[1], e_loc_lst[1])
            b_lst[2], e_loc_lst[2] = self.move_down(b_lst[2], e_loc_lst[2])
            b_lst[3], e_loc_lst[3] = self.move_left(b_lst[3], e_loc_lst[3])
            return [[b_lst[0], e_loc_lst[0], 0],[b_lst[1], e_loc_lst[1], 1],
                    [b_lst[2], e_loc_lst[2], 2],[b_lst[3], e_loc_lst[3], 3]]
        searched = []
        fringe = Queue()
        root = self.board
        fringe.put({"board": root, "prazdne_miesto": self.prazdne_miesto, "path": []})
        while True:
            if fringe.empty():
                return []
            node = fringe.get()
            if node["board"] == self.goal:
                return node["path"]
            if node["board"] not in searched:
                searched.append(node["board"])
                for child in successors(node["board"], node["prazdne_miesto"]):
                    if child not in searched:
                        fringe.put({"board": child[0], "prazdne_miesto": child[1],
                                    "path": node["path"] + [child[2]]})
