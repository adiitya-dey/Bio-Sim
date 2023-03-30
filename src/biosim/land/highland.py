from .land import Land


class HighLand(Land):
    """
    Highland Object

    A Highland object  represents a single land type on an array of islands, that inherits the
    Land Class and has a fodder value of 300

    it also runs all the life cycles just like the land object

    Class Parameters
    =================

    f_max:  float
            Maximum fodder allowed
    """
    # set the amount of fodder for Highland to 300
    f_max = 300

    def __init__(self):
        """
        Inherits the Init function in the Land class

        """
        super().__init__()
        self.habitable = True
