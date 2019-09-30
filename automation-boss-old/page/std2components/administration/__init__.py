from users import Users
from system import System
from features import Features


class Administration(Users, System, Features):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        # super(Administration, self).__init__(*args, **kwargs)
        Users.__init__(self, *args, **kwargs)
        System.__init__(self, *args, **kwargs)
        Features.__init__(self, *args, **kwargs)
