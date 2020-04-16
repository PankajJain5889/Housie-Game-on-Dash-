import numpy as np
import random
rows = 6
columns = 9
class playerCard:
    def __init__(self, name):
        self.name  = name 
        self.ticket = np.zeros((rows , columns))
        self.rows = rows
        self.columns = columns
        self.fill_ticket()
    def fill_ticket(self):
        count =0
        buffer = []
        for x in range(rows):
            for y in range(columns):
                if count>30:
                    break
                if bool(random.getrandbits(1)):
                    next_number = np.random.randint(0,100)
                    while next_number in buffer:
                        next_number = np.random.randint(0,100)
                    buffer.append(next_number)
                    self.ticket[x][y] = next_number
                    count+=1
                else:
                    self.ticket[x][y] = -1
