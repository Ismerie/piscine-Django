import sys

def find_value(to_find):
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
    if to_find in list(capital_cities.values()):
        capital = list(capital_cities.keys())[list(capital_cities.values()).index(to_find)]
        state = list(states.keys())[list(states.values()).index(capital)]
        print(state)
    else:
        print("Unknown capital city")

def init_var():
    arguments = sys.argv
    
    if len(arguments) == 2:
        find_value(arguments[1])
    
if __name__ == '__main__':
    init_var()