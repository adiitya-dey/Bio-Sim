
__author__ = 'Aditya dey, Okubadejo Olutomi, NMBU'


import textwrap
from biosim.simulation import BioSim
from matplotlib import pyplot as plt

"""
A simple example of BioSim experiment on a mono
land with visuals. Visual are updated using 
vis-years. 
- vis_years = 0, graphics is disabled.
- vis_years = 1, plot for each year.
- vis_years = 3, plot after every 3 years.

Please use plt.show() at the end to keep the plot
in active mode, else the after the program run is 
completed, the plot will close automatically.
"""

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]

sim = BioSim(geogr, ini_herbs, seed=1234, vis_years= 1, ymax_animals=200)
sim.simulate(20)
plt.show()