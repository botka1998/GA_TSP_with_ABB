import copy
import random
import numpy as np
from abb import Robot
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.patches as patch

GENERATION_NUM = 300
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.8
BEST_NUM = 20
SEGMENTS = {
    "krug_20":{
        "targets":[[90,125 - 10,50],[90,125 - 10,50]],
        "direction": 0,
        },
    "krug_25":{
        "targets":[[97,193 - 12.5,50],[97,193 - 12.5,50]],
        "direction": 0,  
        },
    "krug_30":{
        "targets":[[200,165 - 15,50],[200,165 - 15,50]],
        "direction": 0,  
        },
    "krug_33":{
        "targets":[[14000,155 - 16.5,50],[140,155 - 16.5,50]], ###############
        "direction": 0,  
        },
    "kvadrat_10":{
        "targets":[[105 - 5,160 - 5,50],[105 - 5,160 - 5,50]],
        "direction": 0,  
        },
    "kvadrat_14":{
        "targets":[[173 - 7,125 - 7,50],[173 - 7,125 - 7,50]],
        "direction": 0,  
        },
    "kvadrat_18":{
        "targets":[[171 - 9,204 - 9,50],[171 - 9,204 - 9,50]],
        "direction": 0,  
        },
    "linija_0":{
        "targets":[[225,75,50],[225,225,50]],
        "direction": 0,  
        },
    "linija_1":{
        "targets":[[225,225,50],[75,225,50]],
        "direction": 0,  
        },
    "linija_2":{
        "targets":[[75,225,50],[75,75,50]],
        "direction": 0,  
        },
    "linija_3":{
        "targets":[[75,75,50],[225,75,50]],
        "direction": 0,  
        },
}

HOME = [("home", {
        "targets":[[150,286.832013798,623],[150,286.832013798,623]],
        "direction": 0,  
    })]
segment_list = list(SEGMENTS.items())


def init_rob():
    # Inicijalizacija robota
    robot = Robot(ip="127.0.0.1", port_motion=5000)
    robot.set_joints([0, 0, 0, 0, 30, 0])
    # for i in [0,1,2,3,10,14,18,20,25,30,33]:
    #     print(i)
    #     if i < 10:
    #         robot.do_path(i, 0)
    #     else:
    #         robot.do_path(i)
    robot.set_joints([0, 0, 0, 0, 30, 0])
    robot.set_workobject([[300,150,10],[0.707106781,0,0,-0.707106781]])
    robot.set_tool([[0,0,93],[0.707107,0,-0.707107,0]])
    robot.set_speed(speed=[400, 200, 200, 200])
    return robot
class Chromosome():
    def __init__(self):
       
        self.route = segment_list
        random.shuffle(self.route)
        self.route = HOME + self.route + HOME
        # print(json.dumps(self.route, indent=2))

    # def copy(self):
    #     cpy = Chromosome()
    #     cpy.route = self.route.copy()
    #     return cpy
    
    def __copy__(self):
        cpy = Chromosome()
        cpy.route = copy.deepcopy(self.route)
        return cpy

    def mutate(self):
        if random.random() < MUTATION_PROBABILITY:
            # menjamo direction
            line_idx = [idx for idx, item in enumerate(self.route) if item[0].split('_')[0] == 'linija']
            index = random.sample(line_idx, 1)[0]
            self.route[index][-1]['direction'] = 1 - self.route[index][-1]['direction']
            self.route[index][-1]['targets'].reverse()
            # print(self.route[index])
            # seg = random.sample(self.route[1:-1], 1)
        if random.random() < MUTATION_PROBABILITY:
            # menjamo sequence
            idx_1, idx_2 = random.sample(range(1, len(self.route) - 1), 2)
            temp = self.route[idx_1]
            self.route[idx_1] = self.route[idx_2]
            self.route[idx_2] = temp
            # for i in self.route:
            #     print(i)
        return self
    
    def path_len(self):
        sum = 0
        for idx in range(len(self.route)-1):
            start = np.array(self.route[idx][1]['targets'][1])
            end = np.array(self.route[idx +1][1]['targets'][0])
            distance = np.linalg.norm(end - start)
            sum += distance
        # for i in self.route:
        #     print(i)
        # print(sum)
        return sum
