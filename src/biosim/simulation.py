"""
BioSim Simulation
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


from .island import Island
from .visualization import Visualization
import random


class BioSim:
    """
    BioSim Object.
    """

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt='png',
                 log_file=None):

        """
        Parameters
        ----------
        island_map : str
            Multi-line string specifying island geography
        ini_pop : list
            List of dictionaries specifying initial population
        seed : int
            Integer used as random number seed
        vis_years : int
            Years between visualization updates (if 0, disable graphics)
        ymax_animals : int
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals : dict
            Color-scale limits for animal densities, see below
        hist_specs : dict
            Specifications for histograms, see below
        img_years : int
            Years between visualizations saved to files (default: `vis_years`)
        img_dir : str
            Path to directory for figures
        img_base : str
            Beginning of file name for figures
        img_fmt : str
            File type for figures, e.g. 'png' or 'pdf'
        log_file : str
            If given, write animal counts to this file

        Notes
        -----
        - If `ymax_animals` is None, the y-axis limit should be adjusted automatically.
        - If `cmax_animals` is None, sensible, fixed default values should be used.
        - `cmax_animals` is a dict mapping species names to numbers, e.g.,

          .. code:: python

             {'Herbivore': 50, 'Carnivore': 20}

        - `hist_specs` is a dictionary with one entry per property for which a histogram
          shall be shown. For each property, a dictionary providing the maximum value
          and the bin width must be given, e.g.,

          .. code:: python

             {'weight': {'max': 80, 'delta': 2},
              'fitness': {'max': 1.0, 'delta': 0.05}}

          Permitted properties are 'weight', 'age', 'fitness'.
        - If `img_dir` is None, no figures are written to file.
        - Filenames are formed as

          .. code:: python

             Path(img_dir) / f'{img_base}_{img_number:05d}.{img_fmt}'

          where `img_number` are consecutive image numbers starting from 0.

        - `img_dir` and `img_base` must either be both None or both strings.
        """
        # Validate the island_map geography is a string.
        if type(island_map) != str:
            raise ValueError("Island map needs to be string")
        else:
            self.island_map = island_map

        # Below validation on island_map identifies if,
        # 1. Edges of map is Water.
        # 2. Map has equal row sizes.

        # Convert the map into island list.
        island_list = self.island_map.splitlines()

        # Calculate max size of x and y coordinates.
        y_coordinates = len(island_list)
        x_coordinates = len(list(island_list[0]))

        for i, y in enumerate(island_list):
            size = len(list(y))
            if size != x_coordinates:
                raise ValueError(f"Island does not have similar number of columns."
                                 f"Check location: {i + 1} row.")
            else:

                for j, x in enumerate(list(y)):
                    if i == 0 or i == (y_coordinates - 1):
                        if x != 'W':
                            raise ValueError(f"Map provided is not an island."
                                             f"Check location ({i + 1},{j + 1})")
                    elif j == 0 or j == (x_coordinates - 1):
                        if x != 'W':
                            raise ValueError(f"Map provided is not an island."
                                             f"Check location ({i + 1},{j + 1})")

        self.map = Island(self.island_map)
        self.map.add_neighbors()
        self.add_population(ini_pop)

        # Validate if vis_years is a positive integer.
        if vis_years is None:
            self.vis_years = 0
        elif type(vis_years) is not int:
            raise ValueError("Vis_years needs to be integer only.")
        elif vis_years < 0:
            raise ValueError("Vis_years cannot be negative. Please"
                             "enter positive integers.")
        else:
            self.vis_years = vis_years

        # Validate img_years is a positive integer.
        if img_years is None:
            self.img_years = self.vis_years
        elif type(img_years) is not int:
            raise ValueError("Img_years needs to be integer only.")
        elif img_years < 0:
            raise ValueError("Img_years cannot be negative. Please"
                             "enter positive integers.")
        else:
            self.img_years = img_years

        # Validate img_dir is string.
        if img_dir is None:
            self.img_dir = None
        elif type(img_dir) != str:
            raise ValueError("Img_dir needs to be string.")
        else:
            self.img_dir = img_dir

        # Validate img_base is string.
        if img_base is None:
            self.img_base = None
        elif type(img_base) != str:
            raise ValueError("Img_dir needs to be string.")
        else:
            self.img_base = img_base

        self.img_fmt = img_fmt

        # Validate if ymax_animals is a positive integer.
        if ymax_animals is None:
            self.y_max = None
        elif type(ymax_animals) != int:
            raise ValueError("ymax_animals needs to be an integer.")
        elif ymax_animals < 0:
            raise ValueError("ymax_animals cannot be negative.")
        else:
            self.y_max = ymax_animals

        # Validate if cmax_animals is a dictionary of format
        # {'Herbivore': 50, 'Carnivore': 20}.
        if cmax_animals is None:
            self.c_max = None
        elif type(cmax_animals) != dict:
            raise ValueError("cmax_animals needs to be a dictionary"
                             " of format {'Herbivore': 50, 'Carnivore': 20}.")
        else:
            for key, value in cmax_animals.items():
                if key not in ("Herbivore", "Carnivore"):
                    raise ValueError(f"{key} is incorrect in cmax_animals."
                                     f" Please enter correctly.")

                if value < 0:
                    raise ValueError("negative values in "
                                     "c_max not allowed.")

            self.c_max = cmax_animals

        self.hist_specs = hist_specs

        # Validate if log file is a string.
        if log_file is None:
            self.log_file = log_file
        elif type(log_file) != str:
            raise ValueError("Log File is not a string.")
        else:
            self.log_file = log_file
            with open(log_file, 'w') as file:
                file.write("Year,Herbivore,Carnivore\n")

        self.num_years = 0

        # Set the seed value.
        self.seed = seed
        if self.seed is None:
            random.seed(123)
        else:
            random.seed(self.seed)

        # If vis_years or img_years is provided, create Visualization
        # Object.
        if self.vis_years > 0 or self.img_years > 0:
            self.visual = Visualization(geogr=self.island_map,
                                        y_max=self.y_max,
                                        c_max=self.c_max,
                                        img_years=self.img_years,
                                        img_dir=self.img_dir,
                                        img_base=self.img_base,
                                        img_fmt=self.img_fmt,
                                        vis_years=self.vis_years,
                                        hist_specs=self.hist_specs)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of species for which parameters shall be set.
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        self.map.update_params('animal', species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        Parameters
        ----------
        landscape : str
            Code letter for landscape
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        self.map.update_params('landscape', landscape, params)

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        """
        # Validate if num_years is a positive integer.
        if type(num_years) != int:
            raise ValueError(f"num_years needs to be int. "
                             f"{num_years} is incorrect.")
        elif num_years < 0:
            raise ValueError("Num years needs to be positive integer.")

        # Calculate animal minimum weight and mu, sigma
        self.map.update_animal_island_values()

        # Plot for zero year.
        if self.vis_years > 0 or self.img_years > 0:

            self.visual.get_plot_values(num_years)
            self.visual.draw_animal_count(animal_count=self.num_animals_per_species,
                                          current_year=self.num_years)
            self.visual.draw_year_counter(self.num_years)
            self.visual.draw_histogram(histogram_values=self.get_histogram_values())
            c_matrix, h_matrix = self.get_matrix()
            self.visual.draw_heatmap(h_matrix=h_matrix,
                                     c_matrix=c_matrix)
            if self.vis_years > 0:
                self.visual.show_plot()
            if self.img_years > 0:
                self.visual.save_fig(self.num_years)

        for _ in range(num_years):

            # Perform Annual Cycle on the island.
            self.map.annual_cycle()
            self.num_years += 1

            # Perform Visualization
            if self.vis_years > 0 or self.img_years > 0:

                # Update animal count irrespective of year jumps.
                self.visual.draw_animal_count(animal_count=self.num_animals_per_species,
                                              current_year=self.num_years)

                if self.num_years % self.vis_years == 0 or \
                        self.num_years % self.img_years == 0:

                    self.visual.draw_year_counter(self.num_years)
                    self.visual.draw_histogram(histogram_values=self.get_histogram_values())
                    c_matrix, h_matrix = self.get_matrix()
                    self.visual.draw_heatmap(h_matrix=h_matrix,
                                             c_matrix=c_matrix)

                    # Show plot
                    if self.num_years % self.vis_years == 0:
                        self.visual.show_plot()

                    # Save plot
                    if self.num_years % self.img_years == 0:
                        self.visual.save_fig(self.num_years)

            # Perform logging of each year to csv file.
            if self.log_file is not None:
                count = self.num_animals_per_species
                self.logger(self.num_years, count)

        # if self.vis_years > 0 or self.img_years > 0:
        #     self.visual.final_plot()

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : List of dictionaries
            See BioSim Task Description, Sec 3.3.3 for details.
        """
        for pop_dict in population:
            loc = pop_dict.get('loc')
            pop = pop_dict.get('pop')
            self.map.add_pop(loc, pop)

    @property
    def year(self):
        """
        Last year simulated

        Returns
        -------
        self.num_years
        """
        return self.num_years

    @property
    def num_animals(self):
        """
        Total number of animals on island.

        Returns
        -------
        self.map.animal_count()

        """
        return self.map.animal_count()

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary

        Returns
        -------
        self.map.num_animals_species
        """

        return self.map.num_animals_species

    def get_histogram_values(self):
        """
        Gets histogram values (age , weight, fitness of each animal per year)

        Returns
        -------
        self.map.get_histogram()

        """
        return self.map.get_histogram()

    def get_matrix(self):
        """
        Gets the carnovore and herbivore matrix

        Returns
        -------

        self.map.get_matrix()
        """

        return self.map.get_matrix()

    def make_movie(self, movie_fmt=None):
        """Create MPEG4 movie from visualization images saved."""

        self.visual.make_movie(movie_fmt)

    def logger(self, year, animal_count):
        """
        creates opens the log file and write the year, and animal count to it

        Parameters
        ----------
        year
            the year of the animal count value

        animal_count
            number of animals Herbivore and Carnivores

        Returns
        -------

        """
        with open(self.log_file, 'a') as file:
            file.write(f'{year}, '
                       f'{animal_count["Herbivore"]},'
                       f'{animal_count["Carnivore"]}\n')
