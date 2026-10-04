from shoe import Shoe
from hand import Dealer, Player_Hand
import numpy as np
from move import move, DEALER_INDICES
from rules import *

# TODO
    # Implement hit on 17 and other deck scenarios
    # Implement Variations
    # Implement Counting
    # Implement money system
    # Implenet reccords system
        # Grading out of 100
        # Individual bet grades
        # Maybe Seeded scenarios being dealt

#-----------------------#
# Initialize Statistics #
#-----------------------#
occurences = [np.zeros((10,10),dtype=int),
              np.zeros((8,10),dtype=int),
              np.zeros((10,10),dtype=int)]
correct = [np.zeros((10,10),dtype=int),
           np.zeros((8,10),dtype=int),
           np.zeros((10,10),dtype=int)]

#-----------#
# Game Loop #
#-----------#
hands = []
shoe = Shoe(DECKS)
playing = input("Another Hand? (y/n) ").upper() == 'Y'
while playing:
    # Bet
    if MONEY:
        print("Working on it")
        # TODO: ORGANIZE BETTING & Counting
    else:
        bet = 0

    # Deal Hand
    dealer = Dealer(shoe, STAND_ON_SOFT_17)
    hands.append(Player_Hand(shoe,bet))
    for hand in hands:
        while not hand.standing:
            # Play Hand
            valid_choice = False
            while not valid_choice:
                state = hand.analyze()
                match state:
                    case "hard":
                        i = 0
                        j = max(0, min(17-hand.total,9))
                        k = DEALER_INDICES[dealer.showing]
                    case "soft":
                        i = 1
                        j = max(0, min(20-hand.total,7))
                        k = DEALER_INDICES[dealer.showing]
                    case "pair":
                        i = 2
                        j = 9-DEALER_INDICES[hand.cards[0]]
                        k = DEALER_INDICES[dealer.showing]
                occurences[i][j][k] += 1
                print("Dealer Showing:",dealer.showing)
                hand.print(AUTO_CALCULATE_TOTALS)

                match int(input("Player move:\n0-stand\n1-hit\n2-double\n3-split\n4-reveal: ")):
                    case 0:
                        choice = "stand"
                        hand.stand()
                        valid_choice = True

                    case 1:
                        choice = "hit"
                        hand.hit()
                        valid_choice = True

                    case 2:
                        if len(hand.cards) and (not hand.been_split or DOUBLE_AFTER_SPLITTING):
                            choice = "double"
                            hand.double_down()
                            valid_choice = True
                        else:
                            print("Invalid option")
                        
                    case 3:
                        if state == "pair":
                            choice = "split"
                            hands.append(hand.split())
                            valid_choice = True
                        else:
                            print("Invalid option")
                        
                    case 4:
                        option = move(dealer.showing, hand)
                        print("\n",option.upper(),"\n")
                        match option:
                            case "stand":
                                hand.stand()
                            case "hit":
                                hand.hit()
                            case "double":
                                hand.double_down()
                            case "split":
                                hands.append(hand.split())
                        valid_choice = True
                    case _:
                        print("Invalid option")
                        
            if choice == move(dealer.showing, hand):
                correct[i][j][k] += 1
                print("-------\nCORRECT\n-------")
            else:
                print("---------\nINCORRECT\n---------")

            hand.analyze()
            if hand.state == "bust":
                print("----\nBust\n----")
                hand.print(True)

            if len(shoe.cards) < 10:
                shoe.reset()
                print("\n--------\nSHUFFLED\n--------")
                
    playing = input("Another Hand? (y/n) ").capitalize() == 'Y'

grades = [0,0,0]
for i, grade in enumerate(grades):
    grades[i] = np.divide(
    correct[i],
    occurences[i],
    out=np.full_like(correct[i], np.nan, dtype=float),
    where=occurences[i] != 0
    )

print(grades)

hand = ['hard','soft','pair']
for i, grade in enumerate(grades):
    valid = ~np.isnan(grade)
    weighted_average = np.average(
        grade[valid],
        weights=occurences[i][valid]
    )
    print(f"{hand[i]}: {100*weighted_average:.1f}% accuracy")