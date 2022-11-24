from random import randint
import time

# Внутренняя логика
# 1 класс точек -
#       метод сравнения точек
#       метод вывода точек ( __eq__ , __repr__)
# 2 классы исключений -
#       общий класс
#       выстрел за доску
#       выстрел в ту же клетку
#       размещение кораблей
# 3 класс корабля -
#       метод размера и ориентации
#       метод выстрела
# 4 класс игровое поле -
#       счетчик убитых кораблей
#       состояние клеток
#       список кораблей
#       метод пределов доски
#       контур корабля
#       размещение корабля
#       метод выстрела
#       метод начала игры
#
# Внешняя логика
# 1 класс игрока -
#       доска противника
#       метод ask
#       метод выстрел
# 2 класс AI -
#       генератор точки
# 3 класс игрок -
#       запрос координаты
# 4 класс игры -
#       конструктор поля
#       два игрока (AI, User)
#       генерация кораблей на доске
#       генерация доски
#       стартовый интерфейс
#       игровой цикл
#       метод старт

# Вывод досок в одну строку
# Выбор расположения досок
# AI не должен стрелять в использованные клетки
# AI добивает корабли
# Выбор размера игрового поля
# Задержка по времени для AI


# Основные исключения
class BoardException(Exception):
    pass

class OutBoardException(BoardException):
    def __str__(self):
        return 'Выстрел за периметр'

class CellUsedException(BoardException):
    def __str__(self):
        return 'Ячейка уже использовалась'

class PlaceException(BoardException):
    pass


# Сравнение точек по координатам
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return f'({self.x}, {self.y})'


# конструктор корабля (нос (начало), длина, ориентация), жизнь - длина.
# Возвращаем список точек. Свойство корабля. Метод попадания по кораблю (сравнение точек).
class Ship:
    def __init__(self, nos, orient, ln):
        self.nos = nos
        self.orient = orient
        self.ln = ln
        self.live = ln


    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ln):
            coor_x = self.nos.x
            coor_y = self.nos.y
            if self.orient == 0:
                coor_x += i

            if self.orient == 1:
                coor_y += i

            ship_dots.append(Dot(coor_x, coor_y))

        return ship_dots


    def shooten(self, shot):
        return shot in self.dots


# Конструктор игрового поля - размер по умолчанию, видимость. Счетчик попаданий.
# Список занятых точек, список с расположенными кораблямми. Возращается переменнная
# со сторокой из клеток (метод __str__).
# Метод проверки диапазона по ориентации.
class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.cnt = 0
        self.field = [['0'] * size for i in range(size)]

        self.busy = []
        self.enemy_busy = []
        self.ships = []


    def __str__(self):
        a = '  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |'
        result = ''
        result += a[:-self.size * -4 + 4]
        for i, row in enumerate(self.field):
            result += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            result = result.replace("■", '0')

        return result


    def out(self, dis):
        return not ((0 <= dis.x < self.size) and (0 <= dis.y < self.size))


    # Контур корабля - список с точками вокруг точки.
    def countour(self, ship, verb=False):
        cntr = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for i in ship.dots:
            for dx, dy in cntr:
                coor = Dot(i.x + dx, i.y + dy)
                if not (self.out(coor)) and coor not in self.busy:
                    if verb:
                        self.field[coor.x][coor.y] = '.'
                    self.busy.append(coor)


    # Добавление корабля на доску - проверка списка занятых точек и точек в диапозоне,
    # если не в диапозоне - вызов исключения.
    def add_ship(self, ship):
        for i in ship.dots:
            if self.out(i) or i in self.busy:
                raise PlaceException()
        for i in ship.dots:
            self.field[i.x][i.y] = "■"
            self.busy.append(i)
        self.ships.append(ship)
        self.countour(ship)


    def shot(self, d):
        if self.out(d):
            raise OutBoardException()

        if d in self.busy:
            raise CellUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.live -= 1
                self.field[d.x][d.y] = 'X'
                if ship.live == 0:
                    self.cnt += 1
                    self.countour(ship, verb = True)
                    print('Убит!')
                    print('-' * 45)
                    return False
                else:
                    print('Ранен!')
                    print('-' * 45)
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        print('-' * 45)
        return False


    def start(self):
        self.busy = []


    def defeat(self):
        return self.cnt == len(self.ships)


# Игрок - две доски. Возвращается повтор хода, если ход неудачный.
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy


    def ask(self):
        raise PlaceException()


    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


# Конструкция AI - рандомный ход (генерация точки)
class AI(Player, Board, Ship):
    def ask(self):
        while True:
            a = Dot(randint(0, 5), randint(0, 5))
            if a in self.board.enemy_busy:
                continue
            self.board.enemy_busy.append(a)
            break

        print(f'AI использовал координаты: {a.y + 1} {a.x + 1}')
        return a


# Конструкция игрока - запрос координат. Проверки: длина, цыфры. Возвращает два int.
class User(Player):
    def ask(self):
        while True:
            enter = input('Введите координаты: ')
            if len(enter) != 2:
                print('Координаты должно быть 2')
                continue
            if not enter.isdigit():
                print('Некорректный ввод')
                continue
            coord = [i for i in enter]
            y, x = int(coord[0]) - 1, int(coord[1]) - 1

            return Dot(x, y)


# Конструктор игры - размер доски. Две доски.
# Генерация досок - список кораблей: 3 2 2 1 1 1 1.
# Счетчик попыток генерации ограниченный. Добавление корабля (4 аргумента).
# Возвращает доску.
# Приветствие. Инструкция.
# Игровой цикл. Счетчик ходов
class Game:
    # Регулируемый размер игрового поля
    def sizer(self):
        while True:
            print('-' * 44)
            print('                МОРСКОЙ БОЙ')
            print('-' * 44)
            print('-- Формат ввода координат: xy (без пробела)')
            print('X - горизонталь')
            print('Y - вертикаль')
            print('-' * 44)
            print('-- Варианты размера игрового поля')
            print('6 x 6 - введите 6')
            print('7 x 7 - введите 7')
            print('8 x 8 - введите 8')
            print('-' * 44)
            a = input('Укажите размер поля: ')
            print('-' * 44)
            if not a.isdigit():
                print('Некорректный ввод')
                continue
            if len(a) > 1:
                print('Введите одну цифру')
                continue
            sett = int(a)
            if sett < 6:
                print('Внимательно ознакомтесь с инструкцией размера поля')
                continue

            return sett


    def __init__(self, size=6):
        self.selec = 0
        self.lng = [3, 2, 2, 1, 1, 1, 1]
        self.size = self.sizer()
        plr = self.rand_board()
        cmp = self.rand_board()
        cmp.hid = True

        self.ai = AI(cmp, plr)
        self.us = User(plr, cmp)


    def build_board(self):
        board = Board(size=self.size)
        tr = 0
        for i in self.lng:
            while True:
                tr += 1
                if tr > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1), i)
                try:
                    board.add_ship(ship)
                    break
                except PlaceException:
                    pass

        board.start()
        return board


    def rand_board(self):
        board = None
        while board is None:
            board = self.build_board()

        return board


    def s(self):
        self.selec = self.select()


    def merge_boards(first, second):
        first_lines = first.split("\n")
        second_lines = second.split("\n")

        result = ""
        for i in range(len(first_lines)):
            result_line = f"{first_lines[i]:28}    {second_lines[i]}\n"
            result += result_line

        return result


    def row_board(self):
        print()
        print("-- Игрок", ' ' * (self.size * 4 - 2), "-- AI")
        user_board = str(self.us.board)
        ai_board = str(self.ai.board)
        print('-' * ((self.size * 4) + (self.size * 4) + 10))
        print(Game.merge_boards(user_board, ai_board))


    def col_board(self):
        print()
        print('-- Игрок')
        print('-' * (4 * self.size + 3))
        print(self.us.board)
        print()
        print('-- AI')
        print('-' * (4 * self.size + 3))
        print(self.ai.board)
        print()


    def select(self):
        sel = 0
        while True:
            print('-- Варианты расположения игровых полей')
            print('1 - горизонтальное')
            print('2 - вертикальное')
            print('-' * 44)
            enter = input('Выбрать вариант: ')
            print('-' * 44)
            if len(enter) > 1:
                print('Введите одну цифру')
                continue
            if not enter.isdigit():
                print('Некорректный ввод')
                continue
            x = int(enter)
            if x != 1 and x != 2:
                print('Введите 1 или 2')
                continue
            if x == 1:
                sel = 1
            elif x == 2:
                sel = 2
            break

        return sel


    def pref(self):
        selection = self.selec
        if selection == 1:
            return self.row_board()
        elif selection == 2:
            return self.col_board()


    def loop(self):
        n = 0
        while True:
            self.pref()

            if n % 2 == 0:
                print('Ход игрока -->')
                print('-' * 44)
                repeat = self.us.move()
            else:
                print('Ход AI -->')
                print('-' * 44)
                time.sleep(randint(1, 3))
                repeat = self.ai.move()
            if repeat:
                n -= 1

            if self.ai.board.defeat():
                self.pref()
                print('-' * 44)
                print('Игрок выиграл')
                break
            if self.us.board.defeat():
                self.pref()
                print('-' * 44)
                print('AI выиграл')
                break
            n += 1

    def start_game(self):
        self.s()
        self.loop()

g = Game()
g.start_game()
