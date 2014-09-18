import z3
from z3 import is_true, is_false
from examples import *
import time
import mcnet.components as components
import random
import sys
"""Check time as pure increase in path length"""
def ResetZ3 ():
    z3._main_ctx = None
    z3.main_ctx()
    z3.set_param('smt.random_seed', random.SystemRandom().randint(0, sys.maxint))
    z3.set_param('smt.mbqi.max_iterations', 10000)
    z3.set_param('smt.mbqi.trace', True)
    z3.set_param('smt.mbqi.max_cexs', 100)
#def ResetZ3 ():
    #z3._main_ctx = None
    #z3.main_ctx()
    #z3.set_param('auto_config', False)
    #z3.set_param('smt.mbqi', True)
    #z3.set_param('model.compact', True)
    #z3.set_param('smt.pull_nested_quantifiers', True)
    #z3.set_param('smt.mbqi.max_iterations', 10000)
    #z3.set_param('smt.random_seed', random.SystemRandom().randint(0, sys.maxint))

iters = 5 
bad_in_row = 0
for sz in xrange(1, 200):
    times = []
    all_bad = True
    for it in xrange(0, iters):
        ResetZ3()
        obj = PathLengthTest (sz)
        # Set timeout to some largish number
        obj.check.solver.set(timeout=10000000)
        start = time.time()
        ret = obj.check.CheckIsolationProperty(obj.e_0, obj.e_1)
        stop = time.time()
        bad = False
        if z3.sat != ret.result:
            bad = True
        if not bad:
            times.append(stop - start)
            all_bad = False
    print "%d %s %s"%(sz, ' '.join(map(str, times)), "bad" if all_bad else "good")
    if all_bad:
        bad_in_row += 1
    else:
        bad_in_row = 0
    assert bad_in_row <= 5, \
            "Too many failures"

