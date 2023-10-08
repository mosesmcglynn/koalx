from collections import namedtuple

loop = int(input())
a = list(input().split())
student = namedtuple('Student', a)
s = []
total = 0
for i in range(loop):
    s = student(*(input().split()))
    total += int(s.MARKS)
print(f'{total / loop:.2f}')
