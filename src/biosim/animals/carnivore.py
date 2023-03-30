from .animal import Animal
import random


class Carnivore(Animal):
    """
    The Carnivore class inherits the Animal class functions,
    and defines its own parameter and values.
    """
    params = {"w_birth": 6.0,
              "sigma_birth": 1.0,
              "beta": 0.75,
              "eta": 0.125,
              "a_half": 40.0,
              "phi_age": 0.3,
              "w_half": 4.0,
              "phi_weight": 0.4,
              "mu": 0.4,
              "gamma": 0.8,
              "zeta": 3.5,
              "xi": 1.1,
              "omega": 0.8,
              "F": 50.0,
              "DeltaPhiMax": 10.0}

    def __init__(self, age=None, weight=None):
        """
        Inherits the Init of the Animal class

        Parameters
        ----------

        age : int
        age of animal

        weight: float
        weight of animal
        """
        # Inherit init of Animal Class.
        super().__init__(age, weight)

    def feeding(self, herbivore_list: list):
        """
        This checks the probability of a herbivore's killing and
        eating that herbivore.
        - if herbivore's weight is higher than carnivore's capacity,
        then carnivore's  weight increases based on remaining
        capacity.
        - if herbivore's weight is lower than carnivore's capacity,
        then carnivore's  weight increases based on herbivore's full
         weight.
        - if the carnivore has not eaten its capacity it can keep
         hunting.


        Parameters
        ----------
        herbivore_list: list
        list of herbivore on the land

        Returns
        -------
        safe_herbivores: list
        herbivore_list: list
        Lists of herbivores remaining.

        """

        # Capacity defines how much food carnivore is allowed
        # to eat or has eaten.
        #
        # This is initially set equal to params['F'] which is
        # max food allowed to eat.
        capacity = self.params['F']

        # Counter is required to slice herbivore_list.
        # This is required to ensure carnivore does not attempt
        # to kill same herbivore twice.
        #
        # Initially value is set to zero.
        counter = 0

        # Safe_herbivore list will consist of herbivores that
        # did not get killed during hunting. This ensures even
        # if herbivore_list is sliced, previously not-killed
        # herbivores are accounted for.
        #
        # Initially set as empty list
        safe_herbivores = []

        for herb in herbivore_list[counter:]:

            # Validate if carnivore probability to kill is higher
            # than random then carnivore is allowed to eat the
            # herbivore.
            if random.random() <= self.prob_kill(herb.phi):

                # Validate if herbivore's weight is less than
                # capacity.
                if capacity <= herb.weight:

                    # Increase weight based on food eaten
                    # which is equal to capacity.
                    self.increase_weight(capacity)

                    # Decrease capacity until it reaches zero
                    # to ensure it has eaten to full capacity.
                    capacity -= capacity

                # Validate if herbivore's weight is greater than
                # capacity.
                else:

                    # Increase weight based on food eaten
                    # which is equal to herbivore's weight.
                    self.increase_weight(herb.weight)

                    # Decrease capacity until it reaches zero
                    # to ensure it has eaten to full capacity
                    capacity -= herb.weight

                # Increase counter by 1 for slicing the herbivore_list.
                # This will start the next cycle with herbivore_list
                # from the remaining alive herbivore.
                counter += 1

            # If carnivore's probability to kill is less than random
            # then herbivore is safe.
            else:
                # Add the alive herbivore to safe_herbivore list.
                safe_herbivores.append(herb)

                # Increase counter by 1 for slicing the herbivore_list.
                # This will start the next cycle with herbivore_list
                # from the remaining alive herbivore.
                counter += 1

            # Validate if carnivore has eaten to full capacity.
            # If condition is True, break the herbivore for loop.
            if capacity <= 0.0:
                break

        # Return the alive herbivores which consists of herbivores
        # who escaped the feeding and remaining herbivores that have
        # not been hunted.
        return safe_herbivores + herbivore_list[counter:]

    def prob_kill(self, fitness):
        """
        Checks the probability of Carnivore killing a Herbivore
        based on their respective fitness values.
        - if carnivore's fitness is less than herbivore, cannot kill.
        - if the difference of carnivore's fitness and herbivore's
        fitness lies between 0 and DeltaPhiMax, then probability kill
        is determined.
                (carnivore's phi - herbivore's phi) / DeltaPhiMax

        Parameters
        ----------
        fitness: float
        herbivore phi/fitness value.

        Returns
        -------
        int
        - 0 if carnivore's fitness is less than herbivore
        - (carnivore's phi - herbivore's phi) / DeltaPhiMax
        - 1

        """
        # Validate if carnivore's fitness is better than herbivore's
        # fitness.
        if self.phi <= fitness:

            # If carnivore's fitness is lower, assign 0.
            return 0

        # If carnivore_fitness - herbivore_fitness > 0 and,
        # carnivore_fitness - herbivore_fitness > DeltaPhiMax then
        # assign value as (carnivore_fitness - herbivore_fitness)/DeltaPhiMax.
        elif 0 < (self.phi - fitness) < self.params["DeltaPhiMax"]:
            return (self.phi - fitness) / (self.params["DeltaPhiMax"])

        else:
            return 1
