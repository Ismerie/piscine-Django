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
    capital = states.get(to_find)
    print(capital_cities.get(capital, "Unknown state"))

def init_var():
    arguments = sys.argv
    
    if len(arguments) == 2:
        find_value(arguments[1])
    
if __name__ == '__main__':
    init_var()