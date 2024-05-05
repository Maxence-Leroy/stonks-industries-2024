from src.robot.robot import robot

if __name__ == "__main__":
    magnets = [robot.magnet1, robot.magnet2, robot.magnet3]
    res = ""
    while res != "q":
        res = input()
        if res == "on":
            for magnet in magnets:
                magnet.switch_on()
        elif res == "off":
            for magnet in magnets:
                magnet.switch_off()
