from . import NetworkObject
import z3
class EndHost (NetworkObject):
    """End host objects"""
    def _init (self, node, network, context):
        self.constraints = list ()
        self.ctx = context
        self.node = node.z3Node
        self._endHostRules()
        self._dumbConstraints()

    @property
    def z3Node (self):
        return self.node

    def _addConstraints (self, solver):
        solver.add(self.constraints)

    def _dumbConstraints (self):
        n = z3.Const('__nodeRules_Node', self.ctx.node)
        n2 = z3.Const('__nodeRules_Node2', self.ctx.node)
        n3 = z3.Const('__nodeRules_Node3', self.ctx.node)
        n4 = z3.Const('__nodeRules_Node4', self.ctx.node)
        p = z3.Const('__nodeRules_Packet', self.ctx.packet)
        p2 = z3.Const('__nodeRules_Packet2', self.ctx.packet)

    def _endHostRules (self):
        eh = z3.Const('__nodeRules_Node', self.ctx.node)
        eh2 = z3.Const('__nodeRules_Node2', self.ctx.node)
        eh3 = z3.Const('__nodeRules_Node3', self.ctx.node)
        p = z3.Const('__nodeRules_Packet', self.ctx.packet)
        # Constraints on packets sent
        # Packet sent always has source address set to something reasonable
        self.constraints.append(z3.ForAll([eh, p], z3.Implies(self.ctx.send(self.node, eh, p), \
            self.ctx.hostHasAddr(self.node, self.ctx.packet.src(p)))))

        # Packet sent always has origin set correctly
        self.constraints.append(z3.ForAll([eh, p],
            z3.Implies(self.ctx.send(self.node, eh, p), \
                    self.ctx.packet.origin(p) ==\
                                self.node)))
        # Body dutifully recorded 
        self.constraints.append(z3.ForAll([eh, p],
            z3.Implies(self.ctx.send(self.node, eh, p), \
                    self.ctx.packet.body(p) ==\
                                self.ctx.packet.orig_body(p))))

        # Constraints on packet received
        # Let us assume that packet received always have the right IP address (alternately the network stack can just
        # drop these).
        # FIXME: Eventually look at whether this can be s
        self.constraints.append(z3.ForAll([eh, p], \
                z3.Implies(self.ctx.recv(eh, self.node, p), \
                    self.ctx.hostHasAddr(self.node, self.ctx.packet.dest(p)))))

        self.constraints.append(z3.ForAll([eh, p], \
                z3.Implies(self.ctx.send(self.node, eh, p), \
                    z3.Not(z3.Exists([eh2], self.ctx.recv(eh2, self.node, p))))))

    @property
    def isEndHost (self):
        return True
