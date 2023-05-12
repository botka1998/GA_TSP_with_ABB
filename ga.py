from main import SEGMENTS_LIST, HOME, MUTATION_PROBABILITY
import json
import random

class Generation():
    def __init__(self) -> None:
        pass



class Chromosome():
    def __init__(self) -> None:
       
        self.route = SEGMENTS_LIST
        random.shuffle(self.route)
        self.route = HOME + self.route + HOME
        # print(json.dumps(self.route, indent=2))
    def mutate(self):
        if random.random() < MUTATION_PROBABILITY:
            line_idx = [idx for idx, item in enumerate(self.route) if item[0].split('_')[0] == 'linija']
            for i in line_idx:
                print(self.route[i])

            seg = random.sample(self.route[1:-1], 1)

            # menjamo direction
            pass
        if random.random() < MUTATION_PROBABILITY:
            # menjamo sequence
            pass




if __name__ == '__main__':
    Chromosome().mutate()
    