def idk(a):
    for i in a:
        o = 'Yes'
        for n in range(len(i)-2):
            if i[n] < i[n+1] > i[n+2]:
                o = 'No'
        print(o)

a=[]
t = int(input())
for i in range(t):
    b = int(input())
    a.append(list(map(int, input().split())))
idk(a)
