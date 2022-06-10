from global_state import Global_State
from gameplay.main_loop import run_game
from app.main_loop import run_app


def main():
    while True:
        if Global_State.APP == 'APP':
            run_app()
        elif Global_State.APP == 'GAME':
            run_game()
        else:
            print(f"can't go to {Global_State.APP}")
            break


if __name__ == '__main__':
    main()
