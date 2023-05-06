from abb import Robot
    
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
