from display import Display
from game import Game


def main():
    while True:
        Display.print_welcome()
        choice = Display.print_menu()
        
        if choice == 'q':
            Display.clear_screen()
            break
        elif choice == '1':
            game = Game(vs_computer=False)
            if not game.play():
                continue
        elif choice == '2':
            game = Game(vs_computer=True)
            if not game.play():
                continue
        else:
            continue
        
        play_again = Display.print_play_again()
        if play_again != 'y':
            Display.clear_screen()
            break


if __name__ == "__main__":
    main()
