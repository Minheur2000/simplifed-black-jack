colors = ["pique", "trefle", "carreau", "coeur"]
nums = ["AS", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
tetes = ["J", "Q", "K"]

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

mainJoueur = []
mainOrdi = []

def point_pour_card(card):
    if card.rank == "AS":
        return 11
    elif tetes.__contains__(card.rank):
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


def main():
    print("Bienvenu dans BlackJack!")
    print("Utilisez [Entrée] pour lancer le jeu")
    print()
    input()

main()