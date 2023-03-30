from biosim.animals.herbivore import Herbivore
from biosim.animals.carnivore import Carnivore
import random


class Land:
    """
    Land Object

    A Land object represents a single land type on an array of islands,
    the land object stores information of the carnivores and herbivores
    in a population list, Land object also performs the various life
    cycles on the animals, which includes death cycle, aging, weight loss
    feeding, birth, migration.
    It stores information of the maximum amount of fodder in a land type

    Class parameters:
    =================
    f_max:  float
            Maximum fodder allowed
    habitable: bool
            Checks if land can be migrated to
    """
    # Initialize f_max (maximum fodder on specific land allowed).
    f_max = None
    habitable = None

    def __init__(self):
        """
        Land Initialization

        the Herbivore list, Carnivore list Land neighbors list, potential herbivore migrants list
        and potential carnivore migrants list are all initialised in self here.

        Init Parameters
        ===============

        pop_herbivore: list
                Herbivores list of a single land type
        pop_carnivore: list
                Carnivore list of a single land type
        neighbors : list
                tuple value of neighboring land coordinates
        fodder: int
                sets the fodder amount for an instance of land
        migrate_pop_herbivore: list
                Herbivores ready to migrate
        migrate_pop_carnivore: list
                Carnivore ready to migrate
        """
        # Initialize an empty list to the store population of
        # herbivores and carnivores.
        self.pop_herbivore = []
        self.pop_carnivore = []

        self.neighbors = []

        # Initialize the self.fodder to f_max
        self.fodder = self.f_max

        # Initiate the migrate_pop_herbivore list to store Herbivores that want to migrate
        self.migrate_pop_herbivore = []

        # Initiate the migrate_pop_carnivore list to store Carnivores that want to migrate
        self.migrate_pop_carnivore = []

    @classmethod
    def set_land_params(cls, params):
        """
        Sets the amount of fodder value for an Instance of land
        based on its type (Lowland, Highland, Desert or Water)

        Parameters
        ----------
        params :dict
                f_max value for update

        Returns
        -------

        Raises
        ------
        value_error


            - If dict contains no key:
                  Update params for land failed


            - If new_fmax is None:
                 f_max cannot be set to None for Land


        """
        # Validate if param values are correct.
        for key in params:
            if key != 'f_max':
                raise ValueError(f"Update params for land failed."
                                 f" {key} does not exists. Use"
                                 f"f_max to set land parameters.")
        new_f_max = params["f_max"]

        # Validate if f_max is positive real number.
        if new_f_max is not None:
            if type(new_f_max) in (int, float) and new_f_max >= 0:
                cls.f_max = new_f_max
            else:
                raise ValueError('f_max value is incorrect. Please use float'
                                 'or integer.')
        else:
            raise ValueError('f_max cannot be set to None for Land.')

    @staticmethod
    def set_animal_params(val, params):
        """
        Inputs the val and params, then based on val, it sets
        parameters to the animal type's :func:`Animal.update_params`.

        Parameters
        ----------
        val : str
                Animal Specie (Herbivore or Carnivore)
        params: dict
                Parameters for update

        Returns
        -------

        Raises
        -------
        Value_error


         - If val not Carnivore or Herbivore:
                animal type does not exist

        """

        # it checks if Val comes in as a Herbivore or Carnivore
        if val == 'Herbivore':

            # then updates the Class Herbivore or Carnivore based on the parameters
            # parsed in.
            Herbivore.update_params(params)
        elif val == 'Carnivore':
            Carnivore.update_params(params)
        else:
            raise ValueError(f"{val} animal type does not exists.")

    def add_neighbor_list(self, neighbors: list):
        """
        sets the tuple value of the neighbor land coordinates for a land instance

        Parameters
        ----------

        neighbors : list
                List of neighbour land coordinates

        Returns
        -------

        """
        self.neighbors = neighbors

    # This function takes in the population list containing new species to be inserted
    def insert_pop(self, pop: list):
        """
        Inserts population into the land object

        Parameters
        ----------

        pop : list(dict)
             Animal population

        Returns
        -------

        Raises
        -------

        ValueError:


            - If key not one of species, age or weight
                Key value does not exist


            - If dictionary has no Key
                Key does not have a valid value


            - If species not carnivore or herbivore
                species does not exist please check again

        """
        # Validare if population entries are correct.
        for entries in pop:
            for key in entries:
                if key not in ("species", "age", "weight"):
                    raise ValueError(f'{key} key does not exist')
                elif entries[key] is None:
                    raise ValueError('Key does not have a valid value')

        # Iterate the dictionary of containing each animal
        for species in pop:

            # We store the age and weight values in individual variables
            age = int(species["age"])
            weight = float(species["weight"])
            if species["species"].lower() == "herbivore":

                # Check if the species is Herbivore, and append to the
                # Herbivore list.
                self.pop_herbivore.append(Herbivore(age=age, weight=weight))

            elif species["species"].lower() == "carnivore":

                # Check if the species is Carnivore, and append to Carnivore list.
                self.pop_carnivore.append(Carnivore(age=age, weight=weight))

            else:
                raise ValueError(f"{species['species']} does not exists. Please check"
                                 f"again.")

    def regrow(self):
        """
        Resets Fodder value

        Returns
        -------

        """
        # Reset fodder value to f_max.
        self.fodder = self.f_max

    def aging_cycle(self):
        """

        Increases each animal in a land object's age by 1
        and decreases their weight

        Returns
        -------

        """

        def aging(population):
            """
            This land function performs aging, weight decrease and fitness calculation on every
            animal in the population list parsed in.

            Parameters
            ----------
            population: list of animals based on specie or migration status

            Returns
            -------

            """
            for animal in population:
                animal.aging()
                animal.decrease_weight()
            return population

        self.pop_herbivore = aging(self.pop_herbivore)
        self.pop_carnivore = aging(self.pop_carnivore)

    def feeding_cycle(self):
        """

        Shuffles herbivore list

            - If fodder on land object is greater than  0
                    performs feeding conditions on every Herbivore in a land object




        Sorts Carnivore in decreasing order of fitness

            - If number of herbivores is greater than 0
                    runs carnivore feeding conditions on all carnivores in a land object

        Returns
        -------

        """
        # Shuffle herbivore population for random eating order.
        random.shuffle(self.pop_herbivore)

        for herbivore in self.pop_herbivore:

            # Check if the fodder is not completely eaten up
            if self.fodder > 0:

                # Parse the amount of fodder left into the animal function feeding and
                # return the amount of fodder eaten by the Herbivore.
                eaten = herbivore.feeding(self.fodder)

                # Decrease the number of fodder left by the amount eaten by the Herbivore
                self.fodder -= eaten
            else:
                break

        # Sort Herbivore list in ascending order of fitness for Carnivore to feed.
        self.pop_herbivore = sorted(self.pop_herbivore, key=lambda herb: herb.phi, reverse=False)

        # Sort the Carnivore list in descending order of fitness.
        self.pop_carnivore = sorted(self.pop_carnivore, key=lambda carni: carni.phi, reverse=True)

        for carnivore in self.pop_carnivore:

            # Check if herbivore population exists.
            if len(self.pop_herbivore) > 0:

                # Parse the current herbivore list into carnivore feeding function and return the
                # updated herbivore list based on those that have been killed.
                self.pop_herbivore = carnivore.feeding(self.pop_herbivore)
            else:
                break

    def death_cycle(self):
        """
        Gets a list of animals that survive, after parsing each animal
        through for death probability check in the animal class (death)

        Returns
        -------

        """

        # Create list of animal population which survives.
        def survivor(pop):
            """

            Parameters
            ----------
            pop: population list

            Returns
            -------

            """

            # If the return is true the animal dies,
            # if the return is false the animal is added to the list.

            # Note: Code has been taken from BioLab project given as part of example.
            return [animal for animal in pop if animal.death() is False]

        # We set the Herbivore and Carnivore list to the list of animals that have survived.
        self.pop_herbivore = survivor(self.pop_herbivore)
        self.pop_carnivore = survivor(self.pop_carnivore)

    @staticmethod
    def update_animal_values():
        """
        Calculates minimum weight of animal needed for childbirth conditions

        Calculates Mu and sigma, parameters for finding child weight

        Returns
        -------

        """
        # Calculate minimum weight required during birth.
        Herbivore.min_weight()
        Carnivore.min_weight()

        # Calculate mu sigma for lognormvariate for child weight.
        Herbivore.calculate_mu_sigma()
        Carnivore.calculate_mu_sigma()

    def birth_cycle(self):
        r"""
        Runs the birth conditions on every animal on the land object with
        :func:`Animal.birth`


            - If length of animal specie list is greater than 1


            - If the animals weight is greater or equal to its minimum weight


            - If the probability of birth is greater than the land birth probability


        probability of birth = Random number generated

        Land birth probability

        .. math::

             = \min(1, \gamma * \phi * N)


        Parameters
        ----------

        pop : list(dict)
            population list of animal type
            used in sub function(birthing)

        Returns
        -------

        """

        # We define a function birthing inorder to generalise the code for carnivore and herbivore
        def birthing(pop):
            """
            This is the generalization function for the birth_cycle function
            Parameters
            ----------
            pop : population list of animal type

            Returns
            -------

            pop_child_list

            """

            # an empty list is created to store the newborn child
            pop_child_list = []

            # Check if there is more than one animal in the animal_list
            if len(pop) > 1:

                # loop through the list of animals in each list
                for animal in pop:
                    if 0 < animal.weight >= animal.minimum_weight:
                        # Set the random value and store in a variable prob_birth
                        prob_birth = random.random()

                        # we calculate the conditions for birth on the land and store in a variable
                        # land_birth_prob = minimum(1, gamma * phi * length of animals in the list
                        # excluding the animal being considered
                        land_birth_prob = min(1, animal.params["gamma"] *
                                              animal.phi * (len(pop) - 1))
                        # Check if the land birth probability is greater than the random number
                        if prob_birth < land_birth_prob:

                            # Run the animal Birth function on the selected animal
                            # and return the child
                            child = animal.birth()

                            # if the child has a value and is not None,
                            # add the child to the child_list
                            if child is not None:
                                pop_child_list.append(child)

            return pop_child_list

        pop_child_herbivore = birthing(self.pop_herbivore)

        # Add the children birthed by the herbivores to the herbivore list
        self.pop_herbivore = self.pop_herbivore + pop_child_herbivore

        pop_child_carnivore = birthing(self.pop_carnivore)

        # Add the children birthed by the carnivores to the carnivore list
        self.pop_carnivore = self.pop_carnivore + pop_child_carnivore

    def migration_cycle(self):
        """
        It contains a generalization function for herbivores and carnivores

        Takes a population list (herbivore or carnivores)


            - If migration probability of animal in list is True

                Call :func:`Animal.migration` parse in land object neighbors.

                return new location


            - If new location has no value

                Add animal to no migration list


            - If new location has value

                Store it and animal in a dictionary


            - If migration probability is false

                Add animal to no migration list

        Returns
        -------

        migration_herbivore: dict
            dictionary of herbivores set to migrate

        migration_carnivore: dict
            dictionary of carnivores set to migrate
        """

        def find_migration(population):
            """
            generalization function for migration_cycle

            Parameters
            ----------
            population : population list of animal type

            Returns
            -------
            no_migration : list of animals not migrating

            migration_dict: dictionary of animals migrating and their destinations
            """
            # Create a migration dict to store location as key and values represent
            # list of animals that choose to migrate.
            migration_dict = {}

            # Create an empty list for animals that do not choose to migrate.
            no_migration = []
            for animal in population:
                if animal.migrate_prob() is True:

                    # Animal provides information of the location.
                    new_loc = animal.migration(self.neighbors)
                    if new_loc is None:

                        # If location is None, animal appended to no_migration
                        # list.
                        # NOTE: This logic was made when water was not passed as
                        # neighbors. It is now deprecated.
                        no_migration.append(animal)
                    else:

                        # Append the animal to existing list for that location.
                        migration_dict[new_loc] = migration_dict.get(new_loc, []) \
                                                  + [animal]
                else:

                    # If migration probability is false, append to no_migration
                    # list.
                    no_migration.append(animal)

            return no_migration, migration_dict

        self.pop_herbivore, migration_herbivore = find_migration(self.pop_herbivore)
        self.pop_carnivore, migration_carnivore = find_migration(self.pop_carnivore)

        return migration_herbivore, migration_carnivore

    def add_migration_pop(self, population: list, fauna):
        """
        Adds population of animals to migration population list of land object:


            - If animal type is carnivore, add to carnivore migration list


            - If animal type is herbivore, add to herbivore migration list

        Parameters
        ----------
        population : list of animals that want to migrate to this land cell

        fauna : animal type (herbivores or carnivores)

        Returns
        -------

        """
        if fauna.lower() == "herbivore":
            self.migrate_pop_herbivore = self.migrate_pop_herbivore + population
        elif fauna.lower() == "carnivore":
            self.migrate_pop_carnivore = self.migrate_pop_carnivore + population

    def combine_pop(self):
        """
        Joins the normal population list of the land object
        with the list of animals migrating to that land.

        Returns
        -------

        """
        self.pop_herbivore = self.pop_herbivore + self.migrate_pop_herbivore
        self.pop_carnivore = self.pop_carnivore + self.migrate_pop_carnivore
        self.migrate_pop_herbivore = []
        self.migrate_pop_carnivore = []

    def get_hist_values(self):
        """
        Gets the age, weight and fitness(phi), for every animal in that land

        Returns
        -------

        """
        herb_age = []
        herb_weight = []
        herb_fitness = []

        carn_age = []
        carn_weight = []
        carn_fitness = []

        for herbivore in self.pop_herbivore:
            herb_age.append(herbivore.age)
            herb_weight.append(herbivore.weight)
            herb_fitness.append(herbivore.phi)

        for carnivore in self.pop_carnivore:
            carn_age.append(carnivore.age)
            carn_weight.append(carnivore.weight)
            carn_fitness.append(carnivore.phi)

        return {"Herbivore": {"age": herb_age,
                              "weight": herb_weight,
                              "fitness": herb_fitness},
                "Carnivore": {"age": carn_age,
                              "weight": carn_weight,
                              "fitness": carn_fitness}}
