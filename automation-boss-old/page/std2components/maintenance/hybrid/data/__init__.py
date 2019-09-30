from users import Users


class Data(Users):
    """All D2 packages"""

    def __init__(self, *args, **kwargs):
        Users.__init__(self, *args, **kwargs)
