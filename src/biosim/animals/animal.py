import math
import random


class Animal:
    """
    Animal Class creates an instance of animal and handles
    the birth, death, fitness conditions.
    """
    # Initialize default class parameters to None.
    params = {"w_birth": None,
              "sigma_birth": None,
              "beta": None,
              "eta": None,
              "a_half": None,
              "phi_age": None,
              "w_half": None,
              "phi_weight": None,
              "mu": None,
              "gamma": None,
              "zeta": None,
              "xi": None,
              "omega": None,
              "F": None,
              "DeltaPhiMax": None}

    # Initialise minimum weight required during childbirth.
    minimum_weight = None

    # Initialize mu and sigma required for child weight
    # calculation.
    mu = None
    sigma = None

    def __init__(self, age: int = None, weight: float = None):

        """
        Animal Class is initialised with age and weight.

        Parameters
        ----------
        age : int
            animal age
        weight : float
            animal weight

        Raises
        ------
        ValueError, KeyError
        """

        # Check if weight is None and set value to zero.
        if weight is None:
            raise ValueError('Weight cannot be None. Please'
                             'enter a positive real number.')

        # Check if weight is not float or int and raise error.
        elif type(weight) not in (float, int):
            raise ValueError(f"Weight needs to be a float or integer. "
                             f"Please enter weight for {type(self)} again. ")

        # Check if weight is negative and raise error.
        elif weight < 0:
            raise ValueError(f"Weight cannot be negative when initialized. "
                             f"Please enter a positive real number for {type(self)}.")
        else:
            self.weight = weight

        # Check if age is None and set value to zero.
        if age is None:
            self.age = 0

        # Check if weight is not int and raise error.
        elif type(age) is not int:
            raise ValueError(f"Age needs to be non-negative integer. "
                             f"Please enter age for {type(self)} again. ")

        # Check if weight is negative and raise error.
        elif age < 0:
            raise ValueError(f"Age cannot be less than zero when initialized. "
                             f"Please enter non-negative integer for {type(self)}.")
        else:
            self.age = age

        self.phi = None
        self.fitness()

    def fitness(self):
        r"""

        The fitness(phi) of the animal is calculated based on the
        weight, age, weight half and age half.

        .. code::

                phi = q_age * q_weight
                q_age = 1 / ( 1 + \e^( phi_age * (age - a_half)))
                q_weight = 1 / ( 1 + e^(- phi_weight * (weight - w_half)))


        Returns
        -------

        """

        # Check if weight is zero, set fitness value to zero else otherwise.
        if self.weight <= 0.0:
            self.phi = 0
        else:
            # Calculate q_age and q_weight for fitness value.
            # phi = q_age * q_weight
            # q_age = 1 / ( 1 + e^( phi_age * (age - a_half)))
            # q_weight = 1 / ( 1 + e^(- phi_weight * (weight - w_half)))
            q_age = 1 / (1 + math.exp(self.params["phi_age"] *
                                      (self.age - self.params["a_half"])))

            q_weight = 1 / (1 + math.exp(-self.params["phi_weight"] *
                                         (self.weight - self.params["w_half"])))
            self.phi = q_age * q_weight

    def aging(self):
        """
        The function increments age of an animal by 1.

        Returns
        -------

        """

        # Increment age by 1.
        self.age += 1

    def increase_weight(self, food: float):
        """
        The weight of an animal is increased by a factor of beta * food
        new_weight = old_weight + beta * food

        Parameters
        ----------

        food: float
        For herbivores food is the amount of fodder eaten.
        For carnivores food is the weight of herbivore.

        Returns
        -------

        """

        if food < 0:
            raise ValueError("food cannot be negative. Validate "
                             "Herbivore and Carnivore Class.")
        else:

            # Increase weight based on food value passed.
            # new_weight = old_weight + beta * food
            self.weight += self.params["beta"] * food

            # Re-update the fitness.
            self.fitness()

    def decrease_weight(self):

        r"""
        Decreases the weight of an animal every year n eta.

        - if weight becomes negative, set the weight to zero.
        - else,
        .. math::

             newweight = oldweight - \eta * oldweight.

        Parameters
        ----------

        Returns
        -------
        """

        # Decrease weight based on eta parameter.
        # new_weight = old_weight - eta * old_weight
        if self.weight < 0:
            self.weight = 0
        else:
            self.weight -= self.params["eta"] * self.weight

    def death(self):
        r"""
        Checks the probability of death of each animal based on the
        fitness and omega.

        .. math::

                    \omega * (1 - \phi)

        Returns
        -------
        bool
        - if bool is True, animal is marked for death.
        - if bool is False, animal survives.
        """
        self.fitness()
        if self.weight == 0:
            return True
        elif random.random() < (self.params['omega'] * (1 - self.phi)):
            return True
        else:
            return False

    @classmethod
    def min_weight(cls):
        r"""
        Calculates the minimum weight required for childbirth
        for an animal.

        .. math::

                \zeta * \omega_birth + \sigma_birth
        Returns
        -------

        """
        # Calculate minimum weight required during birth.
        cls.minimum_weight = (cls.params["zeta"]) * \
                             (cls.params["w_birth"] + cls.params["sigma_birth"])

    @classmethod
    def calculate_mu_sigma(cls):
        r"""
        calculates mu and sigma variable for child weight calculations

        .. math::

                  mu =  \ln (\mu_x^{2} / \sqrt{\mu_x^{2} + \sigma_x^{2}})


        .. math::

           sigma = \sqrt{\ln(1+(\sigma_x^{2}/\mu_x^{2}))}

        Returns
        -------

        """
        # Calculate mu and sigma for lognormvariate function
        # mu = ln( mu_x^2 / (sqrt(mu_x^2 + sigma_x^2)
        # sigma = sqrt( ln( 1 + (mu_x^2 / sigma_x^2)
        mu_x = cls.params["w_birth"]
        sigma_x = cls.params["sigma_birth"]
        cls.mu = math.log((mu_x ** 2) / (math.sqrt(mu_x ** 2 + sigma_x ** 2)))
        cls.sigma = math.sqrt(math.log(1 + (sigma_x ** 2 / mu_x ** 2)))

    def birth(self):
        """
        Checks the probability of an animal giving birth to a child.
        A child is born with age = 0 and weight based on lognormvariate.
        Conditions for child's birth are:
        - child weight should be greater than zero.
        - animal's weight should be greater than birth weight loss.


        Returns
        -------
        Animal Class
        """

        # Calculate child weight based on random lognormvariate
        # using mu and sigma as parameters.
        child_weight: float = random.lognormvariate(self.mu, self.sigma)

        # Calculate mother's weight loss after child's birth.
        # weight loss = xi * child_weight
        weight_loss = self.params["xi"] * child_weight

        # Calculate minimum weight required by mother for child's birth.
        # minimum weight = zeta * (w_birth + sigma_birth)
        # default minimum weight = 33.25
        # minimum_weight = (self.params["zeta"]) * \
        #                  (self.params["w_birth"] + self.params["sigma_birth"])

        # Validate if mother's weight is greater than zero and minimum weight.
        # if 0 < self.weight >= minimum_weight:

        # Validate if child_weight is not zero and,
        # mother's weight is greater than weight loss.
        if (child_weight > 0) and (self.weight > weight_loss):

            # Decrease mother's weight since birth condition is True.
            # mother's new weight = old weight - weight loss.
            # weight loss = xi * child weight
            self.weight -= weight_loss

            # Update fitness value of mother after birth.
            self.fitness()

            # Return newborn child with age=0 and pseudorandom calculated
            # weight.
            return type(self)(age=0, weight=child_weight)

        else:

            # Return None if birth is not allowed.
            return None

    def migrate_prob(self):
        """
        Checks the probability of an animal migrating.
        probability = mu * phi
        - if probability is higher than random, animal can migrate.
        - else, animal cannot migrate.

        Returns
        -------

        """
        probability = self.params["mu"] * self.phi
        if random.random() < probability:
            return True
        else:
            return False

    @staticmethod
    def migration(migration_list: list):
        """
        Makes a random choice from possible migration locations
        for an animal  from the migration list.

        Parameters
        ----------
        migration_list: list
        List of possible migration locations for an animal.

        Returns
        -------
        tuple

        """
        if len(migration_list) == 0:
            return None
        else:
            return random.choice(migration_list)

    @classmethod
    def update_params(cls, params=None):
        """
        Updates the class parameters based on the params parsed
        in and the animal class.

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
            elif key == "DeltaPhiMax" and value <= 0:
                raise ValueError("DeltaPhiMax value has to be greater than 0.")

            # Validate 0 < Eta <= 1
            elif key == "eta" and 0 < value > 1.0001:
                raise ValueError("Eta value has to be less than equal to 1.")

            # Validate values are not negative
            elif value < 0:
                raise ValueError(f"{key} value has to be greater than 0..")

        # If no validation error, update params.
        for key in params:
            cls.params[key] = params[key]
