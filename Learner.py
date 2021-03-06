__author__ = 'philippe'
import World
import threading
import time

discount = 0.9
actions = World.actions
states = []
Q = {}
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2

prevAct = None

def getOpp(side):
    if side == 'up':
        return 'down'
    if side == 'down':
        return 'up'
    if side == 'right':
        return 'left'
    if side == 'left':
        return 'right'

def max_Q(s):
    #print 's:', s
    x,y = s
    
    #global prevAct
    #prevOppAct = getOpp(prevAct)
    val = None
    act = None
    for a, q in Q[s].items():
        #print 'looping, x=', x, 'a=', a
        #if(x==0 and a=='left'):
        #    continue
        #if(x==9 and a=='right'):
        #    continue
        #if(y==0 and a=='up'):
        #    continue
        #if(y==9 and a=='down'):
        #    continue
        #print 'inside'
        #if prevAct is None or prevOppAct != a:
        if val is None or (q > val): # or (q == val and a == prevAct):
            val = q
            act = a

    #print 'decided to go:', act, 'reward: ', val
    #prevAct = act
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    while True:
        # Pick the right action
        s = World.player
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.1)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
