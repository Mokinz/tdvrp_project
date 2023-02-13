import math

def single_fuel_consumption(td, i, j, W, V, mpg):
    k = 0
    fk = 0
    d = calculate_distance(i, j)
    while td % 24 >= W[k + 1]:
        k += 1
    ta = td + d / V[k]
    f = gph(mpg,V[k]) * d / V[k]
    while ta % 24 >= W[k+1]:
        ta = (ta % 24 - W[k+1]) * V[k]/ V[k+1] + W[k+1]
        fk = fk + (W[k+1] - max(td % 24, W[k])) * gph(mpg, V[k])
        f = fk + (ta % 24 - W[k+1]) * gph(mpg, V[k+1])
        k += 1
    t = ta - td
    return f, t

def gph(mpg,v):
    return v/mpg

def calculate_distance(point1, point2):
    return math.sqrt(pow(point2[0] - point1[0],2) + pow(point2[1]-point1[1],2))