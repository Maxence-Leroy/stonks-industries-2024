from src.robot.robot import robot
from src.replay.save_replay import open_replay_file, start_replay

def main():
    p_pos = 0
    p_rot = 0
    i_pos = 0
    i_rot = 0
    d_pos = 0
    d_rot = 0
    while True:
        user_input = input()
        if user_input.startswith("P_POS"):
            p_pos = float(user_input[6:])
            robot.stepper_motors.write(f"PID P_POS {str(p_pos)}")
        elif user_input.startswith("P_ROT"):
            p_rot = float(user_input[6:])
            robot.stepper_motors.write(f"PID P_ROT {str(p_rot)}")
        elif user_input.startswith("D_POS"):
            d_pos = float(user_input[6:])
            robot.stepper_motors.write(f"PID D_POS {str(d_pos)}")
        elif user_input.startswith("D_ROT"):
            d_rot = float(user_input[6:])
            robot.stepper_motors.write(f"PID D_ROT {str(d_rot)}")
        elif user_input.startswith("I_POS"):
            i_pos = float(user_input[6:])
            robot.stepper_motors.write(f"PID I_POS {str(i_pos)}")
        elif user_input.startswith("I_ROT"):
            i_rot = float(user_input[6:])
            robot.stepper_motors.write(f"PID I_ROT {str(i_rot)}")
        elif user_input == "POS":
            open_replay_file(f"POSPP{p_pos}PR{p_rot}IP{i_pos}IR{i_rot}DP{d_pos}DR{d_rot}")
            start_replay()
            robot.stepper_motors.write("HS POS")
        elif user_input == "ROT":
            open_replay_file(f"ROTPP{p_pos}PR{p_rot}IP{i_pos}IR{i_rot}DP{d_pos}DR{d_rot}")
            start_replay()
            robot.stepper_motors.write("HS ROT")
        else:
            raise ValueError()

if __name__ == "__main__":
    main()