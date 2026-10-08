import numpy as np
from rules import *

class Count_Test:
    def __init__(self, shoe):
        self.occurences = 0
        self.correct = 0
        self.shoe = shoe

    def assess(self):
        self.occurences += 1
        running_count_guess = int(input("Running Count? "))
        if running_count_guess == self.shoe.count:
            self.correct +=1
            print("-------\nCORRECT\n-------")
        else:
            print("---------\nINCORRECT\n---------")
            print(f"Running Count: {self.shoe.count}")

    def result(self):
        return f"Counting {100*self.correct/self.occurences:.1f}% Accurate"

def Bet_Spread(true_count, spread):
    true_count = int(true_count)
    spread = int(spread)
    spread4 = {1:1, 2:2, 3:3, 4:4, 5:4, 6:4}
    spread8 = {1:1, 2:2, 3:4, 4:6, 5:8, 6:8}
    spread12= {1:1, 2:2, 3:4, 4:6, 5:8, 6:12}
    spread16= {1:1, 2:2, 3:4, 4:8, 5:12,6:16}

    true_count = np.max((np.min((true_count, 6)), 1))
    
    match spread:
        case 4:
            return spread4[true_count]
        case 8:
            return spread8[true_count]
        case 12:
            return spread12[true_count]
        case 16:
            return spread16[true_count]

class Bet_Test:
    def __init__(self, shoe, starting_cash):
        self.balance = starting_cash
        self.shoe = shoe
        self.stats = []
        # TODO: Use base_bet and spread

    def asses(self):
        print(f"Balance: ${self.balance}")
        bet = int(input(f"Count {int(self.shoe.true_count())}, Base: {BASE_BET} Bet: "))
        # Check if bet follows spread
        correct_bet = BASE_BET*Bet_Spread(self.shoe.true_count(), BET_SPREAD)
        if bet == correct_bet:
            print("-----------\nCorrect Bet\n-----------")
        elif bet != correct_bet:
            print(f"--------------\nIncorrect Bet\n-------------\n ${correct_bet}\n-------------")
        self.stats.append(1-np.abs(correct_bet-bet)/correct_bet)
        return bet

    def result(self):
        return f"Betting {np.average(self.stats)*100}% Accurate"
