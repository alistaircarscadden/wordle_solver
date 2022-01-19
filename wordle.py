from enum import Enum
from random import choice

class Colours(Enum):
    '''The colours the game qualifies your letters with.'''

    GREEN = 'G'
    YELLOW = 'y'
    GREY = '-'


class Game:
    '''A game of Wordle. Has a hidden answer and you can make guesses on it.'''

    def __init__(self, word_list, answer=None):
        self.results = []
        self.guesses = []
        self.win = False

        if not answer:
            self.answer = choice(word_list)
        else:
            self.answer = answer
    

    def guess(self, word):
        result = [Colours.GREY] * 5
        
        self.results.append(result)
        self.guesses.append(word)

        if word == self.answer:
            self.win = True

        for i in range(5):
            if word[i] == self.answer[i]:
                result[i] = Colours.GREEN
        
        for i in range(5):
            if result[i] != Colours.GREEN:
                for j in range(5):
                    if result[j] != Colours.GREEN and self.answer[j] == word[i]:
                        result[i] = Colours.YELLOW
                        break

    
    def get_results(self):
        return self.results
    

    def get_guesses(self):
        return self.guesses


    def guessed_correctly(self):
        return self.win
