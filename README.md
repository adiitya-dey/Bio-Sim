Project Description:

Rossumoya is a small island in the middle of the vast ocean that belongs to the island nation of Pylandia. The ecosystem on Rossumoya is relatively undisturbed, but Pylandias Environmental Protection Agency wants to study the stability of the ecosystem. The long term goal is to preserve Rossumoya as a nature park for future generations. The ecosystem on Rossumoya is characterized by several different landscape types, lowland, highland and desert. The fauna includes only two species, one species of herbivores (plant eaters), and one of carnivores (predators).

The goal of this project a simulation of Russumoya, which would simulate the factors that could affect the island and its inhabitants to study how the island progresses and the animals survive



Notes for Hans:
1 - All requirements have been added and all functionalities
are working. Mono_ho, hc, sample_sim, check_sim and sample_sim 
for 1000 years have close results and running successfully. 

2 - If using vis_years > 0, please ensure to use plt.show() at
the end to stop the plot from closing after program is completed.
Refer to examples\mono_with_visual.py

3 - Tox fails for test_biosim_interface.py at
    test_configure_histograms[age-config1] and,
    test_figure_saved.
But the same file runs successfully when directly running from
PyCharm. 

ERROR: " _tkinter.TclError:" seems to be an 
environment error and hard to fix, since PyCharm does not 
throw errors.

4 - test_migration.py is not being picked up by sphinx

5- "continuation line over-indented for visual indent" - flake8 error
PyCharm was not giving better recommendation to solve it.
