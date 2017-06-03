__author__ = 'philippe'
from Tkinter import *
master = Tk()

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight() - 100

(x, y) = (5, 5)
Width = min(screen_width, screen_height) / max(x,y)
Height = Width
Width *= 1.8

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width*2, height=y*Width)
player = (0, y-1)
score = 1
restart = False
walk_reward = -0.04

walls = [(1, 1), (1, 2), (2, 1), (2, 2)]
specials = [(4, 1, "red", -1), (4, 0, "green", 1)]
cell_scores = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Height,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Height,
                                    (i+0.5)*Width, j*Height,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Height,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Height,
                                    (i+0.5)*Width, (j+1)*Height,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Height,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Height,
                                    i*Width, (j+0.5)*Height,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Height,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Height,
                                    (i+1)*Width, (j+0.5)*Height,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Height, (i+1)*Width, (j+1)*Height, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)

            temp['label'] = StringVar()
            Label(board, textvariable=temp['label']).place(x = i*Width+10,y = j*Height+40)
            
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Height, (i+1)*Width, (j+1)*Height, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Height, (i+1)*Width, (j+1)*Height, fill="black", width=1)

render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    cell = cell_scores[state]
    triangle = cell[action]
    label = cell['label']
    label.set(str(val)[:10])
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Height+Height*2/10, new_x*Width+Width*8/10, new_y*Height+Height*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print "Success! score: ", score
            else:
                print "Fail! score: ", score
            restart = True
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = (0, y-1)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Height+Height*2/10, player[0]*Width+Width*8/10, player[1]*Height+Height*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Height+Height*2/10,
                            player[0]*Width+Width*8/10, player[1]*Height+Height*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
