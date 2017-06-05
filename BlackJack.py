# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
dealer_outcome = ""
player_outcome = "Hit or Stand?"
score = 0
cover = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

in_play = False
outcome = ""

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.cards_in_hand = []

    def __str__(self):
        s = "Hand contains "
        for card in self.cards_in_hand:
            s += card.suit + card.rank + " "
        return s
            
    def add_card(self, card):
        self.cards_in_hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for card in self.cards_in_hand:
            value += VALUES[card.rank]
        
        for card in self.cards_in_hand:
            if card.rank == 'A' and value + 10 <= 21:
                value += 10
            
        return value  
        
    def draw(self, canvas, pos):
        visible = self.cards_in_hand[:5]
        i = 0
        offset = 40
        for card in visible:
            card.draw(canvas, [pos[0] + i * 72 + offset, pos[1]])
            i += 1
       
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards_in_deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards_in_deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards_in_deck)

    def deal_card(self):
        # deal a card object from the deck
        idx = random.randrange(0, len(self.cards_in_deck))
        dealt_card = self.cards_in_deck[idx]
        self.cards_in_deck.pop(idx)
        return dealt_card
    
    def __str__(self):
        s = "deck contains "
        for card in self.cards_in_deck:
            s += card.suit + card.rank + " "   
        return s
    
deck = Deck()
player = Hand()
dealer = Hand()
    
#define event handlers for buttons
def deal():
    global player_outcome, dealer_outcome, in_play
    global deck, player, dealer, cover
    
    deck = Deck()
    player = Hand()
    dealer = Hand()
    deck.shuffle()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    player_outcome = "Hit or Stand?"
    dealer_outcome = ""
    
    # your code goes here
    in_play = True
    cover = True

def hit():
    # replace with your code below
    global in_play, player, deck, score
    global player_outcome, dealer_outcome, cover
    # if the hand is in play, hit the player
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        player_outcome = "You busted!"
        dealer_outcome = "You win!"
        in_play = False
        score -= 1
        cover = False
       
def stand():
    # replace with your code below
    global in_play, dealer, deck, dealer_outcome, score, player_outcome, cover
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
    if dealer.get_value() > 21:
        dealer_outcome = "Dealer busted!"
        player_outcome = "You win!"
        score += 1
        cover = False
        
    else:
        if dealer.get_value() >= player.get_value():
            dealer_outcome = "You win!"
            player_outcome = "You Lose!"
            score -= 1
        else:
            player_outcome = "You win!"
            dealer_outcome = "You Lose!"
            score += 1
        
    in_play = False
    cover = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player, dealer, player_outcome, dealer_outcome, score
    global cover
    canvas.draw_text('BlackJack', [50, 50], 40, 'Red')
    canvas.draw_text('Dealer', [50, 100], 20, 'Black')
    canvas.draw_text("Score: " + str(score), [300, 100], 20, 'Black')
    canvas.draw_text(dealer_outcome, [120, 100], 20, 'Black')
    canvas.draw_text('Player', [50, 300], 20, 'Black')
    canvas.draw_text(player_outcome, [130, 300], 20, 'Black')
    dealer.draw(canvas, [50, 150])
    player.draw(canvas, [50, 350])
    if cover:
        # Draw the hole card
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                         [90 + CARD_CENTER[0], 150 + CARD_CENTER[1]], CARD_SIZE)
        
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric