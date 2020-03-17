# 1- Random function
import random


def choose_first():
    if random.randint(0, 1) == 0:
        return 'Player 1'
    else:
        return 'Player 2'


choose = choose_first()
print('the will start', choose)
# 2- clear output
from IPython.display import clear_output

clear_output()
print('osama')
clear_output()
clear_output()
clear_output()
