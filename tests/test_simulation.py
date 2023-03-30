from biosim.animals.carnivore import Carnivore
from biosim.animals.herbivore import Herbivore
from biosim.simulation import BioSim
import pytest
from biosim.land.lowland import LowLand
from biosim.land.highland import HighLand


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
@pytest.fixture()
def reset_params(map1):
    """
    Resetting BioSim Class Parameter Value

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology

    Returns
    -------

    """

    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)
    sim.set_landscape_parameters('L', {"f_max": 800})
    sim.set_landscape_parameters('H', {"f_max": 300})
    sim.set_landscape_parameters('D', {"f_max": 0})
    sim.set_animal_parameters("Herbivore",
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
                               })
    sim.set_animal_parameters("Carnivore",
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
                               "DeltaPhiMax": 10.0})


@pytest.mark.parametrize("map1", [("WWW\nWXW\nWWW")])
def test_create_island_wrong_land_value(map1):
    """
    Testing Wrong Island Value

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology

    Returns
    -------

    Raises
    -------
    ValueError
    """
    with pytest.raises(ValueError):
        BioSim(map1, ini_pop=[], seed=1, vis_years=0)


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
def test_create_island(map1, reset_params):
    """
    Testing Island creation

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology

    Returns
    -------
    isinstance(land_mass, BioSim) is True

    """
    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)
    assert isinstance(sim, BioSim)


@pytest.mark.parametrize("map1, ", ["WWW\nWLW\nWWW",
                                    "WWW\nWHW\nWWW",
                                    "WWW\nWDW\nWWW"])
def test_add_pop_fail(map1, reset_params):
    """
    Multiple Add pop test for failure

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology
    reset_params: dict
            Parameters reset value

    Returns
    -------

    Raises
    ------
    ValueError

    """
    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)

    with pytest.raises(ValueError):
        sim.add_population([{'loc': (2, 2),
                             'pop': [{'spies': 'Herbivore',
                                      'age': 30,
                                      'weight': 50}
                                     for _ in range(2)]}])

    with pytest.raises(ValueError):
        sim.add_population([{'loc': (2, 2),
                             'pop': [{'species': 'Omnivore',
                                      'age': 30,
                                      'weight': 50}
                                     for _ in range(2)]}])

    with pytest.raises(ValueError):
        sim.add_population([{'loc': (2, 2),
                             'pop': [{'species': 'Herbivore',
                                      'aaage': 30,
                                      'weight': 50}
                                     for _ in range(2)]}])
    #
    # with pytest.raises(ValueError):
    #     sim.add_population([{'loc': (2, 2),
    #                          'pop': [{'species': 'Herbivore',
    #                                   'age': 30,
    #                                   'weight': 50}
    #                                  ]}])

    with pytest.raises(ValueError):
        sim.add_population([{'loc': (2, 2),
                             'pop': [{'species': 'Herbivore',
                                      'age': -1,
                                      'weight': 50}
                                     ]}])

    with pytest.raises(ValueError):
        sim.add_population([{'loc': (2, 2),
                             'pop': [{'species': 'Herbivore',
                                      'age': 30,
                                      'weight': -1}
                                     ]}])


@pytest.mark.parametrize("map1, ", ["WWW\nWLW\nWWW",
                                    "WWW\nWHW\nWWW",
                                    "WWW\nWDW\nWWW"])
