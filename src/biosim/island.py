from .land.lowland import LowLand
from .land.desert import Desert
from .land.highland import HighLand
from .land.water import Water

import numpy as np


class Island:
    """
    Island Object

    The Island object represents a single island on the Bio Simulation model
    the island objects converts the geogr into multiple land objects with
    individual locations, it also stores all this land objects.
    The island object runs the bio simulation lifecycle.
    """

    def __init__(self, geogr):
        """



        Init Parameters
        ===============

        island: dict
            dictionary containing multiple land objects

        geogr : str

            Multi line string specifying Island geography , parsed in from simulation file
        """
        self.island = {}

        # self.count_herb = 0
        # self.count_carn = 0
        for y, line in enumerate(geogr.splitlines()):
            for x, letters in enumerate(list(line)):

                if letters == 'L':
                    self.island[(y + 1, x + 1)] = LowLand()
                elif letters == 'H':
                    self.island[(y + 1, x + 1)] = HighLand()
                elif letters == 'D':
                    self.island[(y + 1, x + 1)] = Desert()
                elif letters == 'W':
                    self.island[(y + 1, x + 1)] = Water()
                else:
                    raise ValueError(f"{letters} does not exists in landscape"
                                     f"types. Please check map again.")

    def add_neighbors(self):
        """

        The function takes each land instance on the island, checks the land neighbours,
        and adds them to a list which is parsed to the add_neighbor_list function

        Returns
        -------

        neighbor_list :list
                list of neighboring land location values(tuples)

        """
        for loc, land in self.island.items():
            neighbors = [(loc[0] + 1, loc[1]),
                         (loc[0] - 1, loc[1]),
                         (loc[0], loc[1] + 1),
                         (loc[0], loc[1] - 1)]

            neighbors_list = []
            for neighbor in neighbors:
                if neighbor in self.island.keys():
                    neighbors_list.append(neighbor)

            land.add_neighbor_list(neighbors_list)

    def add_pop(self, loc, pop):
        """

        Takes in location and population values

        if the location exists in the island

        calls the insert_pop function

        Parameters
        ----------

        loc : tuple
            Location of land parameters parsed in from the simulation

        pop : list(dict)
            population information of land parameters parsed from simulation

        Returns
        -------

        Raises
        ------

        ValueError:
            If Key does not exist in island dictionary

        """
        if loc[0] and loc[1] is not None:

            # Validate if location exists.
            if loc not in self.island.keys():
                raise ValueError(f'{loc} does not exist')

            for key in self.island:
                if key == loc:
                    land_location = loc
                    territory = self.island[land_location]
                    territory.insert_pop(pop)
                    break

    @staticmethod
    def update_params(val1, val2, params):
        """

        Takes the dictionary of parameters that should be updated,

        - If it is for the animal class
                call set_animal_params function

        - if it is for land.
                check land type
                call set_land_params

        Parameters
        ----------
        val1 : str

            can either have the 'animal' or 'Landscape' value

        val2 : str

            can either be Desert, Highland, or Lowland used to determine the type of land

        params: str
            parameters to be updated, comes in a dictionary

        Returns
        -------

        Raises
        ------

        ValueError:
            if params is not a dictionary
            If landscape parameter does not exist

        """
        # Validate if params is a dictionary and validate if keys
        # are correct for land values.
        if type(params) is not dict:
            raise ValueError(f"Update params for land failed."
                             f"{params} is not a dictionary.")

        if val1 == 'animal':
            LowLand.set_animal_params(val2, params)
        elif val1 == 'landscape':
            if val2 == 'L':
                LowLand.set_land_params(params)
            elif val2 == 'H':
                HighLand.set_land_params(params)
            elif val2 == 'D':
                Desert.set_land_params(params)
            elif val2 == 'W':
                Water.set_land_params(params)
            else:
                raise ValueError(f"Landscape parameter {val1} does not exist")

    @staticmethod
    def update_animal_island_values():
        """
        Set Minimum weight

        calculate mu and sigma of animals in each land object
        Returns
        -------

        """
        LowLand.update_animal_values()

    def annual_cycle(self):
        """

        Full Land lifecycle

        - For every land object on the island

        Call birth_cycle

        Call regrow

        Call feeding_cycle

        Call migration_cycle

                - if Island location is habitable
                    migrate animal

                - else
                    keep animal in current land

        combine population of migrants and resident animals

        Call aging_cycle

        Call death_cycle


        Returns
        -------

        """

        for loc, terra in self.island.items():
            if terra.habitable:
                terra.birth_cycle()
                terra.regrow()
                terra.feeding_cycle()

                # Extract a dictionary for both herbivore and carnivore that choose
                # to migrate.
                # Ex:  migration_herbivore = {(1,1):[A1,A2,A3], (1,2):[A4,A5]}
                migration_herbivore, migration_carnivore = terra.migration_cycle()

                # Insert the herbivores that choose to migrate into the other
                # location in their migrate population.
                for location, population in migration_herbivore.items():
                    if self.island[location].habitable:
                        self.island[location].add_migration_pop(population, "Herbivore")
                    else:

                        # If other location is water, insert the animals back to
                        # their own location's migration population.
                        self.island[loc].add_migration_pop(population, "Herbivore")

                # Insert the carnivores that choose to migrate into the other
                # location in their migrate population.
                for location, population in migration_carnivore.items():
                    if self.island[location].habitable:
                        self.island[location].add_migration_pop(population, "Carnivore")
                    else:

                        # If other location is water, insert the animals back to
                        # their own location's migration population.
                        self.island[loc].add_migration_pop(population, "Carnivore")

        for terra in self.island.values():
            if terra.habitable:

                # Combine migration population with original population.
                terra.combine_pop()

                terra.aging_cycle()
                terra.death_cycle()

    def animal_count(self):
        """

        this adds the total number herbivore and carnivores to get the total animals

        Returns
        -------

        total_count: int
                Total number of animals on an Island
        """
        total_count = 0
        for counts in self.num_animals_species.values():
            total_count += counts
        return total_count

    @property
    def num_animals_species(self):
        """

        gets the total number of herbivores and carnivores
        for each land iteration

        Returns
        -------
        count_herbivore:dict

                Total count of herbivores on island object

        count_carnivore:dict

                Total count of carnivores on island object



        """
        count_herbivore = 0
        count_carnivore = 0
        for terra in self.island.values():
            count_herbivore += len(terra.pop_herbivore)
            count_carnivore += len(terra.pop_carnivore)
        return {"Herbivore": count_herbivore,
                "Carnivore": count_carnivore}

    def get_histogram(self):
        """

        Get animal dictionary

        with the age weight and fitness

        of each animal per land object

        Append them to the equivalent histogram_dict key value


        Returns
        -------

        histogram_dict :dict
            dictionary containing age, weight and fitness value of every animal
            on the island

        """
        histogram_dict = {"Herbivore": {"age": [],
                                        "weight": [],
                                        "fitness": []},
                          "Carnivore": {"age": [],
                                        "weight": [],
                                        "fitness": []}}

        for terra in self.island.values():
            animal_dict = terra.get_hist_values()
            histogram_dict["Herbivore"]["age"] = \
                histogram_dict["Herbivore"].get("age", []) + \
                animal_dict["Herbivore"]["age"]

            histogram_dict["Herbivore"]["weight"] = \
                histogram_dict["Herbivore"].get("weight", []) + \
                animal_dict["Herbivore"]["weight"]

            histogram_dict["Herbivore"]["fitness"] = \
                histogram_dict["Herbivore"].get("fitness", []) + \
                animal_dict["Herbivore"]["fitness"]

            histogram_dict["Carnivore"]["age"] = \
                histogram_dict["Carnivore"].get("age", []) + \
                animal_dict["Carnivore"]["age"]

            histogram_dict["Carnivore"]["weight"] = \
                histogram_dict["Carnivore"].get("weight", []) + \
                animal_dict["Carnivore"]["weight"]

            histogram_dict["Carnivore"]["fitness"] = \
                histogram_dict["Carnivore"].get("fitness", []) + \
                animal_dict["Carnivore"]["fitness"]

        return histogram_dict

    def get_matrix(self):
        """

        Creates a Carnivore and Herbivore Matrix

        from the number of Herbivore and Carnivores on

        each land object in the island list based on their location values

        Returns
        -------

        carn_matrix: array
                Carnivore Matrix

        herb_matrix: array
                Herbivore Matrix
        """
        carn_matrix = np.zeros(list(self.island.keys())[-1])
        herb_matrix = np.zeros(list(self.island.keys())[-1])
        for loc, terra in self.island.items():
            herb_matrix[loc[0] - 1][loc[1] - 1] = len(terra.pop_herbivore)
            carn_matrix[loc[0] - 1][loc[1] - 1] = len(terra.pop_carnivore)

        return carn_matrix, herb_matrix
