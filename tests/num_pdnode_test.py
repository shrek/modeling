import z3
from z3 import is_true, is_false
from examples import *
import time
import mcnet.components as components
"""Check time as increase in nodes"""
def ResetZ3 ():
    z3._main_ctx = None
    z3.main_ctx()
    #z3.set_param('auto_config', False)
    #z3.set_param('smt.mbqi', True)
    #z3.set_param('model.compact', True)
    #z3.set_param('smt.pull_nested_quantifiers', True)
    #z3.set_param('smt.mbqi.max_iterations', 10000)

for it in xrange(0, 100):
    for sz in xrange(1, 1000000):
        ResetZ3()
        obj = NumPolicyNodesTest (sz)
        start = time.time()
        # Set timeout to some largish number
        obj.check.solver.set(timeout=10000000)
        ret = obj.check.CheckIsolationProperty(obj.e_0, obj.e_1)
        assert z3.sat == ret.result, \
                "Nothing stopping this"
        stop = time.time()
        print "%d %f"%(sz, stop - start)

