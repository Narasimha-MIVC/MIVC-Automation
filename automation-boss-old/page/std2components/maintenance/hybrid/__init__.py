from services import Services
from data import Data


class Hybrid(Services, Data):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        Services.__init__(self, *args, **kwargs)
        Data.__init__(self, *args, **kwargs)
        # super(STD2Pages, self).__init__(*args, **kwargs)