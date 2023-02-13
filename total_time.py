from single_fuel_consumption import single_fuel_consumption

CENTRUM_POINT = (30,30)
def total_time(ps, Re, N, W, V, mpg, qarray,td):
    tt=0
    s=1
    n=1
    fueldict = {}
    td = td
    while n <= N:
        tn=0
        fuel, t = single_fuel_consumption(td, CENTRUM_POINT, qarray[s].cords, W, V, mpg)
        fueldict[(0,s)] = fuel
        tn= tn + t
        tn = tn + ps

        while s != Re[n]:
            td = tn
            fuel, t = single_fuel_consumption(td, qarray[s].cords, qarray[s+1].cords,  W, V, mpg)
            fueldict[(s, s+1)] = fuel
            tn = tn + t
            s += 1
            tn = tn + ps
        td = tn
        fuel, t = single_fuel_consumption(td, qarray[s].cords, CENTRUM_POINT,  W, V, mpg)
        fueldict[(s, 0)] = fuel
        tn = tn + t
        tt = tt + tn
        n += 1
        s += 1
    return tt, fueldict
