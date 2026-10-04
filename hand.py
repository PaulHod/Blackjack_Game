from shoe import Shoe

class Hand:
    deck = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10
    }

    # Initiates Hand with two cards
    def __init__(self, shoe, cards=None):
        self.shoe = shoe
        self.standing = False
        self.state = ""

        if cards is None:
            self.cards = [self.shoe.draw(), self.shoe.draw()]
        else:
            self.cards = cards

    # Adds a new card to hand
    def hit(self):
        self.cards.append(self.shoe.draw())

    # Changes the status to stand
    def stand(self):
        self.standing = True

class Dealer(Hand):
    def __init__(self, shoe, st17):
        super().__init__(shoe)
        self.showing = self.cards[0]
        self.STAND_ON_SOFT_17 = st17

    # Calculates total and descides move
    def analyze(self):
        self.total = 0
        soft = False

        # Calculate total
        for card in self.cards:
            self.total += self.deck[card]

            if card == "A" and not soft:
                self.total += 10
                soft = True

        # Convert soft Ace from 11 -> 1 if necessary
        if soft and self.total > 21:
            self.total -= 10
            soft = False

        # Determine dealer state
        if self.total > 21:
            self.state = "bust"
            self.stand()
        elif self.total > 17:
            self.state = "stand"
            self.stand()
        elif self.total == 17:
            # Hard 17 always stands
            # Soft 17 depends on casino rules
            if not soft or self.STAND_ON_SOFT_17:
                self.state = "stand"
                self.stand()
            else:
                self.state = "hit"
        else:
            self.state = "hit"

        return self.state

class Player_Hand(Hand):
    def __init__(self, shoe, bet, cards = None):
        super().__init__(shoe, cards)
        self.bet = bet
        self.been_split = False

    def double_down(self):
        self.bet *= 2
        self.hit()
        self.stand()

    def split(self):
        split_card = self.cards.pop()
        new_hand = Player_Hand(self.shoe,
                               self.bet,
                               cards=[split_card])
        self.hit()
        new_hand.hit()

        self.been_split = True
        new_hand.been_split = True

        return new_hand

    # Returns total and hard/soft
    def analyze(self):
        self.total = 0
        self.soft = False

        # Calculate Hard Total
        for card in self.cards:
            self.total += self.deck[card]
            if card == "A" and not self.soft:
                self.total += 10
                self.soft = True

        if self.soft == True and self.total > 21:
            self.total -= 10
            self.soft = False

        # Determine Hand Type
        if self.total > 21:
            self.state = "bust"
            self.stand()
        elif len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            self.state = "pair"
        elif self.soft:
            self.state = "soft"
        else:
            self.state = "hard"
            
        return self.state

    def print(self, calculate_total):
        if calculate_total:
            print("Hand:",self.cards,f"({self.total})")
        else:
            print("Hand:",self.cards)