@pytest.mark.parametrize("h_count, c_count", [(50, 5), (20, 100)])
def test_add_pop_success(map1, h_count, c_count, reset_params):
    """
    Testing add population function success

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology
    reset_params: dict
            Parameters reset value
    h_count: float
            Number of  herbivores inserted
    c_count: float
            Number of carnivores inserted

    Returns
    -------
    sim.num_animals_per_species["Herbivore"] == h_count is True
    sim.num_animals_per_species["Carnivore"] == c_count is True

    """
    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)

    sim.add_population([{'loc': (2, 2),
                         'pop': {}}])
    assert sim.num_animals_per_species["Herbivore"] == 0
    assert sim.num_animals_per_species["Carnivore"] == 0

    sim.add_population([{'loc': (2, 2),
                         'pop': [{'species': 'Herbivore',
                                  'age': 30,
                                  'weight': 50}
                                 for _ in range(h_count)]}])

    sim.add_population([{'loc': (2, 2),
                         'pop': [{'species': 'Carnivore',
                                  'age': 30,
                                  'weight': 50}
                                 for _ in range(c_count)]}])
    assert sim.num_animals_per_species["Herbivore"] == h_count
    assert sim.num_animals_per_species["Carnivore"] == c_count


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
def test_update_params_fail(map1, reset_params):
    """
    Testing parameter Update failing

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology
    reset_params: dict
            Parameters reset value

    Returns
    -------

    Raises
    -------
    ValueError

    """
    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)

    with pytest.raises(ValueError):
        sim.set_landscape_parameters('X', {'f_max': 800})

    with pytest.raises(ValueError):
        sim.set_landscape_parameters('L', {'ff_max': 800})

    with pytest.raises(ValueError):
        sim.set_landscape_parameters('L', {'f_max': None})

    with pytest.raises(ValueError):
        sim.set_landscape_parameters('H', {'ff_max': 100.0})

    with pytest.raises(ValueError):
        sim.set_landscape_parameters('D', {'f_max': 100.0})

    with pytest.raises(ValueError):
        sim.set_animal_parameters("Omnivore",
                                  {"w_birth": 8.0,
                                   "sigma_birth": 1.5})

    with pytest.raises(ValueError):
        sim.set_animal_parameters("Carnivore",
                                  {"ww_birth": 8.0,
                                   "sigma_birth": 1.5})

    with pytest.raises(ValueError):
        sim.set_animal_parameters("Carnivore",
                                  {"w_birth": -1.0,
                                   "sigma_birth": 1.5})


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
@pytest.mark.parametrize("years", [-1, "abc"])
def test_simulate_years(map1, reset_params, years):
    """
        Testing parameter simulate years

        Parameters
        ----------
        map1: str
                Geogr multiline string representing island topology
        reset_params: dict
                Parameters reset value

        Returns
        -------

        Raises
        -------
        ValueError

    """
    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)
    with pytest.raises(ValueError):
        sim.simulate(years)


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
def test_update_params_success(map1, reset_params):
    """
    Testing parameter update success

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology
    reset_params: dict
            Parameters reset value

    Returns
    -------
    LowLand.f_max == 700 is True
    HighLand.f_max == 100 is True
    Carnivore.params['w_birth'] == 4.0 is True
    Herbivore.params['w_birth'] == 10.0 is True
    """
    sim = BioSim(map1, ini_pop=[], seed=1, vis_years=0)

    sim.set_landscape_parameters('L', {'f_max': 700})
    assert LowLand.f_max == 700

    sim.set_landscape_parameters('H', {'f_max': 100})
    assert HighLand.f_max == 100

    sim.set_animal_parameters("Carnivore", {"w_birth": 4.0})
    assert Carnivore.params['w_birth'] == 4.0

    sim.set_animal_parameters("Herbivore", {"w_birth": 10.0})
    assert Herbivore.params['w_birth'] == 10.0


@pytest.mark.parametrize('island, location', [("WWWWW\nWWLWW\nWHDHW\nWWLWW\nWWWWW", (3, 3)),
                                              ("WWWWW\nWLLLW\nWHWHW\nWDDDW\nWWWWW", (2, 3)),
                                              ("WWW\nWLW\nWDW\nWHW\nWDW\nWWW", (3, 2))])
class TestBiosim:

    @pytest.fixture(autouse=True)
    def test_create(self, island, location):
        """
        Creating BioSim Object

        Parameters
        ----------
        island: dict
                An Island object
        location: tuple
                coordinates of land objects

        Returns
        -------


        """
        self.bio_simulate = BioSim(island, ini_pop=[], seed=1, vis_years=0)
        self.loc = location
        self.bio_simulate.add_population([{'loc': self.loc,
                                           'pop': [{'species': 'Herbivore',
                                                    'age': 30,
                                                    'weight': 50}
                                                   for _ in range(51)]}])
        self.bio_simulate.add_population([{'loc': self.loc,
                                           'pop': [{'species': 'Carnivore',
                                                    'age': 30,
                                                    'weight': 50}
                                                   for _ in range(7)]}])
        self.bio_simulate.map.update_animal_island_values()

    @pytest.fixture
    def setting_params(self):
        yield

        self.bio_simulate.set_landscape_parameters('L', {'f_max': 800})
        self.bio_simulate.set_landscape_parameters('H', {'f_max': 300})
        self.bio_simulate.set_landscape_parameters('D', {'f_max': 0})
        self.bio_simulate.set_animal_parameters("Herbivore",
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
        self.bio_simulate.set_animal_parameters("Carnivore",
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

    def test_simulate(self):
        """
        Testing Simulation function

        Returns
        -------

        """
        self.bio_simulate.simulate(2)

    @pytest.mark.parametrize("years", [1, 5, 9])
    def test_multi_simulate(self, years):
        """
        Testing multiple simulations

        Parameters
        ----------
        years: int
            Iterations

        Returns
        -------

        """

        self.bio_simulate.simulate(years)

    def test_num_of_animals(self):
        """
        Testing number of animals in simulation function

        Returns
        -------
        self.bio_simulate.num_animals == 58 is True
        """
        assert self.bio_simulate.num_animals == 58

    def test_num_of_species(self):
        """
        Test Number of animals per species in simulation

        Returns
        -------
        self.bio_simulate.num_animals_per_species["Herbivore"] == 51 is True
        self.bio_simulate.num_animals_per_species["Carnivore"] == 7 is True

        """
        assert self.bio_simulate.num_animals_per_species["Herbivore"] == 51
        assert self.bio_simulate.num_animals_per_species["Carnivore"] == 7

    @pytest.mark.parametrize("years", [1, 5, 9])
    def test_years(self, years):
        """
        Testing years function

        Parameters
        ----------
        years: int
           Iterations

        Returns
        -------
        self.bio_simulate.year == years is True
        """
        self.bio_simulate.simulate(years)
        assert self.bio_simulate.year == years
