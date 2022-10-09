"""
2048游戏，这个算是比较经典的游戏程序了吧，拿来做个练习可以
运行后会画出一个游戏界面，但是这个界面有点简陋，而且是在命令行输出的，
而且也还有就是边界对不齐的问题，如果能够弹出一个单独的界面来玩这个游戏就更好了
通过wasdqr等键位进行控制，来实现数字的移动和叠加，
初始时随机生成两个数字，然后开始移动，根据所设定的规则进行游戏
当所有的空格被填满的时候不能再叠加，游戏结束,r键重新游戏，q键退出程序
当达到设定的分数要求即2048时，游戏胜利
"""
import curses
from random import randrange, choice
from collections import defaultdict

# 这一段的作用就是将键盘键位和上下左右操作对应在一起
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))

def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def transpose(field):
    return [list(row) for row in zip(*field)]


def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = 2048
        self.score = 0
        self.highscore = 0
        self.reset()


    def spawn(self):
        # 随机生成一个数值，当随机数大于89小于100则元素为4，0到89时为2，也就是生成的随机数只是2或者4
        new_element = 4 if randrange(100) > 89 else 2
        # 选择一个位置，放上2或者4
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):
        # 对分数进行计数，保留历史最高分数，如果当前的分数大于历史最高，那么当前的分数就是最高分
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        # 初始化随机生成两个数字
        self.spawn()
        self.spawn()

#   棋盘中移动的函数，获取用户动作，然后根据相应的动作进行移动
    def move(self,direction):
        def move_row_left(row):
            # 将一行中的非0元素全部移动到左边
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            # 将相同的元素聚合
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        # 元素值翻倍，计算新的分数
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        # 边界条件和相邻元素相等条件
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))

        moves = {}
        # 只需要 定义一个向左的函数，向右的是向左的逆，然后上下的是转置
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))
        # 调用move函数时，先判断收可以移动，可以移动时再根据相应的操作进行移动
        if direction in moves:
            if self.move_is_possible(direction):
                # 将原位置上的元素移动，然后新生成一个随机数
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    # 游戏胜利条件，当前棋盘中有值大于等于2048
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)
    # 游戏失败
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    # 判断此时是否可以再移动，如果不能移动，is_gameover函数被激活，游戏结束
    def move_is_possible(self, direction):
        def row_is_left_movable(row):

            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit      '
        gameover_string = '           GAME OVER      '
        win_string = '          YOU WIN!       '

        def cast(string):
            screen.addstr(string + '                                               ')


        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            cast(line)


        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))

        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()


        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

def main(stdscr):
    # 在main的部分先定义了几个函数，函数最后看，调用哪一个具体分析哪一个，从main中定义的变量开始
    def init():
        # 进行初始化，调用GameField中的reset函数对棋盘重置
        game_field.reset()
        # 返回Game值，进入游戏，即进入game函数
        return 'Game'

    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    def game():
        # 例程工作在屏幕、窗口和子窗口上。我们总会有一个curses窗口，称之为stdscr,与物理屏幕是同样大小尺寸。
        # stdscr可以称之为逻辑屏幕。逻辑屏幕的布局是一个字符数组，（0,0）是屏幕左上角，坐标是（y,x）即（行，列）
        game_field.draw(stdscr)
        # 获取用户动作
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):  # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    # 将这个state_actions和上面定义的函数对应
    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }
    curses.use_default_colors()

    # 将GameField初始化一个变量，使用这个变量调用GameField中的各个函数
    game_field = GameField(win=2048)

    # 首先调用Init函数进行初始化，当state值不是exit时，程序一直执行，此时通过按键即可操作程序
    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()

# 程序开始，调用curses利用键盘的上下左右键信息
curses.wrapper(main)