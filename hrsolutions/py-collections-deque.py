from collections import deque

a = int(input())
b = deque()
for i in range(a):
    c = input().split()
    match c[0]:
        case 'append':
            b.append(int(c[1]))
        case 'appendleft':
            b.appendleft(int(c[1]))
        case 'pop':
            b.pop()
        case 'popleft':
            b.popleft()
for i in b:
    print(i, end=' ')
