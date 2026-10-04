import random
import time

class Shoe:
    def __init__(self, decks):
        deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = []
        self.played = []
        self.decks = decks
        self.count = 0
        for card in deck:
            for i in range(decks*4):
                self.cards.append(card)
        random.seed(time.time())
        random.shuffle(self.cards)

    def draw(self):
        card = self.cards.pop(0)
        self.played.append(card)
        if card in ["2", "3", "4", "5", "6"]:
            self.count += 1
        if card in ["10", "J", "Q", "K", "A"]:
            self.count -= 1
        return card

    def shuffle(self):
        random.shuffle(self.cards)
        self.count = 0

    def reset(self):
        random.shuffle(self.played)
        for card in self.played:
            self.cards.append(card)
        self.played.clear()

    def true_count(self):
        return self.count / (len(self.cards) / 52)