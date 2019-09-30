from _users import _Users


class Users(_Users):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        _Users.__init__(self, *args, **kwargs)
        # super(Users, self).__init__(*args, **kwargs)
