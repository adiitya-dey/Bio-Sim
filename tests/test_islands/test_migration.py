import pytest
from biosim.island import Island


@pytest.mark.parametrize('island, location', [("WWWWW\nWWLWW\nWLLLW\nWWLWW\nWWWWW", (3, 3)),
                                              ("WWWWW\nWWHWW\nWHHHW\nWWHWW\nWWWW", (3, 3)),
                                              ("WWWWW\nWWDWW\nWDDDW\nWWDWW\nWWWW", (3, 3))])
class TestIslandMigration:

    @pytest.fixture(autouse=True)
    def test_create(self, island, location):
        """
        Creating Island Object

        Parameters
        ----------
        island: dict
                An Island object
        location: tuple
                coordinates of land objects

        Returns
        -------

        Returns
        -------

        """
        self.continent = Island(island)
        self.continent.add_neighbors()
        self.loc = location
        self.continent.add_pop(self.loc, [{"species": "Herbivore",
                                           "age": "30",
                                           "weight": "50"} for _ in range(51)])
        self.continent.add_pop(self.loc, [{"species": "Carnivore",
                                           "age": "10",
                                           "weight": "30"} for _ in range(7)])
        self.continent.update_animal_island_values()

    @pytest.fixture
    def reset_params(self):
        """
        Resetting Class Parameter Value

        Returns
        -------

        """
        yield

        self.continent.update_params("landscape", 'L', {'f_max': 800})
        self.continent.update_params("landscape", 'H', {'f_max': 300})
        self.continent.update_params("landscape", 'D', {'f_max': 0})
        self.continent.update_params("animal", "Herbivore",
                                     {"w_birth": 8.0,
                                      "sigma_birth": 1.5,
                                      "beta": 0.9,
                                      "eta": 0.05,
                                      "a_half": 40.0,
                                      "phi_age": 0.6,
                                      "w_half": 10.0,
                                      "phi_weight": 0.1,
                                      "mu": 0.25,
                                      "gamma": 0.2,
                                      "zeta": 3.5,
                                      "xi": 1.2,
                                      "omega": 0.4,
                                      "F": 10.0,
                                      }
                                     )
        self.continent.update_params("animal", "Carnivore",
                                     {"w_birth": 6.0,
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
                                     )

    def test_annual_cycle_migration_all_migrate_prob_true(self, reset_params):
        """
        Testing Annual Cycle
        Validating Migration

        Parameters
        ----------


        reset_params: dict
            Parameters reset value

        Notes
        ------
        - Every animal migrates in every land object


        Returns
        -------
        len(self.continent.island[self.loc].pop_herbivore) == 0
        len(self.continent.island[self.loc].pop_carnivore) == 0


        """
        self.continent.update_params("animal", "Herbivore", {'mu': 10,
                                                             'gamma': 0,
                                                             'omega': 0})
        self.continent.update_params("animal", "Carnivore", {'mu': 10,
                                                             'gamma': 0,
                                                             'omega': 0})
        # 'DeltaPhiMax': 100})

        # self.continent.update_animal_min_weight()

        self.continent.annual_cycle()

        assert len(self.continent.island[self.loc].pop_herbivore) == 0
        assert len(self.continent.island[self.loc].pop_carnivore) == 0

    def test_annual_cycle_migration_all_migrate_prob_false(self, reset_params):
        """
        Testing Annual Cycle
        Validating Migration

        Parameters
        ----------

        reset_params: dict
            Parameters reset value

        Notes
        ------
        - No animal migrates in every land object

        Returns
        --------

        location_animal_count == total_count is True

        """
        self.continent.update_params("animal", "Herbivore", {'mu': 0.0001,
                                                             'gamma': 0,
                                                             'omega': 0})
        self.continent.update_params("animal", "Carnivore", {'mu': 0.0001,
                                                             'gamma': 0,
                                                             'omega': 0})

        total_count = self.continent.animal_count()
        # 'DeltaPhiMax': 100})

        # self.continent.update_animal_min_weight()

        self.continent.annual_cycle()

        location_animal_count = len(self.continent.island[self.loc].pop_herbivore) + \
                                len(self.continent.island[self.loc].pop_carnivore)
        assert location_animal_count == total_count
