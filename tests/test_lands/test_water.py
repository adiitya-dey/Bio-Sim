import pytest
from biosim.animals.carnivore import Carnivore
from biosim.land.water import Water
from biosim.animals.herbivore import Herbivore


@pytest.fixture()
def reset_params():
    """
    This test function resets the land parameters back to their default value
    after each test condition

    Returns
    -------

    """
    yield
    Water.set_land_params({"f_max": None})


def test_create_water(reset_params):
    """
    Testing create an Instance of Water class object

    Parameters
    ----------
    reset_params: dict
            reset parameters

    Notes
    ------
    - asserts fodder is equal to None
    Returns
    -------
    area.fodder == None is True

    """
    area = Water()
    assert area.fodder is None


@pytest.mark.parametrize("f_max", [0.1, 200, 201.15])
def test_update_params_success(f_max, reset_params):
    """
    Testing Update params success

    Parameters
    ----------
    f_max: float
        Fodder amount on land object
    reset_params: dict
        reset parameters

    Notes
    ------
    - Should not be allowed to set parameters into water class

    Returns
    -------

    Raises
    -------
    ValueError

    """
    with pytest.raises(ValueError):
        Water.set_land_params({"f_max": f_max})


@pytest.mark.parametrize("f_max", [-1, "abc"])
def test_update_params_fail(f_max, reset_params):
    """
    Testing update params fail conditions

    Parameters
    ----------
    f_max: float
        Fodder amount on land object
    reset_params: dict
        reset parameters

    Notes
    -------
    - using parametrize set f_max values to Negative and string
    - assert that it return a ValueError

    Returns
    -------

    Raises
    -------
    ValueError:
            f_max value is incorrect. Please use float or integer
    """
    with pytest.raises(ValueError):
        Water.set_land_params({"f_max": f_max})


def test_update_params_dict_fail(reset_params):
    """
    Testing update params dictionary fail conditions

    Parameters
    ----------
    reset_params: dict
        reset parameters

    Notes
    ------
    - Set wrong key value in dictionary
    - assert that it return a ValueError
    Returns
    -------

    Raises
    ------
    ValueError:
             Update params for land failed

    """
    with pytest.raises(ValueError):
        Water.set_land_params({"ff_max": 100})


def test_update_params_dict1_fail(reset_params):
    """
    Testing update params dictionary fail

    Parameters
    ----------
    reset_params: dict
        reset parameters

    Notes
    ------
    - Set argument as list not dictionary
    - assert returns value error

    Returns
    -------

    Raises
    -------

    ValueError:
            Update params for land failed
    """
    with pytest.raises(ValueError):
        Water.set_land_params(["ff_max", 100])


class TestWater:

    @pytest.fixture(autouse=True)
    def create(self):
        """
        Test creating Water Object

        Notes
        -----
        - Set water instance
        - Set neighbours

        Returns
        -------

        """
        self.terra = Water()
        self.terra.neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    @pytest.fixture
    def reset_params(self):
        yield
        Water.set_land_params({"f_max": None})
        Herbivore.update_params({"w_birth": 8.0,
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
        Carnivore.update_params({"w_birth": 6.0,
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

    @pytest.mark.parametrize("h_val, c_val", [(10, 5), (200, 100)])
    @pytest.mark.parametrize("herb_dict, carn_dict",
                             [({"species": "Herbivore",
                                "age": "30",
                                "weight": "50"},
                               {"species": "Carnivore",
                                "age": "5",
                                "weight": "20"})])
    def test_insert_pop_initial_herbivore(self, herb_dict, carn_dict, h_val, c_val):
        """
        Test insert Population into Water object

        Parameters
        ----------
         herb_dict: dict
                population list of herbivores
        carn_dict: dict
                population list of carnivores
        h_val: float
            number of herbivores to be inserted
        c_val:
            number of carnivores to be inserted
        reset_params: dict
                Parameters reset

        Returns
        -------

        Raises
        ------

        ValueError

        """
        with pytest.raises(ValueError):
            self.terra.insert_pop([herb_dict for _ in range(h_val)])

    @pytest.mark.parametrize("h_val, c_val", [(10, 5), (200, 100)])
    @pytest.mark.parametrize("herb_dict, carn_dict",
                             [({"species": "Herbivore",
                                "age": "30",
                                "weight": "50"},
                               {"species": "Carnivore",
                                "age": "5",
                                "weight": "20"})])
    def test_insert_pop_initial_carnivore(self, herb_dict, carn_dict, h_val, c_val):
        """
        Test insert Population into Water object

        Parameters
        ----------
         herb_dict: dict
                population list of herbivores
        carn_dict: dict
                population list of carnivores
        h_val: float
            number of herbivores to be inserted
        c_val:
            number of carnivores to be inserted
        reset_params: dict
                Parameters reset

        Returns
        -------

        Raises
        ------

        ValueError

        """
        with pytest.raises(ValueError):
            self.terra.insert_pop([carn_dict for _ in range(c_val)])

    @pytest.mark.parametrize("years", [10, 50, 100])
    def test_regrow(self, reset_params, years):
        """
         Testing fodder regrow function

         Parameters
         ----------
         reset_params: dict
                 Parameters reset

         years: int
                 Interation number


         Notes
         -----
         - assert each year that fodder value is None

         Returns
         -------
         self.terra.fodder == None
         """
        for _ in range(years):
            self.terra.feeding_cycle()
            self.terra.regrow()
            assert self.terra.fodder is None