class Generation():
    def __init__(self):
        self.chromosomes = []
        for i in range(POPULATION_SIZE):
            self.chromosomes.append(Chromosome().mutate())
    def get_best(self):
        best = []
        lengths = []
        for chromosome in self.chromosomes:
            lengths.append(chromosome.path_len())
        lengths = np.asarray(lengths)
        best_indexes = np.argsort(lengths)[:BEST_NUM]
        for index in best_indexes:
            best.append(self.chromosomes[index].__copy__())
        return best

    def crossover(self, parent_1, parent_2):
        index = random.sample(range(1, len(parent_1.route) - 1), 1)[0]
        child = Chromosome()
        child.route = copy.deepcopy(parent_1.route[:index])
        for target in parent_2.route:
            if not target in child.route:
                child.route.append(target)
        child.route.append(child.route[0])
        return child
    
    def evolve(self):
        best = self.get_best()
        self.chromosomes = []
        self.chromosomes.append(best[0])
        while len(self.chromosomes) < POPULATION_SIZE:
            parent_1, parent_2 = random.sample(best, 2)
            child = self.crossover(parent_1, parent_2)
            self.chromosomes.append(child.mutate())


def Visualization(best):
    annot = 0
    for i in range(len(best.route) - 1):
        start, end = best.route[i][1]['targets']
        if "linija" in best.route[i][0]:
            plt.scatter(start[0], start[1])
            # plt.annotate(i, (start[0], start[1]))
            plt.scatter(end[0], end[1])
            # plt.annotate(i, (start[0], start[1]))
            plt.plot((start[0], end[0]), (start[1], end[1]))
            plt.annotate(annot, ((start[0] + (end[0] - start[0])/2), (start[1] + (end[1] - start[1])/2)))
            annot += 1

            if not "linija" in best.route[i+1][0]:
                start, end = best.route[i][1]['targets'][1], best.route[i+1][1]['targets'][0] 
                plt.plot((start[0], end[0]), (start[1], end[1]))
                plt.annotate(annot, ((start[0] + (end[0] - start[0])/2), (start[1] + (end[1] - start[1])/2)))
                annot += 1
        else:
            plt.scatter(start[0], start[1])
            if "kvadrat" in best.route[i][0]:
                size = float(best.route[i][0].split('_')[-1])
                rect = patch.Rectangle((start[0], start[1]), size, size)
                rect.set(fill=False)
                plt.gca().add_patch(rect)
            elif "krug" in best.route[i][0]:
                size = float(best.route[i][0].split('_')[-1])
                circle = plt.Circle((start[0], start[1] + size/2), size/2)
                circle.set(fill=False)
                plt.gca().add_patch(circle)
            start, end = best.route[i][1]['targets'][1], best.route[i+1][1]['targets'][0] 
            plt.plot((start[0], end[0]), (start[1], end[1]))
            plt.annotate(annot, ((start[0] + (end[0] - start[0])/2), (start[1] + (end[1] - start[1])/2)))
            annot += 1

    plt.show()
        # start, end = best.route[i][1]['targets']
        # plt.scatter(start[0], start[1])
        # plt.plot(best_path[i][0],best_path[i+1][0],best_path[i][1],best_path[i+1][1])



if __name__ == '__main__':
    robot = init_rob()
    unreachable_targets = []
    for target in segment_list:
        if not "home" in target[0]:
            is_reachable_1 = robot.check_target(target=[target[1]["targets"][0],[0.5,-0.5,0.5,0.5]])
            is_reachable_2 = robot.check_target(target=[target[1]["targets"][1],[0.5,-0.5,0.5,0.5]])
            if not is_reachable_1 or not is_reachable_2:
                unreachable_targets.append(target)
    for target in unreachable_targets:
        segment_list.remove(target)
    print(len(unreachable_targets))
    print(len(segment_list))
    gen = Generation()
    best = Chromosome()
    best.route = copy.deepcopy(gen.get_best()[0].route)
    for target in best.route:
        print(target)
    print(best.path_len())
    best_len = []
    
    for i in tqdm(range(GENERATION_NUM)):
        best_len.append(best.path_len())
        gen.evolve()
        if gen.get_best()[0].path_len() < best.path_len():
            best.route = copy.deepcopy(gen.get_best()[0].route)

    for target in best.route:
        print(target)
    print(best.path_len())

    plt.plot(range(len(best_len)), best_len)
    plt.show()
    Visualization(best)
    for target in best.route:
        if "linija" in target[0]:
            robot.do_path(target[0].split("_")[-1],target[1]["direction"])      
        elif not "home" in target[0]:
            robot.do_path(target[0].split("_")[-1])      
    robot.set_joints([0, 0, 0, 0, 30, 0])



