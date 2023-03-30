
__author__ = 'Aditya dey, Okubadejo Olutomi, NMBU'


import textwrap
from biosim.simulation import BioSim
from matplotlib import pyplot as plt

"""
A simple example of BioSim experiment, on a mono land
with visualization enabled and logging enabled.
Logging is enabled using log_file which the path or the
file name in txt or csv format.

Please use plt.show() at the end to keep the plot
in active mode.
"""

geogr = """\
           WWWWW
           WLHLW
           WWWWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (2, 4),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(10)]}]

sim = BioSim(geogr, ini_herbs, seed=1234, vis_years=1, ymax_animals=700, log_file="../../../log.csv")
sim.simulate(20)
sim.add_population(ini_carns)
sim.simulate(20)
plt.show()