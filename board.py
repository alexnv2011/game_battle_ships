from ships import Ship, Dot
import random

symbolFree = 'O'
symbolShip = '■'
symbolMis = 'T'
symbolHit = 'X'
symbolContour = '-'
directions = ('vertical', 'horizontal')
SHIPS_DEF = {'3': 1, '2': 2, '1': 3}    # Количество палуб и кораблей



class Board:
    def __init__(self, owner):
        self.owner = owner  # Имя Игрока
        self.hidden = False # Скрыть живые корабли
        self.ships = []     # Корабли
        self.shots = []     # Выстрелы
        self.hits = []      # Попадания
        self.contours = []   # Точки контуров

    def add_ship(self, ship):
        self.ships.append(ship)

        for contour in ship.contours:
            self.contours.append(contour)   # Добавляем в список контуров контур нового корабля

    def ship_in_comtour(self, ship):    # Корабль попадает в контуры всех кораблей доски True / False
        for dot in ship.dots:
            if dot in self.contours:
                return True
        return False

    @property
    def exist_alive_ship(self):    # Есть ли еще живой корабль
        for ship in self.ships:
            if ship.alive:
                return True
        return False

    @property
    def exist_step(self):     # Есть ли еще шаг
        return len(self.shots) < 6 * 6


    def shot(self, dot):    # Выстрел - попал True / False
        self.shots.append(dot)  # заносим в список выстрелов
        for ship in self.ships:
            if ship.hit(dot):
                self.hits.append(dot)   # заносим в список попаданий
                return True
        return False

    def draw(self):     # Отрисовка доски
        print('\nДОСКА ', self.owner)
        s_title = ' '
        for i in range(6):
            s_title += '   ' + str(i + 1)
        print(s_title)

        for j in range(6):
            s_field = str(j + 1)

            for i in range(6):
                dot = Dot(j, i)

                symb = symbolFree

                #for ship in self.ships:     # Показать контур кораблей
                 #   if dot in ship.contours:
                  #      symb = symbolContour

                if not self.hidden:     # Показать корабли
                    for ship in self.ships:
                        if dot in ship.dots:
                            symb = symbolShip

                if dot in self.shots:
                    if dot in self.hits:
                        symb = symbolHit
                    else:
                        symb = symbolMis


                s_field += '   ' + symb
            print(s_field)
        print()




class Player:   # класс ИГРОК
    last_hit = None

    def __init__(self, board_own, board_enemy, name):
        self.board_own = board_own
        self.board_enemy = board_enemy
        self.name = name
        self.show_warnings = True

    def move(self):     # ход в игре
        print('Ходит : ', self.name)
        while self.board_enemy.exist_step:
            move_dot = self.ask()
            new_move = True
            for shot in self.board_enemy.shots:
                if (shot.x == move_dot.x) and (shot.y == move_dot.y):
                    new_move = False
                    break
            if new_move:
                break
            else:
                if self.show_warnings:
                    print(f'Такой ход ({move_dot.y + 1} {move_dot.x + 1}) уже был!')
        self.board_enemy.shot(move_dot)

    def ask(self):      # запрос хода - реализуется у потомков
        pass

    def show_last_hit(self):    # отображение последнего хода
        print( f'Ходит {self.name}: {self.last_hit}')


class User(Player):     # класс Пользователь
    def ask(self):
        while True:
            xy_str = input('Введите координаты выстрела (y x) ').split()
            if not (len(xy_str) == 2):
                print('Введите 2 числа через пробел!')
            else:
                try:
                    x = int(xy_str[0])
                    y = int(xy_str[1])
                    dot = Dot(x - 1, y - 1) # Надо уменьшить числа от пользователя
                    self.last_hit = dot
                except ValueError:
                    print('Введите корректные числа 1..6!')
                else:
                    return self.last_hit



class AI(Player):
    def ask(self):
        xr = random.randint(0, 5)
        yr = random.randint(0, 5)
        self.last_hit = Dot(xr, yr)
        return self.last_hit



class Game:
    userName = None

    def __init__(self):
        self.greeting()
        self.boardUser = Board(self.userName)
        self.boardAI = Board('ПК')
        self.boardAI.hidden = True
        self.user = User(self.boardUser, self.boardAI, self.userName)
        self.ai = AI(self.boardAI, self.boardUser, 'ПК')
        self.ai.show_warnings = False

    def random_ships(self, board):
        for i in range(2, -1, -1):  # i + 1 - длина корабля
            for current in range(SHIPS_DEF.get(str(i + 1))):    # current - номер корабля с длиной i+1
                while True:     # цикл для добавления 1 корабля
                    try:
                        xtmp = random.randint(0, 5)
                        ytmp = random.randint(0, 5)
                        dottmp = Dot(xtmp, ytmp)
                        dir = random.randint(0, 1)
                        dir_str = directions[dir]
                        shiptmp = Ship(dottmp, i + 1, dir_str)
                        if board.ship_in_comtour(shiptmp):
                            raise ValueError("Ship touch contour")
                    except:
                        pass
                    else:
                        board.add_ship(shiptmp)
                        break


    def greeting (self):
        print('Приветствую в игре "Морской бой"\n')
        self.userName = input('Введите Ваше имя: ')

    def loop (self):
        step_AI = bool(random.randint(0, 1))

        while True:
            if step_AI:     # Ходит PC
                if self.ai.board_enemy.exist_step and self.ai.board_enemy.exist_alive_ship:
                   self.ai.move()
                   self.ai.board_enemy.draw()
            else:       # Ходит человек
                if self.user.board_enemy.exist_step and self.user.board_enemy.exist_alive_ship:
                    self.user.move()
                    self.user.board_enemy.draw()

            step_AI = not step_AI

            if not self.user.board_enemy.exist_alive_ship:
                print(f'ПОБЕДИЛ {self.user.name}! ПОЗДРАВЛЯЕМ!')
                break

            if not self.ai.board_enemy.exist_alive_ship:
                print(f'ПОБЕДИЛ {self.ai.name}!')
                break

            if step_AI and (not self.user.board_enemy.exist_step) \
                    or (not step_AI and (not self.ai.board_enemy.exist_step)):
                print('Шаги закончились!')
                break




    def start (self):
        self.random_ships(self.boardAI)
        self.random_ships(self.boardUser)

        self.loop()
