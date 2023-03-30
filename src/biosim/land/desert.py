from .land import Land


class Desert(Land):
    """
    Desert Object

    A Desert object  represents a single land type on an array of islands, that inherits the
    Land Class and has a fodder value of 0, means animal that migrate to this land object would
    have no fodder to feed

    it also runs all the life cycles just like the land object

    Class Parameters
    =================

    f_max:  float
            Maximum fodder allowed
    """
    # set the amount of fodder for desert to 0
    f_max = 0

    def __init__(self):
        """
        Inherits the Init function in the Land class

        """
        super().__init__()
        self.habitable = True

    @classmethod
    def set_land_params(cls, params):
        """
        Sets the amount of fodder value for Desert object

        Parameters
        ----------
        params: dict
            Parameter for update

        Returns
        -------

        Raises
        -------
        Value_error:str


            - If dict contains no key:
                    Update params for land failed


            - If f_max value not an int or float:
                    f_max value is incorrect. Please use float or integer


            - If f_max value not 0
                      f_max for Desert has to be zero.
                      please check again

        """
        # Validate if user attempts to update Desert to anything other
        # than zero.
        for key in params:
            if key != 'f_max':
                raise ValueError(f"Update params for land failed."
                                 f"{key} does not exists. Use"
                                 f"f_max to set land parameters.")
        new_f_max = params["f_max"]
        if new_f_max is not None:
            if type(new_f_max) not in (int, float):
                raise ValueError('f_max value is incorrect. Please use float'
                                 'or integer.')
            elif new_f_max != 0:
                raise ValueError('f_max for Desert has to be zero. Please '
                                 'check again.')
            else:
                cls.f_max = new_f_max
