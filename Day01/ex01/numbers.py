def parse_file():
    with open("numbers.txt", "r") as file:
        lines = file.readlines()
    file.close()

    for caractere in lines[0]:
        if caractere.isdigit():
            print(caractere, end="")
        elif caractere == ",":
            print()

if __name__ == '__main__':
    parse_file()