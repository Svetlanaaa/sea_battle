import random
class User:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.killed = True
        self.field = []
        self.field_opponent = []
        for i in range(10):
            self.field.append([' ' for _ in range(10)])
            self.field_opponent.append([' ' for _ in range(10)])

    def set_last(self,x,y, k):
        self.x = x
        self.y = y
        self.killed = k


def show_user_fields():
    print('\nВаше поле: ')
    show(user.field)
    print('\nПоле противника')
    show(user.field_opponent)


def show(field):
    print('  ',end='')
    for i in range(10): print(' ', i + 1, end='')
    for i in range(10):
        print('\n', i + 1, end='')
        for j in range(10): print(' ',field[i][j],end='')


def validate(field, dir, c, start, end):
    if dir == 'h':
        for k in range(start, end):
            if field[c][k] != ' ':
                return False
        return True
    else:
        for k in range(start, end):
            if field[k][c] != ' ':
                return False
        return True


def set_ship(field, dir, c, start, end):
    if dir == 'h':
        for j in range(start, end):
            field[c][j] = 'O'
    else:
        for i in range(start, end):
            field[i][c] = 'O'


def remove_free_places(i1, i2, j1, j2, free, field):
    for i in range(i1, i2):
        for j in range(j1, j2):
            try:
                if field[i][j] == ' ':
                    field[i][j] = '-'
                free.remove(i * 10 + j)
            except:
                continue
    return free


def set_ships(free, field, deck, n):
    for _ in range(n):
        _set = False
        while not _set:
            r = free[random.randint(0, len(free) - 1)]
            x = r // 10
            y = r % 10
            h = random.randint(0,1)

            if h:
                if y - deck + 1 > -1:
                    validated = validate(field, 'h', x, y-deck+1, y)
                    if validated:
                        set_ship(field, 'h', x, y-deck+1, y+1)
                        free = remove_free_places([0, x-1][x-1>-1], [10, x+2][x+2<=10],
                                                  [0, y - deck][y - deck > -1], [10, y + 2][y + 2 <= 10],
                                                  free, field)
                        _set = True

                if not _set and y + deck <= 10:
                    validated = validate(field, 'h', x, y, y+deck)
                    if validated:
                        set_ship(field, 'h', x, y, y+deck)
                        free = remove_free_places([0, x-1][x-1>-1], [10, x+2][x+2<=10],
                                                  [0, y - 1][y - 1 > -1], [10, y + deck + 1][y + deck + 1 <= 10],
                                                  free, field)
                        _set = True

            else:
                if not _set and x - deck + 1 > -1:
                    validated = validate(field, 'v', y, x-deck+1, x)
                    if validated:
                        set_ship(field, 'v', y, x-deck+1, x+1)
                        free = remove_free_places([0, x-deck][x-deck>-1], [10,x+2][x+2<=10],
                                                  [0, y - 1][y - 1 > -1], [10, y + 2][y + 2 <= 10],
                                                  free, field)
                        _set = True

                if not _set and x + deck <= 10:
                    validated = validate(field, 'v', y, x , x + deck)
                    if validated:
                        set_ship(field, 'v', y, x, x+deck)
                        free = remove_free_places([0, x - 1][x - 1 > -1], [10, x + deck+1][x + deck+1 <= 10],
                                                  [0, y - 1][y - 1 > -1], [10, y + 2][y + 2 <= 10],
                                                  free, field)
                        _set = True
    return free


def set_ships_random(field):
    free_places = [i for i in range(100)]
    free_places = set_ships(free_places, field, 4, 1)
    free_places = set_ships(free_places, field, 3, 2)
    free_places = set_ships(free_places, field, 2, 3)
    free_places = set_ships(free_places, field, 1, 4)
    for i in range(len(free_places)):
        x = int(free_places[i] / 10)
        y = free_places[i] % 10
        field[x][y] = '-'

def set_ship_by_user(field, deck):
    _set = False
    while not _set:
        print('\nВведите начальную координату',deck,'-х палубного корабля и его направление (горизонтально, вертикально)\n'
              'строка = ', end='')
        x = int(input()) - 1
        print('столбец = ', end='')
        y = int(input()) - 1
        print('направление (h или v) = ', end='')
        dir = str(input())
        h = dir == 'h'
        res = validate(field, dir, [y, x][h], [x, y][h], [x+deck, y+deck][h])
        if res:
            set_marks(field, dir, [y,x][h], [x, y][h], [x+deck-1, y+deck-1][h])
            _set = True
            print('\nКорабль успешно поставлен!\nВаше поле:\n')
            show(field)
        else:
            print('Ошибка! Корабль не может быть здесь размещен. Попробуйте новые координаты.')


