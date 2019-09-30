"""
"""
from topology import Topology
from hybrid import Hybrid


class Maintenance(Topology, Hybrid):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        Topology.__init__(self, *args, **kwargs)
        Hybrid.__init__(self, *args, **kwargs)
        # super(Maintenance, self).__init__(*args, **kwargs)
