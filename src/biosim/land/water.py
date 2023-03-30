from .land import Land


class Water(Land):
    """
    This class creates an instance of class Land as a Type Water, and then set the amount of
    fodder available to None as animals cannot live here, it inherits the functions from Land class.
    """
    # set the amount of fodder for water to none
    f_max = None

    def __init__(self):
        """
        Inherits the Init function in the Land class

        """
        super().__init__()
        self.habitable = False

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


           - If f_max value not None
                     f_max value for Water should only be None.
        """
        # Validate if user attempts to update Water to anything other
        # than None.
        for key in params:
            if key != 'f_max':
                raise ValueError(f"Update params for Water failed."
                                 f"{key} does not exists. Use"
                                 f"f_max to set land parameters.")
        new_f_max = params["f_max"]
        if new_f_max is not None:
            if type(new_f_max) not in (int, float):
                raise ValueError('f_max value is incorrect. Please use float'
                                 'or integer.')
            elif new_f_max is not None:
                raise ValueError('f_max value for Water should only be None.')
            else:
                cls.f_max = new_f_max

    def insert_pop(self, pop: list):
        """
        Check if population to be inserted is None

        Parameters
        ----------
        pop : list(dict)
                empty population list

        Returns
        -------

        Raises
        -------

        ValueError:


            - If pop not None
                    In Water you cannot insert animals.

        """
        if pop is not None:
            raise ValueError('In Water you cannot insert animals.')

    def aging_cycle(self):
        """
        Do nothing,  pass the function
        Returns
        -------

        """
        pass

    def feeding_cycle(self):
        """
        Do nothing,  pass the function

        Returns
        -------

        """
        pass

    def death_cycle(self):
        """
        Do nothing,  pass the function
        Returns
        -------

        """
        pass

    def birth_cycle(self):
        """
        Do nothing,  pass the function
        Returns
        -------

        """
        pass

    def migration_cycle(self):

        """
        Do nothing,  pass the function
        Returns
        -------

        """
        pass

    def add_migration_pop(self, population: list, fauna):
        """
        Do nothing,  pass the function
        Returns
        -------

        """
        # Note: This logic was used to allow Water to perform migration
        # like other cells to validate if any animal is inserted in water.
        # This code is deprecated.

        pass

    def combine_pop(self):

        """


        Returns
        -------

        Raises
        -------
        ValueError:


                - If number of herbivore is not 0
                        There are some Herbivores in Water location, validate your results.

                - If number of carnivore is not 0
                        There are some Herbivores in Water location, validate your results.

                - If number of herbivore migration list is not 0
                        There are some Herbivores migrated in water, validate your results.

                - If number of carnivore migration list is not 0
                        There are some carnivores migrated in water, validate your results.
        """
        # Note: This Logic was meant to validate if during migration some animal is
        # inserted in water, we can throw error and validate the code.
        # This code is now deprecated since we do not iterate over water cells.
        if len(self.pop_herbivore) != 0:
            raise ValueError("There are some Herbivores in Water location."
                             " Validate your results.")
        if len(self.pop_carnivore) != 0:
            raise ValueError("There are some Carnivore in Water location."
                             " Validate your results.")
        if len(self.migrate_pop_herbivore) != 0:
            raise ValueError("There are some Herbivores migrated in Water"
                             " location. Validate your results.")
        if len(self.migrate_pop_carnivore) != 0:
            raise ValueError("There are some Herbivores migrated in Water"
                             " location. Validate your results.")
