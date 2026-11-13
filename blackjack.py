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

commands = ["MAIN", "DRAW", "STOP", "ACTION"]

class Card:
    def __init__(self, suit:str, rank:str):
        self.suit = suit
        self.rank = rank

mainJoueur = []
mainOrdi = []
ordiDrawing:bool = True
playerDrawing:bool = True

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

def card_value(card) -> int:
    if card.rank == "AS":
        return 11
    elif card.rank in tetes:
        return 10
    else:
        return int(card.rank)

def somme_points(hand) -> int:
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

def draw_card() -> Card:
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

def ordi_draw():
    global ordiDrawing
    if cards_left() == 0: # check if no cards
        ordiDrawing = False # to stop running this if player stopped too
        no_cards_left()
        return
    # check if the ordi should not draw
    if not ordiDrawing:
        tour()
        return
    if somme_points(mainOrdi) >= 17:
        print("L'ordi choisi d'arrêter de piocher.")
        ordiDrawing = False
        if not playerDrawing: # if player stopped drawing - run conventional
            conventional_stop()
        elif playerDrawing:
            tour()
        return
    # ordi draws
    mainOrdi.append(draw_card())
    print("L'ordi pioche une carte...")
    # check winning
    result = check_win_status()
    if result == WinStatus.ORDI_21:
        loss_21()
    elif result == WinStatus.ORDI_OVER_21:
        win_plus_21()
    elif playerDrawing:
        tour()

def play_actions():
    # print actions
    print("Actions:")
    print(" - MAIN : obtenez vos cartes exactes en main")
    print(" - DRAW : vous piochez une carte.")
    print("   L'ordi choisira de suivre ou arrêter")
    print(" - STOP : vous arrêtez de piocher")
    print("   L'ordi choisira de continuer ou arrêter")

def play_main():
    print("Voici votre main:")
    for card in mainJoueur:
        print(f" - {card.rank} de {card.suit}")

def play_draw():
    # joueur pioche
    print("Vous piochez une carte...")
    card = draw_card()
    mainJoueur.append(card)
    print(f"Vous avez {card.rank} de {card.suit}")
    # check win
    result = check_win_status()
    if result == WinStatus.PLAYER_21:
        win_21()
        return
    elif result == WinStatus.PLAYER_OVER_21:
        loss_plus_21()
        return
    # ordi pioche si il veux
    ordi_draw()

def play_stop():
    print("Vous arrêtez de piocher.")
    global playerDrawing
    playerDrawing = False
    if not ordiDrawing: # ordi ne piochait pas - fin de partie
        print("L'ordi ne piochait pas non plus.")
        conventional_stop()
        return
    # ordi draws till it not
    while ordiDrawing:
        ordi_draw()

def tour():
    # check in no cards
    if cards_left() == 0:
        no_cards_left()
        return
    print(f"Votre main vaut {somme_points(mainJoueur)}")
    print("Faites 'ACTION' pour vos actions")
    # get action
    action = input()
    if not action.upper() in commands: # command not recognized
        print("Nous n'avons pas compris...")
        print()
        tour() # rerun tour
    # EXEC ACTION
    match action.upper():
        case "ACTION": # rewrite actions available
            play_actions()
            tour()
        case "MAIN": # simple handshake : we send some messages then we to this back
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
    play_actions()
    print()

    # draw 2 cartes pour joueur
    print("Vous piochez deux cartes...")
    joueur1 = draw_card()
    joueur2 = draw_card()
    print(f"Vous avez pioché {joueur1.rank} de {joueur1.suit}")
    print(f"Vous avez pioché {joueur2.rank} de {joueur2.suit}")
    mainJoueur.append(joueur1)
    mainJoueur.append(joueur2)
    if check_win_status() == WinStatus.PLAYER_21: # first check : player gets insta 21
        win_early_21()
        return

    # draw 2 cartes ordi
    print("L'ordinateur pioche deux cartes...")
    mainOrdi.append(draw_card())
    mainOrdi.append(draw_card())
    if check_win_status() == WinStatus.ORDI_21: # second check : ordi gets insta 21
        loss_early_21()
        return

    # enter main game loop
    tour()

def win_early_21():
    print("Vous avez obtenu 21 sur votre premier tour !")
    print("Vous avez gagné cette partie!")
    recap()
def loss_early_21():
    print("L'ordinateur à eu 21 sur sont premier tour !")
    print("Vous avez perdu...")
    recap()
def loss_21():
    print("L'ordinateur à atteint 21 !")
    print("Vous avez perdu...")
    recap()
def win_21():
    print("Vous avez atteint 21 !")
    print("Vous avez gagné cette partie!")
    recap()
def win_plus_21():
    print("L'ordinateur à dépassé 21, vous avez donc gagné !")
    recap()
def loss_plus_21():
    print("Vous avez dépassé 21 et avez donc perdu...")
    recap()
def no_cards_left():
    print("Il ne reste plus de cartes dans la pioche.")
    conventional_stop()
def conventional_stop():
    result = check_win_status(stopped=True)
    match result:
        case WinStatus.PLAYER_21:
            win_21()
        case WinStatus.ORDI_21:
            loss_21()
        case WinStatus.PLAYER_OVER_21:
            loss_plus_21()
        case WinStatus.ORDI_OVER_21:
            win_plus_21()
        case WinStatus.PLAYER_HIGHER:
            print("Vous avez plus de points de l'ordi !")
            print("Vous avez gagné !")
            recap()
        case WinStatus.ORDI_HIGHER:
            print("Vous avez moins de points de l'ordi !")
            print("Vous avez perdu...")
            recap()
        case WinStatus.EQUALS:
            print("Égalité !")
            recap()

def recap():
    print()
    print(f"Votre main, avec {somme_points(mainJoueur)} points :")
    for card in mainJoueur:
        print(f" - {card.rank} de {card.suit}")
    print(f"Main de l'ordi, avec {somme_points(mainOrdi)} points :")
    for card in mainOrdi:
        print(f" - {card.rank} de {card.suit}")

main()