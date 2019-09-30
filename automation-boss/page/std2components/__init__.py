from administration import Administration
from maintenance import Maintenance


class STD2Pages(Administration, Maintenance):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        Administration.__init__(self, *args, **kwargs)
        Maintenance.__init__(self, *args, **kwargs)
        # super(STD2Pages, self).__init__(*args, **kwargs)



