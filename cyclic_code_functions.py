import random
import pandas
import matplotlib.pyplot as plt
import numpy as np

# g(x) - generator polynomial
#l - length of the encoded sequence
#e - accuracy of probability estimate

def mod2(polynom):
    for i in range(len(polynom)):
        polynom[i] = polynom[i] % 2
    return polynom


def count_d(p1, p2):
    d = 0
    for i in range(get_degree(p1)):
        if p1 != p2:
            ++d
    return d


def count_min_d(words):
    min = 1000
    for i in range(len(words)):
        for k in range(len(words)):
            if (k == i):
                continue
            d = count_d(words[i], words[k])
            if (d < min_d):
                min_d = d
    return min_d


def get_degree(polynom):
    degree = len(polynom) - 1
    return degree


def get_list(polynom):
    l = []
    polynom = str(polynom)
    for i in range(len(polynom)):
        l.append(int(polynom[i]))
    return l


def mirror(polynom):
    buf = []
    for i in range(get_degree(polynom), -1, -1):
        buf.append(polynom[i])
    return buf


def sum(p1, p2):
    p1 = mirror(p1)
    if get_degree(p1) > get_degree(p2):
        for i in range(len(p2)):
            p1[i] = (p1[i] + p2[i]) % 2
            res = p1
    else:
        for i in range(len(p1)):
            p2[i] = (p2[i] + p1[i]) % 2
            res = p2
    return mirror(res)


def divide(p1, p2):
    p1 = mirror(p1)
    p2 = mirror(p2)

    p1_degree = get_degree(p1)
    p2_degree = get_degree(p2)
    res_degree = p1_degree - p2_degree + 1;
    remainder = p1
    res = 10 ** res_degree
    res = get_list(res)
    res[0] = 0

    if p1_degree == p2_degree:
        res[0] = 1
        for i in range(p1_degree + 1):
            remainder[i] = p1[i] - p2[i]
    else:
        for i in range(res_degree):
            res[res_degree - i - 1] = remainder[p1_degree - i] / p2[p2_degree]
            for j in range(p2_degree + 1):
                remainder[p1_degree - j - i] -= int(p2[p2_degree - j] * res[res_degree - i - 1])
    remainder = mod2(remainder)
    return remainder


def coder(m, g):
    words = []
    r = len(str(g))
    m = get_list(m)
    g = get_list(g)
    new_m = []
    for i in range(len(m)):
        new_m.append(m[i])

    for i in range(r - 1):
        new_m.append(0)
    c = divide(new_m, g)
    a = sum(new_m, c)
    return a


def decoder(a, g, p):
    g = get_list(g)
    e = []
    error_degree = get_degree(a)
    for i in range(error_degree):
        n = random.uniform(0, 1)
        if n > p:
            e.append(1)
        else:
            e.append(0)
    b = sum(a, e)
    s = divide(b, g)

    if s.count(1) == 0:
        print('Erorr not found')
        return 1
    else:
        print('Error found')
        return 0


def probability_error(g, l, e):
    m = ''
    error_found = 0
    errors = 0
    N = int(9 // (4 * (e ** 2)))
    p = 0
    p_array = []
    Per_array = []
    for j in range(0, 100):
        p = j/100
        for i in range(N):
            for k in range(l):
                m += str(random.randint(0, 1))
            a = coder(m, g)
            errors += 1
            error_found += decoder(a, g, p)
            m = ''
        P = error_found / errors
        print('Error probability: ', P)
        p_array.append(j)
        Per_array.append(P)

    plt.plot(p_array, Per_array, )
    plt.xlabel('p ', fontsize=10, color='black')
    plt.ylabel('Per', fontsize=10, color='black')
    plt.title('Dependence of the decoding error on the error probability p', fontsize=10)
    plt.show()


def parse_polynom(g_parse):
    g = 0
    for i in range(0, len(g_parse) - 1):
        if '^' in g_parse[i]:
            g_degree = int(g_parse[i].split('^')[1])
            if g_parse[i].split('x')[0] == '':
                g += (10 ** g_degree)
            else:
                g = g + (int(g_parse[i].split('x')[0]) % 2) * (10 ** g_degree)
        else:
            g += 10
    g += int(g_parse[-1])
    return g



