
__author__ = 'Aditya dey, Okubadejo Olutomi, NMBU'

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

"""
This is an example of a  sample island to test the
Bio Simulation.

"""

if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLDDLLLLLLLWW
               WHHHHHHHHDDDLLLLLLWWW
               WHHHHHLDDWWDDLLLLLWWW
               WHHHHHLDDWWDDLHLLLWWW
               WHHLLLLDDWWDDLHHHHWWW
               WWHHHHLDDWWDDLHWWWWWW
               WHHHLLLDDWWDDLLLLLWWW
               WHHHHLLDDWWDDLLWWWWWW
               WWHHHHLLLDDLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (4, 6),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (4, 6),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 vis_years=10,
                 ymax_animals=30000,
                 cmax_animals={'Herbivore': 300, 'Carnivore': 150})

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 800})
    sim.set_landscape_parameters('H', {'f_max': 500})

    sim.simulate(num_years=100)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=300)
    print(f"Current Year: {sim.year}")
    print(f"Total number of Animals: {sim.num_animals}")
    print(f"Animals by species: \n{sim.num_animals_per_species}")
    plt.show()
    plt.savefig('check_sim.pdf')
