def my_var():
   varInt = 42
   varStr = "42"
   varStr2 = "quarante-deux"
   varFloat = 42.0
   varBool = True
   varList = [42]
   varDict = {42: 42}
   varTuple = (42,)
   varSet = set()

   liste = [varInt, varStr, varStr2, varFloat, varBool, varList, varDict, varTuple, varSet]

   for element in liste:
        print(f"{element} est de type {type(element)}")

if __name__ == '__main__':
    my_var()