
__author__ = 'Aditya dey, Okubadejo Olutomi, NMBU'


import textwrap
from biosim.simulation import BioSim

"""
A simple example of BioSim experiment, on a mono land
with no visuals.

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
                      for _ in range(50)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

sim = BioSim(geogr, ini_herbs + ini_carns, seed=1234, vis_years=0)
sim.simulate(10)
