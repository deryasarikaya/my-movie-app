from colors import RESET, RED



def get_valid_float(prompt):

    while True:
        try:
            return float(input(prompt))

        except ValueError:
            print(f"{RED}Please enter a valid rating number.{RESET}")


def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print(f"{RED}Please enter a valid year number.{RESET}")


def get_valid_text(prompt):
    while True:
        text = input(prompt).strip()

        if text == "":
            print(f"{RED}Movie title cannot be empty.{RESET}")
        else:
            return text