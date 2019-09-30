from services import Services
from synchronization import Synchronization


class Hybrid(Services, Synchronization):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        Services.__init__(self, *args, **kwargs)
        Synchronization.__init__(self, *args, **kwargs)
        # super(Users, self).__init__(*args, **kwargs)