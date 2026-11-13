import random
from enum import Enum

colors = ["pique", "trefle", "carreau", "coeur"]
nums = ["AS", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
tetes = ["J", "Q", "K"]
totalCards = 52

class WinStatus(Enum):
    # INSTA WIN
    PLAYER_21 = "p21"
    ORDI_21 = "o21"
    PLAYER_OVER_21 = "p+21"
    ORDI_OVER_21 = "o+21"
    # WIN if both stopped
    PLAYER_HIGHER = "p+"
    ORDI_HIGHER = "o+"
    EQUALS = "e"
    # no winner yet
    CONTINU = "c"

commands = ["MAIN", "DRAW", "STOP"]

cartesJoueur = []
cartesOrdi = []

class Card:
    def __init__(self, suit:str, rank:str):
        self.suit = suit
        self.rank = rank

mainJoueur = []
mainOrdi = []

def check_win_status(stopped = False) -> WinStatus:
    # get scores
    value_player = somme_points(mainJoueur)
    value_ordi = somme_points(mainOrdi)

    if value_player == 21: # player is 21 : win
        return WinStatus.PLAYER_21
    elif value_ordi == 21: # ordi is 21 : win
        return WinStatus.ORDI_21
    elif value_player > 21: # player OVER 21 : loss
        return WinStatus.PLAYER_OVER_21
    elif value_ordi > 21: # ordi OVER 21 : loss
        return WinStatus.ORDI_OVER_21
    elif stopped: # If both have stopped drawing
        if value_ordi > value_player: # and ordi is better
            return WinStatus.ORDI_HIGHER
        elif value_player > value_ordi: # of player is better
            return WinStatus.PLAYER_HIGHER
        else:
            return WinStatus.EQUALS # player and ordi are equals
    else:
        return WinStatus.CONTINU # they have not stopped : we continue playing


def card_exists(card: Card) -> bool:
    for c in mainJoueur:
        if c.suit == card.suit and c.rank == card.rank:
            return True
    for c in mainOrdi:
        if c.suit == card.suit and c.rank == card.rank:
            return True
    return False

def cards_left() -> int:
    found = len(mainJoueur)
    found += len(mainOrdi)
    return totalCards - found

def card_value(card):
    if card.rank == "AS":
        return 11
    elif card.rank in tetes:
        return 10
    else:
        return int(card.rank)

def somme_points(hand):
    as_amount = 0
    points = 0
    for card in hand:
        if card.rank == "AS":
            as_amount += 1
        else:
            points += card_value(card)
    for i in range(as_amount):
        if (points + 11) > 21:
            points += 1
        else:
            points += 11
    return points

def draw_card():
    card = Card(suit=random.choice(colors), rank=random.choice(nums))
    drawn = [card]
    while card_exists(card):
        card = Card(suit=random.choice(colors), rank=random.choice(nums))
        if not card in drawn:
            drawn.append(card)
        if len(drawn) >= totalCards:
            print("GAME IS CRASHED")
            print("GAME IS CRASHED")
            print("GAME IS CRASHED")
            print("There is no more cards available to draw")
            raise RuntimeError("NO MORE CARDS AVAILABLE")
    return card

def play_main():
    print("Voici votre main:")
    for card in mainJoueur:
        print(f" - {card.rank} de {card.suit}")

def play_draw():
    pass

def play_stop():
    pass

def tour():
    print(f"Votre main vaut {somme_points(mainJoueur)}")
    # print actions
    print("Actions:")
    print(" - MAIN : obtenez vos cartes exactes en main")
    print(" - DRAW : vous piochez une carte.")
    print("   L'ordi choisira de suivre ou arrêter")
    print(" - STOP : vous arrêtez de piocher")
    print("   L'ordi choisira de continuer ou arrêter")
    # get action
    action = input()
    if not action.upper() in commands: # command not recognized
        print("Nous n'avons pas compris...")
        print()
        tour() # rerun tour
    # EXEC ACTION
    match action.upper():
        case "MAIN":
            play_main()
            tour()
        case "DRAW":
            play_draw()
        case "STOP":
            play_stop()

def main():
    print("Bienvenu dans BlackJack!")
    print("Utilisez [Entrée] pour lancer le jeu")
    print()
    input()

    # draw 2 cartes pour joueur
    print("Vous piochez deux cartes...")
    joueur1 = draw_card()
    joueur2 = draw_card()
    print(f"Vous avez pioché {joueur1.rank} de {joueur1.suit}")
    print(f"Vous avez pioché {joueur2.rank} de {joueur2.suit}")
    mainJoueur.append(joueur1)
    mainJoueur.append(joueur2)
    # draw 2 cartes ordi
    print("L'ordinateur pioche deux cartes...")
    mainOrdi.append(draw_card())
    mainOrdi.append(draw_card())

    # check insta-win
    check_win_status()

    # enter main game loop
    tour()

main()