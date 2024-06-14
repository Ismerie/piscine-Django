import random
from beverages import HotBeverage, Coffee, Tea, Cappuccino, Chocolate

class CoffeeMachine:
    class EmptyCup(HotBeverage):
        def __init__(self):
            self.name = "empty cup"
            self.price = 0.90
        
        def description(self):
            return "An empty cup?! Gimme my money back!"
    
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.drink_count = 10

    def repair(self):
        self.drink_count = 10
    
    def serve(self, drink: HotBeverage):
        if (self.drink_count <= 0):
            raise CoffeeMachine.BrokenMachineException
        self.drink_count -= 1
        if random.randint(0, 1) == 1:
            return CoffeeMachine.EmptyCup()
        return drink()

def test():
    coffeeMachine = CoffeeMachine()
    while True:
        try:
            print(coffeeMachine.serve(random.choice(
                [Coffee, Tea, Cappuccino, Chocolate, HotBeverage])))
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            print("\n---- method repair called ----\n")
            coffeeMachine.repair()
            break
    
    while True:
        try:
            print(coffeeMachine.serve(random.choice(
                [Coffee, Tea, Cappuccino, Chocolate, HotBeverage])))
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            print("\n---- method repair called ----\n")
            coffeeMachine.repair()
            break
        

if __name__ == '__main__':
    test()