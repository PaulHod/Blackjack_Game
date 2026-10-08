import numpy as np

from shoe import Shoe
from hand import Dealer, Player_Hand
from move import move, DEALER_INDICES
from rules import *
from tests import Count_Test, Bet_Test

# TODO
    # Implement money
        # Implement Counting
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

shoe = Shoe(DECKS)

if COUNTING_ENABLED:
    count_test = Count_Test(shoe)

if MONEY:
    bet_test = Bet_Test(shoe, STARTING_CASH)

#-----------#
# Game Loop #
#-----------#

playing = input("Another Hand? (y/n) ").upper() == 'Y'
while playing:

    # Betting
    if MONEY:
        bet = bet_test.asses()
    else:
        bet = 0

    # Deal Hand
    hands = []
    hands.append(Player_Hand(shoe,bet))
    dealer = Dealer(shoe, STAND_ON_SOFT_17)

    dealer.count()
    hands[0].count()

    # Check for player blackjack
    if hands[0].total == 21 and len(hands[0].cards) == 2:
        hands[0].stand()
        hands[0].print(True)
        print("Blackjack")
    # Check for dealer blackjack
    if dealer.total == 21 and len(dealer.cards) == 2:
        hands[0].analyze()
        outcome = hands[0].compare(dealer)
        print(f"Dealer Blackjack: {outcome}")
        hands[0].print(True)
        if COUNTING_ENABLED:
            count_test.assess()
        playing = input("Another Hand? (y/n) ").upper() == 'Y'
        continue

    for hand in hands:
        while not hand.standing:
            # Play Hand
            valid_choice = False

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
                case "blackjack":
                    print("Blackjack")              
            occurences[i][j][k] += 1


            while not valid_choice:
                print("Dealer Showing:",dealer.showing)
                hand.print(AUTO_CALCULATE_TOTALS)
                choice = input("Player move:\n0-stand\n1-hit\n2-double\n3-split\n4-reveal: ")   
                correct_choice = move(dealer.showing, hand)
                match choice:
                    case '0':
                        choice = "stand"
                        hand.stand()
                        valid_choice = True

                    case '1':
                        choice = "hit"
                        hand.hit()
                        valid_choice = True

                    case '2':
                        if len(hand.cards) == 2 and (not hand.been_split or DOUBLE_AFTER_SPLITTING):
                            choice = "double"
                            hand.double_down()
                            valid_choice = True
                        else:
                            print("Invalid option")
                        
                    case '3':
                        if state == "pair":
                            choice = "split"
                            hands.append(hand.split())
                            valid_choice = True
                        else:
                            print("Invalid option")
                        
                    case '4':
                        match correct_choice:
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

            if choice == correct_choice:
                correct[i][j][k] += 1
                print("-------\nCORRECT\n-------")
            elif choice == '4':
                print("----\nHINT\n----")
                print("\n",correct_choice.upper(),"\n")
            else:
                print("---------\nINCORRECT\n---------")
                print(correct_choice)

            hand.analyze()
            if hand.state == "bust":
                print("----\nBust\n----")
                hand.print(True)

    # Dealer Plays
    dealer.play()

    if len(shoe.cards) < 10:
        shoe.reset()
        print("\n--------\nSHUFFLED\n--------")

    # Calculate outcomes:
    for i, hand in enumerate(hands):
        outcome = hand.compare(dealer)
        if MONEY:
            if outcome == "loss":
                winnings = -hand.bet
            elif outcome == "win":
                winnings = hand.bet
            elif outcome == "blackjack":
                winnings = int(hand.bet*1.5)
            else:
                # Nothing!
                winnings = 0
            bet_test.balance += winnings
            print(f"Hand {i+1}: {outcome} ${winnings}")
        else:
            print(f"Hand {i+1}: {outcome}")

    # Test running count
    if COUNTING_ENABLED:
        count_test.assess()
                
    playing = input("Another Hand? (y/n) ").capitalize() == 'Y'

grades = [0,0,0]
for i, grade in enumerate(grades):
    grades[i] = np.divide(
    correct[i],
    occurences[i],
    out=np.full_like(correct[i], np.nan, dtype=float),
    where=occurences[i] != 0
    )

hand = ['hard ','soft ','pairs']
for i, grade in enumerate(grades):
    if occurences[i].sum() != 0:
        valid = ~np.isnan(grade)
        weighted_average = np.average(
            grade[valid],
            weights=occurences[i][valid]
        )
        print(f"{hand[i]}: {100*weighted_average:.1f}% accuracy")
    else:
        print(f"{hand[i]} not played")

if COUNTING_ENABLED:
    print(count_test.result())

if MONEY:
    print(bet_test.result())