# implementation of card game - Memory

import simplegui
import random

# List of numbers on cards
numbers = list(range(8)) * 2
random.shuffle(numbers)

# The state of each card
exposed = [False for i in range(16)]

# Number of clicks that have been applied now
exp_card_num = 0
exp_cards = []

# Consts
CARD_WIDTH = 50
CARD_HEIGHT = 100

# Count of clicks
turns = 2

# helper function to initialize globals
def new_game():
    global exposed, exp_card_num, exp_cards, numbers, turns
    global label
    random.shuffle(numbers)
    exposed = [False for i in range(16)]
    exp_card_num = 0
    exp_cards = []
    turns = 0
    label.set_text('Turns = 0')
    
# define event handlers
def mouseclick(pos):
    global exp_card_num, exposed, exp_cards
    global turns, label
    idx = pos[0] / CARD_WIDTH
    if exposed[idx]:
        return
    
    turns += 1
    label.set_text('Turns = ' + str(turns / 2))
    
    if exp_card_num <= 1:
        exposed[idx] = True
        exp_card_num += 1
        exp_cards.append(idx)
    else:
        if numbers[exp_cards[0]] <> numbers[exp_cards[1]]:
            exposed[exp_cards[0]] = False
            exposed[exp_cards[1]] = False
        exp_cards = [idx]
        exp_card_num = 1
        exposed[idx] = True
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    offset = list(range(16))
    for i in offset:
        if exposed[i]:
            canvas.draw_text(str(numbers[i]), 
                             (i * 50 + 10, 70), 60, 
                             'White')
        else :
            canvas.draw_polygon([(i * 50, 0),
                                 (i * 50, 100),
                                 (i * 50 + 50, 100),
                                 (i * 50 + 50, 0)],
                                4,
                                'Black',
                                'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric