def welcome():
    print("-----------------")
    print(" Добро пожаловать")
    print("      в игру     ")
    print(" крестики-нолики")
    print("-----------------")
    print(" формат ввода: x y")
    print(" x - номер строки")
    print(" y - номер столбца")

def table():
    print()
    print("    | 0 | 1 | 2 |")
    print("   _______________")
    for i, row in enumerate(field):
        row_str = f"  {i} | {' | '.join(row)} |"
        print(row_str)
        print("  ________________")
    print()


def request():
    while True:
        must = input("Ваш ход:").split()

        if len(must) != 2:
            print("Введите 2 координаты!")
            continue

        x, y = must

        if not (x.isdigit()) or not (y.isdigit()):
            print("Введите координаты!")
            continue

        x, y = int(x), int(y)
        if 0 > x or x > 2 or 0 > y or y > 2:
            print(" Координаты выходят за рамки игрового поля!")
            continue

        if field[x][y] != " ":
            print("Клетка занята!")
            continue

        return x, y


def check_win():
    win_combination = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                      ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                      ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for combination in win_combination:
        symbols = []
        for c in combination:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["x", "x", "x"]:
            print("Выиграл x!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!")
            return True
    return False

welcome()

field = [[" "] * 3 for i in range(3)]
count = 0

while True:
    count += 1

    table()

    if count % 2 == 1:
        print("Ходит крестик")
    else:
        print("Ходит нолик")
    x, y = request()

    if count % 2 == 1:
        field[x][y] = "x"
    else:
        field[x][y] = "0"
    if check_win():
        break
    if count == 9:

        print("Ничья")
        break