from .land import Land


class LowLand(Land):
    """
      Lowland Object

    A lowland object  represents a single land type on an array of islands, that inherits the
    Land Class and has a fodder value of 800

    it also runs all the life cycles just like the land object

    Class Parameters
    =================

    f_max:  float
            Maximum fodder allowed
    """
    # set the amount of fodder for Lowland to 800
    f_max = 800

    def __init__(self):
        """
        Inherits the Init function in the Land class

        """
        super().__init__()
        self.habitable = True
