class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __str__(self):
        return f'x = {self._x}, y = {self._y}'

    @property
    def x(self):
        return self._x

    @x.setter    ## Декоратор сеттер x
    def x(self, value):
        if 0 <= value <= 5:  # от 0 до 5
            self._x = value
        else:
            raise ValueError("X must be between 0 .. 5")
    @property
    def y(self):
        return self._y

    @y.setter    ## Декоратор сеттер y
    def y(self, value):
        if 0 <= value <= 5:  # от 0 до 5
            self._y = value
        else:
            raise ValueError("Y must be between 0 .. 5")


class Deck(Dot):  # Палуба корабля
    live = True
    def __init__(self, x, y, live=True): # помимо координаты точки палуба имеет состояние (Живая - Подбитая)
        super().__init__(x, y)
        self.live = live


class Ship:
    def __init__(self, dot_start, length=1, direction='горизонтальный'):
        self.dotStart = dot_start
        self.length = length
        self.direction = direction
        self.decks = []     # все палубы c состоянием живые или нет True / False
        self.dots = []      # все точки палуб корабля
        self.contours = []  # все точки контура корабля

        # Добавление точек корабля
        for i in range(length):
            if direction.lower() == 'горизонтальный' or direction.lower() == 'horizontal' or direction[0:3].lower() == 'hor' or direction[0:1].lower() == 'h' or direction[0:1].lower() == 'г':
                dot = Dot(dot_start.x, dot_start.y + i)
            else:
                dot = Dot(dot_start.x + i, dot_start.y)
            self.dots.append(dot)
            self.decks.append(True)

            for i in range(dot.x - 1, dot.x + 2):
                for j in range(dot.y - 1, dot.y + 2):
                    if (0 <= i <= 5) and (0 <= j <= 5):
                        dot_contour = Dot(i, j)
                        self.contours.append(dot_contour)    # присвоение точек контура



    @property
    def alive(self):    # True  = корабль живой или нет
        return any(self.decks)

    def __str__(self):
        if self.alive:
            st = 'живой'
        else:
            st = 'убит'
        sdecks = '. Палубы (' + str(self.length) + '): '
        for i in self.dots:
            sdecks += f'{i.x},{i.y},{str(self.decks)};  '
        return 'Корабль ' + st + sdecks

    def hit(self, dot):     # Попадание в палубу. Меняем состояние палубы на False
        for i in range(len(self.decks)):
            if dot == self.dots[i]:
                self.decks[i] = False
                return True
        return False

