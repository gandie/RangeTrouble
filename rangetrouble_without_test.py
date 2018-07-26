#!/usr/bin/env python

import timeit
import matplotlib
import matplotlib.pyplot
import random

random.seed(1701 + 4711)

minsize = 100
maxsize = 10000
stepsize = 100
calls = 1000

# alternative definition of listsizes
# listsizes = [10 ** i for i in xrange(2, 5)]
listsizes = range(minsize, maxsize + stepsize, stepsize)

# normally we do not know the size of our list!
# pass list to functions as global to avoid hazzle (the hoff) with timeit-
# module which does not seem to allow passing arguments (wrapper might be used)
evil_list = []


def badLoop():
    result = []
    for i in range(len(evil_list)):
        item = evil_list[i]
        if item % 2 == 0:
            result.append(item)
    return result


def betterLoop():
    result = []
    for item in evil_list:
        if item % 2 == 0:
            result.append(item)
    return result


def comprehetionLoop():
    return [item for item in evil_list if item % 2 == 0]


def generatorLoop():
    def myfilter(input_list):
        for item in input_list:
            if item % 2 == 0:
                yield item
    return list(myfilter(evil_list))


def filterLoop_lambda():
    return list(filter(lambda x: x % 2 == 0, evil_list))


e_times = []
b_times = []
c_times = []
g_times = []
fl_times = []

for size in listsizes:
    evil_list = [random.randint(0, 9) for _ in range(size)]
    e = badLoop()
    b = betterLoop()
    c = comprehetionLoop()
    g = generatorLoop()
    fl = filterLoop_lambda()

    assert e == b, 'Results must be equal!'
    assert e == c, 'Results must be equal!'
    assert e == g, 'Results must be equal!'
    assert e == fl, 'Results must be equal!'

    print('Bad loop with size %s' % size)
    evil_time = timeit.timeit(badLoop, number=calls)
    e_times.append(evil_time)
    print('Better loop with size %s' % size)
    better_time = timeit.timeit(betterLoop, number=calls)
    b_times.append(better_time)
    print('Comprehention loop with size %s' % size)
    curious_time = timeit.timeit(comprehetionLoop, number=calls)
    c_times.append(curious_time)
    print('Generator Loop with size %s' % size)
    generator_time = timeit.timeit(generatorLoop, number=calls)
    g_times.append(generator_time)
    print('Filter Loop lambda with size %s' % size)
    filter_time_lambda = timeit.timeit(filterLoop_lambda, number=calls)
    fl_times.append(filter_time_lambda)

figure, axes = matplotlib.pyplot.subplots()
axes.plot(listsizes, e_times, label='range(len()) loop')
axes.plot(listsizes, b_times, label='for item in loop')
axes.plot(listsizes, c_times, label='List comprehention loop')
axes.plot(listsizes, g_times, label='Generator loop')
axes.plot(listsizes, fl_times, label='filter() with lambda loop')
biglabel = '''
List size, random integers
Stepsize is {stepsize}
Filter items from list with i % 2 == 0
'''.format(stepsize=stepsize)
axes.set(xlabel=biglabel, ylabel='Time needed for %s calls [s]' % calls)
axes.legend()
axes.grid()
figure.savefig('plot.png')
matplotlib.pyplot.show()
