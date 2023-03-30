
__author__ = 'Aditya dey, Okubadejo Olutomi, NMBU'


import textwrap
from biosim.simulation import BioSim
from matplotlib import pyplot as plt

"""
A simple example of BioSim experiment, on a mono land 
with visualization enabled and saving images. Images are
saved based on img_years.

To plot images it is required to pass img_dir and img_base.
- img_dir is the image directory.
- img_base is the image name.

If img_dir and img_base is mentioned, and not img_years,
img_years will be equal to vis_years.
if img_years = 1, plot saved for each year.
if img_years = 3, plot saved every 3rd year.

Please use plt.show() at the end to keep the plot
in active mode, if you need to view the file on screen.
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

sim = BioSim(geogr, ini_herbs, seed=1234, img_years=1, ymax_animals=200, img_base='Biosim',
             img_dir='data')
sim.simulate(20)
plt.show()