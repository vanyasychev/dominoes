import random


class Dominoes:
    messages = ("It's your turn to make a move. Enter your command.",
                'Computer is about to make a move. Press Enter to continue...',
                'The game is over. You won!',
                'The game is over. The computer won!',
                "The game is over. It's a draw!",
                'Illegal move. Please try again.')

    def __init__(self):
        self.stock_pieces = list()
        self.computer_pieces = list()
        self.player_pieces = list()
        self.snake = list()
        self.status = str()

    def domino_set(self):
        domino = [[i, j] for i in range(0, 7) for j in range(i, 7)]
        random.shuffle(domino)

        self.stock_pieces = domino[0:14]
        self.computer_pieces = domino[14:21]
        self.player_pieces = domino[21:]

    def domino_snake(self):
        while not self.snake:
            maximum = max(max(self.computer_pieces), max(self.player_pieces))
            if maximum[0] == maximum[1]:
                self.snake = [maximum]
            else:
                self.domino_set()

        if self.snake[0] in self.computer_pieces:
            self.computer_pieces.remove(self.snake[0])
            self.status = Dominoes.messages[0]
        else:
            self.player_pieces.remove(self.snake[0])
            self.status = Dominoes.messages[1]

    def user_move(self):
        while True:
            try:
                n = int(input())

                if -len(self.player_pieces) <= n <= len(self.player_pieces):
                    break
                print('Invalid input. Please try again.')
            except ValueError:
                print('Invalid input. Please try again.')

        if n > 0:
            if self.player_pieces[n - 1][0] == self.snake[-1][-1]:
                self.snake.append(self.player_pieces[n - 1])
                self.player_pieces.pop(n - 1)
            elif self.player_pieces[n - 1][1] == self.snake[-1][-1]:
                self.snake.append(list(reversed(self.player_pieces[n - 1])))
                self.player_pieces.pop(n - 1)
            else:
                print('Illegal move. Please try again.')
                self.user_move()
        elif n < 0:
            if self.player_pieces[abs(n) - 1][0] == self.snake[0][0]:
                self.snake.insert(0, list(reversed(self.player_pieces[abs(n) - 1])))
                self.player_pieces.pop(abs(n) - 1)
            elif self.player_pieces[abs(n) - 1][1] == self.snake[0][0]:
                self.snake.insert(0, self.player_pieces[abs(n) - 1])
                self.player_pieces.pop(abs(n) - 1)
            else:
                print('Illegal move. Please try again.')
                self.user_move()
        else:
            if len(self.stock_pieces) != 0:
                self.player_pieces.append(self.stock_pieces[0])
                self.stock_pieces.pop(0)

    def computer_move(self):
        input()

        number_of_digits = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for i in self.computer_pieces + self.snake:
            for j in i:
                number_of_digits[j] += 1

        points = dict()
        for i in self.computer_pieces:
            points.update({sum(i): i})

        for key in sorted(points)[::-1]:
            if points[key][0] == self.snake[0][0]:
                self.snake.insert(0, list(reversed(points[key])))
                self.computer_pieces.remove(points[key])
                break
            elif points[key][1] == self.snake[0][0]:
                self.snake.insert(0, points[key])
                self.computer_pieces.remove(points[key])
                break
            elif points[key][0] == self.snake[-1][-1]:
                self.snake.append(points[key])
                self.computer_pieces.remove(points[key])
                break
            elif points[key][1] == self.snake[-1][-1]:
                self.snake.append(list(reversed(points[key])))
                self.computer_pieces.remove(points[key])
                break
        else:
            if len(self.stock_pieces) != 0:
                self.computer_pieces.append(self.stock_pieces[0])
                self.stock_pieces.pop(0)

    def game_status(self):
        if len(self.player_pieces) == 0:
            self.status = Dominoes.messages[2]
        elif len(self.computer_pieces) == 0:
            self.status = Dominoes.messages[3]
        elif self.snake[0][0] == self.snake[-1][-1]:
            counter = 0
            for i in self.snake:
                for j in i:
                    counter += 1 if j == self.snake[0][0] else 0

            if counter == 8:
                self.status = Dominoes.messages[4]

    def interface(self):
        self.domino_set()
        self.domino_snake()

        while True:
            print('=' * 70)
            print('Stock size:', len(self.stock_pieces))
            print('Computer pieces:', len(self.computer_pieces), end='\n\n')

            if len(self.snake) > 6:
                print(*[i for i in self.snake[:3]], '...',
                      *[i for i in self.snake[-3:]], sep='')
            else:
                print(*[i for i in self.snake], sep='')

            print('\nYour pieces:')
            for count, value in enumerate(self.player_pieces):
                print(f'{count + 1}:{value}')

            print('\nStatus:', self.status)
            if self.status in Dominoes.messages[2:5]:
                break

            if self.status == Dominoes.messages[0]:
                self.user_move()
                self.status = Dominoes.messages[1]
            else:
                self.computer_move()
                self.status = Dominoes.messages[0]

            self.game_status()


if __name__ == '__main__':
    Dominoes().interface()
