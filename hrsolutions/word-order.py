a = int(input())
b = {}
for i in range(a):
    word = input()
    if word not in b:
        b[word] = 1
    else:
        b[word] += 1
print(len(b.keys()))
for values in b.values():
    print(f'{values}', end=' ')
