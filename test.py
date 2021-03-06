from pynput.keyboard import Key
import numpy as np
import threading
import time

from utils.player import Player
from utils.keyboard import Keyboard
from utils.reader import Reader


# env vars
orbDist = None

# screen reader
reader = Reader()

reader.showWindow = False
reader.printDebug = False

reader.selectMonitor(2)
reader.calibrate()
readingThread = threading.Thread(target=reader.start)

# player
player = Player('./out/nnconf_24:08:2021:04:13:18_ep1000.json')

# keyboard controller
controller = Keyboard({
    0: 'w',
    1: 's',
    2: 'a',
    3: 'd',
    4: Key.space,
})


def main():
    # variable binding
    global agent, orbPos, readingThread

    readingThread.start()

    # print ready up prompt
    print('move your cursor to window')
    time.sleep(1)
    print('game starts in\n3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')

    # start
    controller.apply(4)
    state, orbDist, newOrb, gameover = reader.getState()

    plays = 0
    tScore = 0
    while plays < 20:
        tempState, newOrbDist, newOrb, gameover = reader.getState()
        # reset if gameover
        if gameover:
            plays += 1            

            time.sleep(0.5)
            controller.apply(4)
            time.sleep(0.1)
            state, orbDist, newOrb, gameover = reader.getState()

        # step controller
        elif not np.array_equal(state, tempState) or orbDist != newOrbDist:
            state = tempState
            orbDist = newOrbDist

            if newOrb:
                tScore += 1

            action = player.getAction(state)
            controller.apply(action)

    print('avg score in 20 plays: {}'.format(tScore / 20))

if __name__ == "__main__":
    main()
