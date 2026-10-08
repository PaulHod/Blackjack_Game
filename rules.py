# Blackjack Rules
DECKS = 4   # 1, 2, 4+
STAND_ON_SOFT_17 = True
DOUBLE_AFTER_SPLITTING = True
SURRENDER_ALLOWED = False

# Game Rules
COUNTING_ENABLED = True
VARIATIONS_ENABLED = False
AUTO_CALCULATE_TOTALS = False
TIMER = False

MONEY = True
STARTING_CASH = 1000
BASE_BET = 10
MAX_BET = 500
BET_SPREAD = 12

# Import rules 
match (DECKS, STAND_ON_SOFT_17):
    case (1, True):
        from Strategy_Charts.Single_Deck_S17 import hard, soft, pairs
    case (2, True):
        from Strategy_Charts.Double_Deck_S17 import hard, soft, pairs
    case (4, True):
        from Strategy_Charts.Multiple_Deck_S17 import hard, soft, pairs
    case _:
        print("Uknown Setup")