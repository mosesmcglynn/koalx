from collections import Counter

a = int(input())
b = Counter(input().split())
c = int(input())
total = 0
for i in range(c):
    d = input().split()
    if b[d[0]] == 0:
        continue
    else:
        b[d[0]] -= 1
        total += int(d[1])
print(total)
