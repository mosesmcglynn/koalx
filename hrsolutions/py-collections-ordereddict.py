from collections import OrderedDict

hmtimes = int(input())
ordDict = OrderedDict()
for i in range(hmtimes):
    items = input().split()
    price = int(items.pop())
    items = ' '.join(items)
    if items not in ordDict:
        ordDict[items] = price
    else:
        ordDict[items] += price
for keys, values in ordDict.items():
    print(f'{keys} {values}')