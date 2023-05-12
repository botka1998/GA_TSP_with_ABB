from abb import Robot

GENERATION_NUM = 500
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.6
BEST_NUM = 20
SEGMENTS = {
    "krug_20":{
        "targets":[[90,125,50],[90,125,50]],
        "direction": 0,
        },
    "krug_25":{
        "targets":[[97,193,50],[97,193,50]],
        "direction": 0,  
        },
    "krug_30":{
        "targets":[[200,165,50],[200,165,50]],
        "direction": 0,  
        },
    "krug_33":{
        "targets":[[140,155,50],[140,155,50]],
        "direction": 0,  
        },
    "kvadrat_10":{
        "targets":[[105,160,50],[105,160,50]],
        "direction": 0,  
        },
    "kvadrat_14":{
        "targets":[[173,125,50],[173,125,50]],
        "direction": 0,  
        },
    "kvadrat_18":{
        "targets":[[171,204,50],[171,204,50]],
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

HOME = [("home_666", {
        "targets":[[150,286.832013798,623],[150,286.832013798,623]],
        "direction": 0,  
    })]
SEGMENTS_LIST = list(SEGMENTS.items())


if __name__ == '__main__':

    # Inicijalizacija robota
    robot = Robot(ip="127.0.0.1", port_motion=5000)
    robot.set_joints([0, 0, 0, 0, 30, 0])
    for i in [0,1,2,3,10,14,18,20,25,30,33]:
        print(i)
        if i < 10:
            robot.do_path(i, 0)
        else:
            robot.do_path(i)
    robot.set_joints([0, 0, 0, 0, 30, 0])
