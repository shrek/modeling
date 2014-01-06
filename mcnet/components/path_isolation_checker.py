import z3
"""
Check if a property can be verified in a path independent manner (and verify it).
"""
VERIFIED_ISOLATION = 1
VERIFIED_GLOBAL = 2
UNKNOWN = 3

def CheckIsPathIndependentIsolated (checker_path, checker_full, psrc, pdest, fsrc, fdest, path_elements):
    """Check isolation based on path independence"""
    class PathIndependenceResult (object):
        def __init__ (self, judgement, isolation_result):
            self.result = isolation_result.result
            self.violating_packet = isolation_result.violating_packet
            self.last_hop = isolation_result.last_hop
            self.model = isolation_result.model
            self.judgement = judgement
            self.ctx = isolation_result.ctx

    result = checker_path.CheckIsolationProperty (psrc, pdest)

    if result.result == z3.unsat:
        # If we are being conservative then this is sufficient; but it
        # probably is not.
        return PathIndependenceResult(VERIFIED_ISOLATION, result)

    if result.result == z3.unknown:
        # Hmm let us see what comes of the big thing.
        result = checker_full.CheckIsolationProperty (fsrc, fdest)
        # We really do not know what in the world happened. So really it is possible that it was all path independent
        # and such but really things didn't work out
        return PathIndependenceResult(UNKNOWN, result)

    # This gives us the list of all participants. The reason for the :-1 is to get rid of the else_value which by
    # definition is 0
    participants = map(lambda l: l[0], result.model[result.model[result.ctx.etime].else_value().decl()].as_list()[:-1])
    z3PathElements = map(lambda n: n.z3Node, path_elements)
    bad_participants = filter(lambda p: not any(map(lambda z: p is z, z3PathElements)), participants)
    
    if len(bad_participants) == 0:
        return PathIndependenceResult(VERIFIED_ISOLATION, result)

    # OK so now we know that there are bad participants. In the normal way of the world we could just try globally but
    # we want to see if this really is path independent or not.
    p = z3.Const('path_independent_packet', result.ctx.packet)
    elements_to_consider = filter(lambda p: not any(map(lambda z: p is z, z3PathElements)), map(lambda l: l.z3Node, \
            result.ctx.node_list))
    constraint = z3.And(map(lambda n: z3.ForAll([p], result.ctx.etime(n, p, result.ctx.send_event) == 0), \
                        elements_to_consider))
    checker_path.AddExternalConstraints(constraint)
    result2 = checker_path.CheckIsolationProperty (psrc, pdest)
    checker_path.ClearExternalConstraints ()
    if result2.result != result.result:
        # Definitely not path independent.
        result_final = checker_full.CheckIsolationProperty (fsrc, fdest)
        return PathIndependenceResult (VERIFIED_GLOBAL, result_final)
    else:
        return PathIndependenceResult (VERIFIED_ISOLATION, result2)
