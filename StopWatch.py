# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
success = 0
total = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tens_second = t % 10
    seconds = (t / 10) % 60
    minutes = (t / 10) / 60
    
    if seconds < 10 :
        return str(minutes) + ":0" + str(seconds) + "." + str(tens_second)
        
    return str(minutes) + ":" + str(seconds) + "." + str(tens_second)
   
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    if not timer.is_running():
        timer.start()
    
def stop():
    global time, success, total
    if timer.is_running():
        timer.stop()
        total = total + 1    
        if time % 10 == 0:
            success = success + 1
 
def reset():
    global time, success, total
    timer.stop()
    time = 0
    success = 0
    total = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time = time + 1
    
# define draw handler
def draw_handler(canvas):
    global time, success, total
    canvas.draw_text(format(time), (70, 110), 20, 'White')
    canvas.draw_text(str(success) + '/' + str(total), (160, 20), 20, 'Red')
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.add_button('Start', start, 50)
frame.add_button('Stop', stop, 50)
frame.add_button('Reset', reset, 50)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
