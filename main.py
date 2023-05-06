from abb import Robot
    
if __name__ == '__main__':

    # Inicijalizacija robota
    robot = Robot(ip="127.0.0.1", port_motion=5000)
    robot.set_joints([0, 0, 0, 0, 30, 0])