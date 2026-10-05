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
        self.count()

    # Adds a new card to hand
    def hit(self):
        self.cards.append(self.shoe.draw())
        self.count()

    # Changes the status to stand
    def stand(self):
        self.standing = True

    # Calculates Total
    def count(self):
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

class Dealer(Hand):
    def __init__(self, shoe, st17):
        super().__init__(shoe)
        self.showing = self.cards[0]
        self.STAND_ON_SOFT_17 = st17

    def hit(self):
        super().hit()
        print("Dealer Hits")

    def stand(self):
        super().stand()
        if self.state == "bust":
            print("Dealer Busts")
        else:
            print("Dealer Stands")

    # Calculates total and descides move
    def play(self):
        while not self.standing:
            self.count()
            self.print()

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
                if not self.soft or self.STAND_ON_SOFT_17:
                    self.state = "stand"
                    self.stand()
                else:
                    self.state = "hit"
                    self.hit()
            else:
                self.state = "hit"
                self.hit()

        return self.state

    # Prints the dealer's hand
    def print(self):
        print("Dealer:", self.cards, f"({self.total})")

class Player_Hand(Hand):
    def __init__(self, shoe, bet, cards = None):
        super().__init__(shoe, cards)
        self.bet = bet
        self.been_split = False

    def double_down(self):
        self.bet *= 2
        self.hit()
        self.stand()
        self.print(True)

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
        super().count()

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

    def compare(self, dealer):
        player_blackjack = (
            self.total == 21
            and len(self.cards) == 2
            and not self.been_split
        )

        dealer_blackjack = (
            dealer.total == 21
            and len(dealer.cards) == 2
        )

        if self.state == "bust":
            self.outcome = "loss"

        # Deal with natural blackjacks
        elif player_blackjack and dealer_blackjack:
            self.outcome = "push"
        elif player_blackjack:
            self.outcome = "blackjack"
        elif dealer_blackjack:
            self.outcome = "loss"

        # Deal with normal comparison
        elif dealer.state == "bust":
            self.outcome = "win"
        elif self.total > dealer.total:
            self.outcome = "win"
        elif self.total == dealer.total:
            self.outcome = "push"
        else:
            self.outcome = "loss"

        return self.outcome
            
    def print(self, calculate_total):
        if calculate_total:
            print("Hand:",self.cards,f"({self.total})")
        else:
            print("Hand:",self.cards)