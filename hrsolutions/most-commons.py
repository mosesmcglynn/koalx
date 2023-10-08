def cl(a):
    b = {}
    for i in a:
        if i not in b:
            b[i] = 1
        else:
            b[i] += 1
    sb = sorted(b.items(), key=lambda x: (-x[1], x[0]))[:3]

    for i in range(3):
        print(' '.join(list(map(str, sb[i]))))

if __name__ == '__main__':
    s = input()
    cl(s)
