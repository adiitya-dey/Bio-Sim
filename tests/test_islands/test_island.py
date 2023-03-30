from biosim.animals.carnivore import Carnivore
from biosim.animals.herbivore import Herbivore
from biosim.island import Island
import pytest
from biosim.land.lowland import LowLand
from biosim.land.desert import Desert
from biosim.land.highland import HighLand


@pytest.fixture()
def reset_params():
    """
    Resetting Class Parameter Value

    Returns
    -------

    """
    LowLand.set_land_params({"f_max": 800})
    HighLand.set_land_params({"f_max": 300})
    Desert.set_land_params({"f_max": 0})
    LowLand.set_animal_params("Herbivore",
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
    LowLand.set_animal_params("Carnivore",
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
def test_create_island_wrong_land_value(map1, reset_params):
    """
    Testing Wrong Island Value

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
    with pytest.raises(ValueError):
        Island(map1)


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
def test_create_island(map1, reset_params):
    """
    Testing Island creation

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology
    reset_params: dict
            Parameters reset value

    Returns
    -------
    isinstance(land_mass, Island) is True

    """
    land_mass = Island(map1)
    assert isinstance(land_mass, Island)


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
    land_mass = Island(map1)

    with pytest.raises(ValueError):
        land_mass.add_pop((1, 1), [{"species": "Herbivore",
                                    "age": 30,
                                    "weight": 50} for _ in range(2)])

    with pytest.raises(ValueError):
        land_mass.add_pop((2, 2), [{"spies": "Herbivore",
                                    "age": 30,
                                    "weight": 50} for _ in range(2)])

    with pytest.raises(ValueError):
        land_mass.add_pop((2, 2), [{"species": "Omnivore",
                                    "age": 30,
                                    "weight": 50} for _ in range(2)])

    with pytest.raises(ValueError):
        land_mass.add_pop((2, 2), [{"species": "Herbivore",
                                    "aaage": 30,
                                    "weight": 50} for _ in range(2)])

    with pytest.raises(ValueError):
        land_mass.add_pop((2, 2), {"species": "Herbivore",
                                   "age": 30,
                                   "weight": 50})

    with pytest.raises(ValueError):
        land_mass.add_pop((2, 2), [{"species": "Herbivore",
                                    "age": -1,
                                    "weight": 50}])

    with pytest.raises(ValueError):
        land_mass.add_pop((2, 2), [{"species": "Herbivore",
                                    "age": 10,
                                    "weight": -1}])


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
    len(land_mass.island[(2, 2)].pop_herbivore) == h_count is True
    len(land_mass.island[(2, 2)].pop_carnivore) == c_count is True

    """
    land_mass = Island(map1)

    land_mass.add_pop((2, 2), [])
    assert len(land_mass.island[(2, 2)].pop_herbivore) == 0
    assert len(land_mass.island[(2, 2)].pop_herbivore) == 0

    land_mass.add_pop((2, 2), [{"species": "Herbivore",
                                "age": "30",
                                "weight": "50"} for _ in range(h_count)])
    land_mass.add_pop((2, 2), [{"species": "Carnivore",
                                "age": "30",
                                "weight": "50"} for _ in range(c_count)])
    assert len(land_mass.island[(2, 2)].pop_herbivore) == h_count
    assert len(land_mass.island[(2, 2)].pop_carnivore) == c_count


@pytest.mark.parametrize("map1", [("WWW\nWLW\nWWW")])
def test_add_neighbors(map1, reset_params):
    """
    Testing Land objects adding neighbours

    Parameters
    ----------
    map1: str
            Geogr multiline string representing island topology
    reset_params: dict
            Parameters reset value

    Returns
    -------
    sorted(land_mass.island[(2, 2)].neighbors) \
           == sorted([(1, 2), (3, 2), (2, 1), (2, 3)]) is True

    sorted(land_mass.island[(1, 1)].neighbors) == \
           sorted([(1, 2), (2, 1)]) is True

    sorted(land_mass.island[(2, 1)].neighbors) == \
           sorted([(1, 1), (2, 2), (3, 1)]) is True


    """
    land_mass = Island(map1)
    land_mass.add_neighbors()
    assert sorted(land_mass.island[(2, 2)].neighbors) \
           == sorted([(1, 2), (3, 2), (2, 1), (2, 3)])

    assert sorted(land_mass.island[(1, 1)].neighbors) == \
           sorted([(1, 2), (2, 1)])

    assert sorted(land_mass.island[(2, 1)].neighbors) == \
           sorted([(1, 1), (2, 2), (3, 1)])


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
    land_mass = Island(map1)

    with pytest.raises(ValueError):
        land_mass.update_params("landscape", 'X', {'f_max': 800})

    with pytest.raises(ValueError):
        land_mass.update_params("landscape", 'L', {'ff_max': 800})

    with pytest.raises(ValueError):
        land_mass.update_params("landscape", 'L', {'f_max': None})

    with pytest.raises(ValueError):
        land_mass.update_params("landscape", 'H', {'ff_max': 100.0})

    with pytest.raises(ValueError):
        land_mass.update_params("landscape", 'D', {'f_max': 100.0})

    with pytest.raises(ValueError):
        land_mass.update_params("animal", "Omnivore",
                                {"w_birth": 8.0,
                                 "sigma_birth": 1.5})

    with pytest.raises(ValueError):
        land_mass.update_params("animal", "Carnivore",
                                {"ww_birth": 8.0,
                                 "sigma_birth": 1.5})

    with pytest.raises(ValueError):
        land_mass.update_params("animal", "Carnivore",
                                {"w_birth": -1.0,
                                 "sigma_birth": 1.5})


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
    land_mass = Island(map1)

    land_mass.update_params("landscape", 'L', {'f_max': 700})
    assert LowLand.f_max == 700

    land_mass.update_params("landscape", 'H', {'f_max': 100})
    assert HighLand.f_max == 100

    land_mass.update_params("animal", "Carnivore", {"w_birth": 4.0})
    assert Carnivore.params['w_birth'] == 4.0

    land_mass.update_params("animal", "Herbivore", {"w_birth": 10.0})
    assert Herbivore.params['w_birth'] == 10.0


@pytest.mark.parametrize('island, location', [("WWWWW\nWWLWW\nWHDHW\nWWLWW\nWWWWW", (3, 3)),
                                              ("WWWWW\nWLLLW\nWHWHW\nWDDDW\nWWWW", (2, 3)),
                                              ("WWW\nWLW\nWDW\nWHW\nWDW\nWWW", (3, 2))])
class TestIsland:

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

    @pytest.fixture
    def backup_params(self):
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
        self.continent.update_animal_island_values()

    @pytest.mark.parametrize("years", [1, 5, 10])
    def test_annual_cycle_aging(self, years, backup_params):
        """
        Testing annual cycle
        focussing on validating aging cycle

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        herbivore_new_avg_age == herbivore_current_avg_age + years is True
        carnivore_new_avg_age == carnivore_current_avg_age + years is True

        """
        # random.seed(12345)
        self.continent.update_params("animal", "Herbivore", {'gamma': 0,
                                                             'omega': 0,
                                                             # 'mu': 0,
                                                             'eta': 0.001})
        self.continent.update_params("animal", "Carnivore", {'gamma': 0,
                                                             'omega': 0,
                                                             'F': 0,
                                                             # 'mu': 0,
                                                             'eta': 0.001})
        animal_values = self.continent.get_histogram()

        herbivore_current_avg_age = sum(animal_values["Herbivore"]["age"]) \
                                    / len(animal_values["Herbivore"]["age"])
        carnivore_current_avg_age = sum(animal_values["Carnivore"]["age"]) \
                                    / len(animal_values["Carnivore"]["age"])

        for _ in range(years):
            self.continent.annual_cycle()

        animal_values = self.continent.get_histogram()

        herbivore_new_avg_age = sum(animal_values["Herbivore"]["age"]) \
                                / len(animal_values["Herbivore"]["age"])
        carnivore_new_avg_age = sum(animal_values["Carnivore"]["age"]) \
                                / len(animal_values["Carnivore"]["age"])

        assert herbivore_new_avg_age == herbivore_current_avg_age + years
        assert carnivore_new_avg_age == carnivore_current_avg_age + years

    @pytest.mark.parametrize("years", [1, 5, 9])
    def test_annual_cycle_aging_weight_loss(self, years, backup_params):
        """
        Testing Annual cycle
        Validating weight loss

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        herbivore_new_avg_weight < herbivore_current_avg_weight is True
        carnivore_new_avg_weight < carnivore_current_avg_weight is True

        """
        self.continent.update_params("animal", "Herbivore", {'gamma': 0,
                                                             'omega': 0,
                                                             # 'mu': 0,
                                                             'eta': 0.001})
        self.continent.update_params("animal", "Carnivore", {'gamma': 0,
                                                             'omega': 0,
                                                             'F': 0,
                                                             # 'mu': 0,
                                                             'eta': 0.001})
        self.continent.update_params("landscape", "L", {"f_max": 0})
        self.continent.update_params("landscape", "H", {"f_max": 0})

        animal_values = self.continent.get_histogram()

        herbivore_current_avg_weight = sum(animal_values["Herbivore"]["weight"]) \
                                       / len(animal_values["Herbivore"]["weight"])
        carnivore_current_avg_weight = sum(animal_values["Carnivore"]["weight"]) \
                                       / len(animal_values["Carnivore"]["weight"])

        for _ in range(years):
            self.continent.annual_cycle()

        animal_values = self.continent.get_histogram()

        herbivore_new_avg_weight = sum(animal_values["Herbivore"]["weight"]) \
                                   / len(animal_values["Herbivore"]["weight"])
        carnivore_new_avg_weight = sum(animal_values["Carnivore"]["weight"]) \
                                   / len(animal_values["Carnivore"]["weight"])

        assert herbivore_new_avg_weight < herbivore_current_avg_weight
        assert carnivore_new_avg_weight < carnivore_current_avg_weight

    @pytest.mark.parametrize("years", [1, 7])
    def test_annual_cycle_birthing_no_child_herbivore(self, backup_params, years):

        """
        Testing Annual cycle
        Validating no child is born herbivore

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        current_total_count["Herbivore"] < new_total_count["Herbivore"]
        """
        self.continent.update_params("animal", "Herbivore", {'zeta': 10,
                                                             'omega': 0})
        self.continent.update_params("animal", "Carnivore", {'zeta': 10,
                                                             'omega': 0,
                                                             'F': 0})
        # 'DeltaPhiMax': 100})

        self.continent.update_animal_island_values()
        current_total_count = self.continent.num_animals_species

        for _ in range(years):
            self.continent.annual_cycle()

        new_total_count = self.continent.num_animals_species

        assert current_total_count["Herbivore"] == new_total_count["Herbivore"]

    @pytest.mark.parametrize("years", [1, 5, 7])
    def test_annual_cycle_birthing_child_birth_herbivore(self, backup_params, years):
        """
        Testing Annual cycle
        Validating childbirth herbivore

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        current_total_count["Herbivore"] < new_total_count["Herbivore"] is True
        """
        self.continent.update_params("animal", "Herbivore", {
            'omega': 0})
        self.continent.update_params("animal", "Carnivore", {
            'omega': 0,
            'F': 0})
        # 'DeltaPhiMax': 100})

        self.continent.update_animal_island_values()
        current_total_count = self.continent.num_animals_species

        for _ in range(years):
            self.continent.annual_cycle()

        new_total_count = self.continent.num_animals_species

        assert current_total_count["Herbivore"] < new_total_count["Herbivore"]

    @pytest.mark.parametrize("years", [1, 5, 7])
    def test_annual_cycle_birthing_no_child_carnivore(self, backup_params, years):
        """
        Testing Annual cycle
        Validating no childbirth carnivore

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        current_total_count["Carnivore"] == new_total_count["Carnivore"] is True
        """
        self.continent.update_params("animal", "Herbivore", {'omega': 0})
        self.continent.update_params("animal", "Carnivore", {'zeta': 30,
                                                             'omega': 0,
                                                             })
        # 'DeltaPhiMax': 100})

        self.continent.update_animal_island_values()
        current_total_count = self.continent.num_animals_species

        for _ in range(years):
            self.continent.annual_cycle()

        new_total_count = self.continent.num_animals_species

        assert current_total_count["Carnivore"] == new_total_count["Carnivore"]

    @pytest.mark.parametrize("years", [1, 5, 7])
    def test_annual_cycle_birthing_child_birth_carnivore(self, backup_params, years):
        """

        Testing Annual cycle
        Validating childbirth carnivore

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        current_total_count["Carnivore"] < new_total_count["Carnivore"] is True

        """
        self.continent.update_params("animal", "Herbivore", {'omega': 0})
        self.continent.update_params("animal", "Carnivore", {'omega': 0})
        # 'DeltaPhiMax': 100})

        self.continent.update_animal_island_values()
        current_total_count = self.continent.num_animals_species

        for _ in range(years):
            self.continent.annual_cycle()

        new_total_count = self.continent.num_animals_species

        assert current_total_count["Carnivore"] < new_total_count["Carnivore"]

    @pytest.mark.parametrize("years", [10, 23])
    def test_annual_cycle_death(self, backup_params, years):
        """
        Testing Annual cycle
        validating Death

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        current_total_count["Herbivore"] > new_total_count["Herbivore"] is True
        current_total_count["Carnivore"] > new_total_count["Carnivore"] is True

        """
        self.continent.update_params("animal", "Herbivore", {
            'gamma': 0})
        self.continent.update_params("animal", "Carnivore", {
            'gamma': 0,
            'F': 0})
        # 'DeltaPhiMax': 100})

        # self.continent.update_animal_min_weight()
        current_total_count = self.continent.num_animals_species

        for _ in range(years):
            self.continent.annual_cycle()

        new_total_count = self.continent.num_animals_species

        assert current_total_count["Herbivore"] > new_total_count["Herbivore"]
        assert current_total_count["Carnivore"] > new_total_count["Carnivore"]

    @pytest.mark.parametrize("years", [3, 5, 9])
    def test_annual_cycle_feeding_herbivore(self, backup_params, years):
        """
        Testing annual cycle
        Validating herbivore feeding cycle

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        herbivore_new_avg_weight > herbivore_current_avg_weight is True
        """
        self.continent.update_params("animal", "Herbivore", {'omega': 0,
                                                             'gamma': 0,
                                                             'eta': 0})
        self.continent.update_params("animal", "Carnivore", {'omega': 0,
                                                             'gamma': 0,
                                                             'eta': 0,
                                                             'F': 0})
        animal_values = self.continent.get_histogram()

        herbivore_current_avg_weight = sum(animal_values["Herbivore"]["weight"]) \
                                       / len(animal_values["Herbivore"]["weight"])

        for _ in range(years):
            self.continent.annual_cycle()

        animal_values = self.continent.get_histogram()

        herbivore_new_avg_weight = sum(animal_values["Herbivore"]["weight"]) \
                                   / len(animal_values["Herbivore"]["weight"])

        assert herbivore_new_avg_weight > herbivore_current_avg_weight

    @pytest.mark.parametrize("years", [3, 5, 9])
    def test_annual_cycle_feeding_carnivore(self, backup_params, years):
        """

        Testing annual cycle
        Validating herbivore feeding cycle

        Parameters
        ----------
        years: int
            Number of iterations

        backup_params: dict
                Parameters for reset

        Returns
        -------
        carnivore_new_avg_weight > carnivore_current_avg_weight is True
        """

        self.continent.update_params("animal", "Herbivore", {'omega': 0,

                                                             })
        self.continent.update_params("animal", "Carnivore", {'omega': 0,
                                                             'gamma': 0,
                                                             'eta': 0,
                                                             })
        animal_values = self.continent.get_histogram()

        carnivore_current_avg_weight = sum(animal_values["Carnivore"]["weight"]) \
                                       / len(animal_values["Carnivore"]["weight"])

        for _ in range(years):
            self.continent.annual_cycle()

        animal_values = self.continent.get_histogram()

        carnivore_new_avg_weight = sum(animal_values["Carnivore"]["weight"]) \
                                   / len(animal_values["Carnivore"]["weight"])

        assert carnivore_new_avg_weight > carnivore_current_avg_weight
