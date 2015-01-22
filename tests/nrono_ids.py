from examples import SimpleIDSShuntTopo 
import z3
import time
import random
import sys
import argparse

def ResetZ3 (seed):
    z3._main_ctx = None
    z3.main_ctx()
    z3.set_param('smt.random_seed', seed)

def Rono(internal, external, seed, samples):
    total_checks = 0
    total_time = 0.0
    times = []
    ResetZ3(seed)
    topo = SimpleIDSShuntTopo ((internal + external), external, 1)
    topo.net.Attach(*topo.fws)
    topo.net.Attach(*topo.hosts)
    topo.net.Attach(*topo.shunts)
    topo.net.Attach(*topo.ids)
    for (idx, i) in zip(xrange(samples), xrange(external)):
        start = time.time()
        result = topo.checker.CheckIsolationProperty(topo.hosts[i], topo.hosts[external])
        stop = time.time()
        total_time += (stop - start)
        total_checks += 1 
        times.append(stop - start)
    return (total_time / float(total_checks), times)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Non-rono fat-tree test')
    parser.add_argument('--iters', type=int, nargs='?', default=10)
    parser.add_argument('--imin', type=int, nargs='?', default=1)
    parser.add_argument('--imax', type=int, nargs='?', default=10)
    parser.add_argument('--emin', type=int, nargs='?', default=1)
    parser.add_argument('--emax', type=int, nargs='?', default=10)
    parser.add_argument('--seed', type=int, nargs='?', default=42)
    parser.add_argument('--samples', type=int, nargs='?', default=5)
    args = parser.parse_args()
    iters = args.iters
    int_min = args.imin
    ext_min = args.emin
    int_max = args.imax
    ext_max = args.emax
    seed = args.seed
    samples = args.samples
    print "external internal time"
    for iter in xrange(iters):
        for i in xrange(int_min, int_max):
            for e in xrange(ext_min, ext_max):
                (t, times) = Rono(i, e, seed, samples)
                times = ' '.join(map(str, times))
                print "%d %d %f %s"%(i, e, t, times)
