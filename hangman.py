# Hangman Game
# Author: Edinor Junior
# Import libraries
import random

# Board
board = ['''
>>>>>>>>>>Hangman<<<<<<<<<<
+---+
|   |
    |
    |
    |
    |
=========''', '''
+---+
|   |
O   |
    |
    |
    |
=========''', '''
+---+
|   |
O   |
|   |
    |
    |
=========''', '''
 +---+
 |   |
 O   |
/|   |
     |
     |
=========''', '''
 +---+
 |   |
 O   |
/|\  |
     |
     |
=========''', '''
 +---+
 |   |
 O   |
/|\  |
/    |
     |
=========''', '''
 +---+
 |   |
 O   |
/|\  |
/ \  |
     |
=========''']


# Class
class Hangman:

    # Constructor Method
    def __init__(self, word):
        self.word = word
        self.missed_letters = []
        self.guessed_letters = []

    # Method to guess a letter
    def guess(self, letter):
        if letter in self.word and letter not in self.guessed_letters:
            self.guessed_letters.append(letter)
        elif letter not in self.word and letter not in self.missed_letters:
            self.missed_letters.append(letter)
        else:
            return False
        return True

    # Method to know if the game ends
    def hangman_over(self):
        return self.hangman_won() or (len(self.missed_letters) == 6)

    # Method to check if the player won
    def hangman_won(self):
        if '_' not in self.hide_word():
            return True
        return False

    # Method to hide the letter
    def hide_word(self):
        rtn = ''
        for letter in self.word:
            if letter not in self.guessed_letters:
                rtn += '_'
            else:
                rtn += letter
        return rtn

    # Method to check the game status and show the board
    def print_game_status(self):
        print(board[len(self.missed_letters)])
        print('\nLetter: ' + self.hide_word())
        print('\nWrong Letters: ', )
        for letter in self.missed_letters:
            print(letter, )
        print()
        print('Correct Letters: ', )
        for letter in self.guessed_letters:
            print(letter, )
        print()


# Method to read a word randomic
def rand_word():
    with open("words.txt", "rt") as f:
        bank = f.readlines()
    return bank[random.randint(0, len(bank))].strip()


def main():
    # Object
    game = Hangman(rand_word())

    # While the game is not over, print status and ask a letter doing the read of the character
    while not game.hangman_over():
        game.print_game_status()
        user_input = input('\nType a letter: ')
        game.guess(user_input)

    # Verify the game status
    game.print_game_status()

    # Print the screen message to user conform game status
    if game.hangman_won():
        print('\nCongrats! You win!!')
    else:
        print('\nGame over! You lost.')
        print('The word was: ' + game.word)

    print('\nNice game! Now go study Python!\n')


# Execute program
if __name__ == "__main__":
    main()
