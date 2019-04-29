import os
import math
import random

import pylab


def write_config_to_file(filename, configuration):
    with open(filename, 'w+') as f:
        for a in configuration:
            f.write(str(a[0]) + ' ' + str(a[1]) + '\n')


def setup_configuration(filename, N_sqrt):
    L = []

    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            for line in f:
                a, b = line.split()
                L.append([float(a), float(b)])
        print('starting from file', filename)
    else:
        # from the initial_configuration_64.png file
        two_delxy = 1 / N_sqrt
        delxy = two_delxy / 2
        # generate a new configuration
        L = [[delxy + i * two_delxy, delxy + j * two_delxy] for i in range(N_sqrt) for j in range(N_sqrt)]

        # write it to a file
        write_config_to_file(filename, L)

        print('starting from a new random configuration')

    return L


def calc_sigma(eta, num_disks):
    return math.sqrt(eta / (num_disks * math.pi))


def show_conf(L, sigma, title, fname):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()


def dist(x, y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return math.sqrt(d_x ** 2 + d_y ** 2)


eta = 0.72
N = 64
sigma = calc_sigma(eta, N)
sigma_sq = sigma ** 2

filename = 'disk_configuration_N{0}_eta{1}.txt'.format(N, eta)

L = setup_configuration(filename, int(math.sqrt(N)))
delta = 0.3 * sigma
n_steps = 10000
# n_steps = 0
n_runs = 10

i = 0
for run in range(n_runs):
    print('Starting run {}'.format(i))
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        min_dist = min(dist(b, c) for c in L if c != a)
        if not (min_dist ** 2 < 4.0 * sigma_sq):
            a[:] = b
            a[0], a[1] = a[0] % 1.0, a[1] % 1.0
    i += 1
    show_conf(L, sigma, "N={} eta={}".format(N, eta), "b5_{}.png".format(i))

print(L)

# show_conf(L, sigma, "N={} eta={}".format(N, eta), "one_b5.png")
