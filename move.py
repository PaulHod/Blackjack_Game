from rules import *

DEALER_INDICES = {
    "A": 9,
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "10":8,
    "J": 8,
    "Q": 8,
    "K": 8
}  

def move(showing, hand):

    state = hand.analyze()
    total = hand.total
    dealer_index  = DEALER_INDICES[showing]

    match state:
        case "hard":
            if total > 17:
                total = 17
            if total < 8:
                total = 8
            option = hard[total][dealer_index]
        case "soft":
            if total > 20:
                total = 20
            option = soft[total][dealer_index]
        case "pair":
            option = pairs[hand.cards[0]][dealer_index]
        case "bust":
            return "bust"

    match option:
        case "S":
            return "stand"

        case "H":
            return "hit"

        case "Dh":
            if len(hand.cards) == 2 and (not hand.been_split or DOUBLE_AFTER_SPLITTING): # If you can double
                return "double"
            else:
                return "hit"

        case "Ds":
            if len(hand.cards) == 2 and (not hand.been_split or DOUBLE_AFTER_SPLITTING): # If you can double
                return "double"
            else:
                return "stand"

        case "P":
            return "split"

        case "Ph":
            if DOUBLE_AFTER_SPLITTING:
                return "split"
            else:
                return "hit"
            
        case "Pd":
            if DOUBLE_AFTER_SPLITTING:
                return "split"
            elif not hand.been_split:
                return "double"
            else:
                return "hit"
                
        case "Rh":
            if SURRENDER_ALLOWED and len(hand.cards) == 2:
                return "surrender"
            else:
                return "hit"

        case "Rs":
            if SURRENDER_ALLOWED and len(hand.cards) == 2:
                return "surrender"
            else:
                return "stand"
    return "bro how'd you get here"