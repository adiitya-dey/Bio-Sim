from .animal import Animal


class Herbivore(Animal):
    """
    The Herbivore class inherits the Animal class functions,
     and defines its own parameter and values.
    """
    # Initialize default class parameters.
    params = {"w_birth": 8.0,
              "sigma_birth": 1.5,
              "beta": 0.9,
              "eta": 0.05,
              "a_half": 40.0,
              "phi_age": 0.6,
              "w_half": 10.0,
              "phi_weight": 0.1,
              "mu": 0.25,
              "gamma": 0.2,
              "zeta": 3.5,
              "xi": 1.2,
              "omega": 0.4,
              "F": 10.0,
              "DeltaPhiMax": None}

    def __init__(self, age=None, weight=None):
        """
          Inherits the Init of the Animal class.

          Parameters
          ----------

          age : int
          age of animal

          weight: float
          weight of animal
          """
        # Inherit init of Animal Class.
        super().__init__(age, weight)

    def feeding(self, grass: float):
        """
        Herbivore eats an amount either equal to capacity or fodder
        amount.
        - If the amount of fodder left is less than the capacity of
         the Herbivore to eat then it increases the herbivores weight
          by fodder left
        - Else capacity F.

        Parameters
        ----------
        grass: float
        fodder not yet eaten

        Returns
        -------
        F : float
        if F <= grass

        grass: float
        if F > grass

        """
        # Validate if params['F'] is less than grass value.
        if self.params["F"] <= grass:

            # Increase weight based on amount of grass eaten.
            self.increase_weight(self.params['F'])

            # Re-update fitness based on new weight.

            # Return amount of grass eaten which is equal to
            # params['F'].
            return self.params['F']

        # Validate if params['F'] is greater than grass value.
        else:

            # Increase weight based on amount of grass eaten.
            self.increase_weight(grass)

            # Return amount of grass eaten which is equal to
            # grass.
            return grass

    @classmethod
    def update_params(cls, params=None):
        """
        Updates the class parameters based on the params parsed
        in and the Herbivore class.

        Parameters
        ----------
        params: dict

        Returns
        -------

        Raises
        ------
        ValueError
        """
        if params is None:
            raise ValueError("No parameters are passed. Please check again.")
        elif type(params) != dict:
            raise ValueError("Only dictionary format allowed.")

        # Validate parameters have correct information.
        for key, value in params.items():
            # Validate key exists in params.
            if key not in cls.params:
                raise ValueError(f'{key} parameter does not exist.'
                                 f' Please enter correct values.')

            # Validate param values are only int and float.
            elif type(value) not in (int, float):
                raise ValueError(f'{key} parameter value is not integer or float'
                                 f'for {type(cls)}.Please enter correct values.')

            # Validate DeltaPhiMax > 0
            elif key == "DeltaPhiMax" and value is not None:
                raise ValueError("DeltaPhiMax value cannot be set for Herbivore.")

            # Validate 0 < Eta <= 1
            elif key == "eta" and 0 < value > 1.0001:
                raise ValueError("Eta value has to be less than equal to 1.")

            # Validate values are not negative
            elif value < 0:
                raise ValueError(f"{key} value has to be greater than 0..")

        # If no validation error, update params.
        for key in params:
            cls.params[key] = params[key]
