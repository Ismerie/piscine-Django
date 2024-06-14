import sys

def is_state(state, initial, capital_cities):
    for key, value in capital_cities.items():
        if initial == key:
            print(f"{value} is the capital of {state}")

def is_capital(initial, capital, states):
    for key, value in states.items():
        if initial == value:
            print(f"{capital} is the capital of {key}")

def resolve_list(liste, states, capital_cities):
    find = False

    for element in liste:
        for key, value in states.items():
            if element.lower() == key.lower():
                is_state(key, value, capital_cities)
                find = True
        for key, value in capital_cities.items():
            if element.lower() == value.lower():
                is_capital(key, value, states)
                find = True
        if find == False and element != '':
            print(f"{element} is neither a capital city nor a state")
        else:
            find = False
            

def parse_arg(arg):
    if arg.find(",,") != -1:
        return

    liste = arg.split(",")
    liste_clear = []
    
    for element in liste:
        liste_clear.append(element.strip())
    return liste_clear
    

def main():
    arguments = sys.argv
    liste = []
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    
    if len(arguments) != 2:
        return
    liste = parse_arg(arguments[1])
    resolve_list(liste, states, capital_cities)


if __name__ == '__main__':
    main()