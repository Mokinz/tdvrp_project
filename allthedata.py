import find_subpath
import fuel_consumption
import total_time


def whole_process( p, C, S, ps, qarray, W, V, mpg, Td):
    Re, Rb, N = find_subpath.find_subpath(S, C, qarray)
    print('Re', Re)
    print('Rb', Rb)
    print('N', N)
    print('qarray', qarray)
    tt, fuelDict = total_time.total_time(ps, Re, N, W, V, mpg, qarray,Td)
    print('fuelDict', fuelDict)
    tf = fuel_consumption.fuel_consumption(N, Re, Rb, p, fuelDict, qarray)
    return (tt, tf, Re, Rb, N)