def set_ships_by_user(field):
    set_ship_by_user(field, 4)
    for _ in range(0, 2):
        set_ship_by_user(field, 3)
    for _ in range(0, 3):
        set_ship_by_user(field, 2)
    for _ in range(0, 4):
        set_ship_by_user(field, 1)


def is_killed(x, y, field, opponent):
    if (y-1>-1 and opponent[x][y-1] != '-') or (y+1<10 and opponent[x][y+1] != '-'):
        ind = y - 1
        while ind > -1 and opponent[x][ind] != '-':
            if field[x][ind] != 'X':
                return False, []
            ind -= 1
        while y + 1 < 10 and opponent[x][y + 1] != '-':
            if field[x][y + 1] != 'X':
                return False, []
            y += 1
        return True, ['h', x, ind+1, y]
    else:
        if (x-1>-1 and opponent[x-1][y] != '-') or (x+1<10 and opponent[x+1][y] != '-'):
            ind = x -1
            while ind > -1 and opponent[ind][y] != '-':
                if field[ind][y] != 'X':
                    return False, []
                ind -= 1
            while x + 1 < 10 and opponent[x + 1][y] != '-':
                if field[x + 1][y] != 'X':
                    return False, []
                x += 1
            return True, ['v', y, ind+1, x]
        else:
            return True, ['h', x, y,y]


def get_coor_user():
    get = False
    while not get:
        print('\nВведите координаты:\n строка = ', end='')
        x = int(input()) - 1
        print('столбец = ', end='')
        y = int(input()) - 1

        if 9 < x < 0 or 9 < y < 0:
            print('Ошибка! Номер столбца и строки = 1..10\nПопробуйте снова\n')
        else:
            if user.field_opponent[x][y] != ' ':
                print('Ошибка! Вы уже открыли эту ячейку.\nПопробуйте снова\n')
            else:
                get = True
    return x, y


def set_marks(field, dir,c, start, end):
    if dir == 'h':
        for j in range(start, end+1):
            field[c][j] = 'X'
        for i in range(c-1, c+2):
            if  -1<i<10:
                for j in range(start-1, end+2):
                    if -1<j<10 and field[i][j] == ' ':
                        field[i][j] = '-'
    else:
        for i in range(start, end+1):
            field[i][c] = 'X'
        for j in range(c-1, c+2):
            if  -1<i<10:
                for i in range(start-1, end+2):
                    if -1<j<10 and field[i][j] == ' ':
                        field[i][j] = '-'


def fire(x, y, player, opponent):
    if opponent.field[x][y] == 'O':
        player.field_opponent[x][y] = 'X'
        opponent.field[x][y] = 'X'
        killed, res = is_killed(x, y, player.field_opponent, opponent.field)
        if killed:
            print('Корабль убит!\n')
            set_marks(player.field_opponent, res[0], res[1], res[2], res[3])
            return 2
        else:
            print('Корабль ранен!\n')
            return 1
    else:
        print('Промах...')
        player.field_opponent[x][y] = '-'
        opponent.field[x][y] = '+'
        return 0


def init():
    print("Расставить корабли случайным образом? Y or N\n\t>>", end='')
    ans = str(input())
    if ans == 'Y':
        set_ships_random(user.field)
    else:
        set_ships_by_user(user.field)
    set_ships_random(computer.field)


def near(x, y):

    r = random.randint(0, 3)
    if r == 0:
        return x, y + 1
    else:
        if r == 1:
            return x, y - 1
        else:
            if r == 2:
                return x + 1, y
            else:
                return x - 1, y


def get_coor_computer():

    get = False
    while not get:
        if computer.x != -1 and computer.y != -1 and not computer.killed:
            x, y = near(computer.x, computer.y)
        else:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

        if computer.field_opponent[x][y] == ' ':
            get = True
    return x, y


def get_coor(flag_player):
    if flag_player:
        return get_coor_user()
    else:
        return get_coor_computer()


def make_a_move(s, player, opponent, flag_user):
    miss = False
    killed_ships = 0
    while not miss:
        print(s)
        x, y = get_coor(flag_user)
        res = fire(x, y, player, opponent)
        if res == 0:
            miss = True
        else:
            player.set_last(x,y, False)
            if res == 2:
                player.killed = True
                killed_ships += 1
        show_user_fields()
    return killed_ships


def play():
    killed_ships_by_user = 0
    killed_ships_by_computer = 0

    while killed_ships_by_user != 10 or killed_ships_by_computer != 10:
        killed_ships_by_user += make_a_move('\n\nВаш ход', user, computer, True)
        killed_ships_by_computer += make_a_move('\n\nХод компьютера', computer, user, False)
    if killed_ships_by_user == 10:
        print('\nВы выиграли!')
    else:
        print('\nВы проиграли!')



user = User()
computer = User()
init()
play()