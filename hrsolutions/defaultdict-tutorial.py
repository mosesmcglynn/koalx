from collections import defaultdict

groups = input().split()
default_dict = defaultdict(list)
letters = []
for i in range(len(groups)):
    for n in range(int(groups[i])):
        letter = input()
        if i == 0:
            default_dict[letter].append(n+1)
        else:
            letters.append(letter)
for i in letters:
    if i not in default_dict:
        print('-1')
    else:
        print(*default_dict[i])
