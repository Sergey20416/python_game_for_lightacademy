import os
import msvcrt
from random import randint

from prettytable import PrettyTable
from termcolor import colored

from Player import Player


class App:
    def __init__(self):
        # Массив игроков
        self.players = [
            Player('Игрок', 'player'),
            Player('Компьютер', 'computer'),
        ]

        # Массив действий
        self.actions = [
            {
                'name': 'Умеренный урон',
                'type': 'damage',
                'range': range(18, 26)
            },
            {
                'name': 'Сильный урон',
                'type': 'damage',
                'range': range(10, 35)
            },
            {
                'name': 'Исцеление',
                'type': 'healing',
                'range': range(18, 26)
            },
        ]

        # Текущий ход
        self.stepIterator = 0

        # Игрок который сейчас ходит
        self.currentPlayer = None

        # Текущий противник
        self.currentRival = None

        # Текущее действие
        self.currentAction = None

        # Описание текущего хода
        self.message = ''

        # Таблица отображаемая на экране
        self.table = ''

        # Статус игры
        self.gameIsOn = False

    # Создаёт таблицу с информацией об игроках и текущем ходе
    def makeTable(self):
        self.table = ''
        table = PrettyTable()
        playerNames = []
        playersHealth = []
        currentStep = [
            self.stepIterator > 0 and
            "Сейчас ходит: {}".format(
                colored(self.currentPlayer.name, 'green')
            ) or '',
            self.message
        ]

        for player in self.players:
            playerName = colored(player.name, 'white')
            if self.stepIterator > 0:
                if self.currentPlayer.name == player.name:
                    playerName = colored(player.name, 'green')
                else:
                    playerName = colored(player.name, 'yellow')
            playerNames.append(playerName)
            playersHealth.append(player.health)

        table.add_column("Имя", playerNames)
        table.add_column("Здоровье", playersHealth)
        self.stepIterator > 0 and table.add_column(
            "Текущий ход ({})".format(self.stepIterator), currentStep
        )
        table.align = "l"
        self.table = table

    # Создаёт сообщение о текущем действии
    def makeMessage(self):
        if self.currentAction['type'] == 'damage':
            self.message = "{} наносит {} \"{}\" {}".format(
                colored(self.currentPlayer.name, 'green'),
                colored(self.currentRival.name+'у', 'yellow'),
                self.currentAction['name'],
                colored(self.currentActionValue, 'cyan'),
            )
        elif self.currentAction['type'] == 'healing':
            self.message = "{} исцеляет себя на {} единиц".format(
                colored(self.currentPlayer.name, 'green'),
                colored(self.currentActionValue, 'cyan'),
            )

    # Проверяет жив ли текущий противник
    def isAlive(self):
        if self.currentRival.health == 0:
            return False
        else:
            return True

    # Завершает игру
    def gameOver(self):
        self.gameIsOn = False
        print("[ Игра окончена, победил  {} ]".format(
            colored(self.currentPlayer.name, 'green')
        ))

    # Случайно определяет игрока, действие и силу действия в заданом диапазоне
    def nextStep(self):
        self.stepIterator += 1
        self.message = ''
        r_p = randint(0, 1)
        self.currentPlayer = self.players[r_p]
        self.currentRival = self.players[r_p-1]
        # Увеличивает компьютеру шанс на "Исцеление" если его здоровье менее 35
        if self.currentPlayer.tag == 'computer' and self.currentPlayer.health < 35:
            r = randint(0, len(self.actions))
            r_a = r > 2 and 2 or r
        else:
            r_a = randint(0, len(self.actions) - 1)
        self.currentAction = self.actions[r_a]
        self.currentActionValue = randint(
            self.currentAction['range'][0],
            self.currentAction['range'][-1]
        )

    # Отвечает за логику действий
    def step(self):
        self.nextStep()
        self.makeMessage()
        if self.currentAction['type'] == 'damage':
            self.currentRival.damage(self.currentActionValue)
        elif self.currentAction['type'] == 'healing':
            self.currentPlayer.healing(self.currentActionValue)
        self.render()
        if self.isAlive() is False:
            self.gameOver()
            return 0

    # Рисует таблицу в консоли
    def render(self):
        os.system('cls')
        self.makeTable()
        print(self.table)

    # Метод запускающий игру
    def run(self):
        self.gameIsOn = True
        self.render()
        count = []
        while self.gameIsOn:
            print(
                'Нажми любую кнопку для продолжения (для завержения нажми Esc)'
            )
            char = msvcrt.getch()
            if char and char != b'\x1b':
                self.step()
            else:
                self.gameIsOn = False


app = App()
app.run()
