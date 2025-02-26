# Dependencies
# - readchar

import readchar


def menu(options: list[str]) -> str:
    current_index = 0

    def print_menu():
        for i, option in enumerate(options):
            if i == current_index:
                print(f"\033[7m {option} \033[0m")
            else:
                print(f" {option} ")

    print_menu()

    while True:
        key = readchar.readkey()

        if key == readchar.key.UP and current_index > 0:
            current_index -= 1
        elif key == readchar.key.DOWN and current_index < len(options) - 1:
            current_index += 1
        elif key == readchar.key.ENTER:
            print("\033[F" * len(options), end="")
            print("\033[J", end="")
            return options[current_index]

        print("\033[F" * len(options), end="")
        print_menu()
