from hybrid import Hybrid


class System(Hybrid):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        Hybrid.__init__(self, *args, **kwargs)
        # super(Users, self).__init__(*args, **kwargs)