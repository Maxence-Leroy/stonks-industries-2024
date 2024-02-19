from src.robot import robot

if __name__ == "__main__":
    res = ""
    while res != "q":
        res = input()
        if res == "on":
            robot.magnet.switch_on()
        elif res == "off":
            robot.magnet.switch_off()
