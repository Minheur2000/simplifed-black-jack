import random

colors = ["pique", "trefle", "carreau", "coeur"]
nums = ["AS", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
tetes = ["J", "Q", "K"]

cartesJoueur = []
cartesOrdi = []

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

mainJoueur = []
mainOrdi = []

def carte_exists(card: Card):
    for c in mainJoueur:
        if c.suit == card.suit and c.rank == card.rank:
            return True
    for c in mainOrdi:
        if c.suit == card.suit and c.rank == card.rank:
            return True
    return False

def point_pour_card(card):
    if card.rank == "AS":
        return 11
    elif card.rank in tetes:
        return 10
    else:
        return card.rank

def somme_points(joueur):
    as_amount = 0
    points = 0
    for card in joueur:
        if card.rank == "AS":
            as_amount += 1
        else:
            points += point_pour_card(card)
    for i in range(as_amount):
        if (points + 11) > 21:
            points += 1
        else:
            points += 11
    return points

def draw_card():
    card = Card(suit=random.choice(colors), rank=random.choice(nums))
    while carte_exists(card):
        card = Card(suit=random.choice(colors), rank=random.choice(nums))
    return card

def tour():
    print(f"Votre main vaut {somme_points(mainJoueur)}")

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

    # enter main game loop
    tour()

main()