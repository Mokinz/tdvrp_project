import math
import random

import numpy as np
from numpy.random import rand

import allthedata


class Point:
  def __init__(self, cords, s, q, name):
    self.cords = cords
    self.s = s
    self.q = q
    self.name = name

  def __repr__(self):
      return f"Point cords:{self.cords} s:{self.s} q:{self.q} name: {self.name}"
  def __str__(self):
      return str(self.cords) + str(self.s) + str(self.q)

# define range for input



def calculate_distance(point1, point2):
    return math.sqrt(pow(point2[0]- point1[0],2) + pow(point2[1]-point1[1],2))

def closest_node(node, nodes):
    dist_2 = []
    for nodee in nodes:
        if nodee.s != 0:
            dist_2.append(99999999999999999)
        else:
            dist_2.append(calculate_distance(node, nodee.cords))
    min = np.argsort(dist_2)
    for i in range(len(nodes)):
        if nodes[min[i]].s ==0:
            return min[i]

def initial_solution(S, retailStories):
    array = retailStories
    point = (30, 30)
    s = 1
    while s <= S:
        closest_node_index = closest_node(point, retailStories)
        point = retailStories[closest_node_index].cords
        array[closest_node_index].s = s
        s += 1
    return retailStories


def randomize_solution(curr):
    newArr= curr
    seqlist = []
    for s in curr:
        seqlist.append(s.s)
    min = np.argsort(seqlist)
    sample = random.sample(range(1, len(curr)), 2)
    newArr[min[sample[0]-1]].s = sample[1]
    newArr[min[sample[1]-1]].s = sample[0]
    return newArr

def simulated_annealing(A, tempstart, tempEnd, retailStories, C, p, ps, V, W, mpg, Td):
    # generate an initial point
    # first point pierwsza siatka współrzednych poprawna
    best = initial_solution(len(retailStories), retailStories)
    qarray = {}
    for r in best:
        qarray[r.s] = r
    S = len(retailStories)
    beta = (tempstart - tempEnd) / ((A-1) * tempstart * tempEnd)
    temp = tempstart
    # print('beta and temp',  beta, temp)
    # evaluate the initial point
    best_eval = allthedata.whole_process(p, C, S,  ps, qarray,  W, V, mpg, Td)
    # current working solution
    count = 0
    curr, curr_eval = best, best_eval
    # run the algorithm
    for i in range(A):
        # take a step
        candidate = randomize_solution(curr)
        qarray = {}
        for r in candidate:
            qarray[r.s] = r
        # evaluate candidate point
        candidate_eval = allthedata.whole_process(p, C, S,  ps, qarray,  W,V,mpg, Td)
        # check for new best solution
        if candidate_eval[1] < best_eval[1]:
            # store new best point
            best, best_eval = candidate, candidate_eval
        # difference between candidate and current point evaluation
        diff = candidate_eval[1] - curr_eval[1]
        # calculate temperature for current epoch
        temp = temp / (temp * beta + 1)
        # calculate metropolis acceptance criterion
        try:
            metropolis = math.exp(-diff / temp)
        except OverflowError:
            metropolis = float('inf')
        # check if we should keep the new point
        rnd = rand()/100
        if diff < 0 or rnd < metropolis:
            # store the new current point
            curr, curr_eval = candidate, candidate_eval
            count+=1
    print([best, best_eval[0], best_eval[1], best_eval[2], best_eval[3],  best_eval[4], count])
    return [best, best_eval[0], best_eval[1], best_eval[2], best_eval[3], best_eval[4], count]


# retailStories = [Point((0, 20), 0, 2), Point((10, 30), 0, 3), Point((0, 40), 0, 3), Point((0, 50), 0, 3), Point((20, 20), 0, 3), Point((50, 20), 0, 3)]
# print(simulated_annealing(1000, 225.84, 0.01, retailStories, 20, 0.01, 15, V=[20,40,50], W=[8,16,24], mpg=5, Td=12))
