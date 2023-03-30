import pytest
import random
from biosim.animals.carnivore import Carnivore
from biosim.land.desert import Desert
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
    Desert.set_land_params({"f_max": 0})


def test_create_desert(reset_params):
    """
    Testing create an Instance of Desert class object

    Parameters
    ----------
    reset_params: dict
            reset parameters

    Notes
    ------
    - This creates a desert instance
    - asserts fodder is equal to 0
    Returns
    -------
    area.fodder == 0 is True

    """
    area = Desert()
    assert area.fodder == 0


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
    - Sets f_max to 0 with the set_land_params function
    - asserts fodder and f_max are 0
    Returns
    -------

    """
    with pytest.raises(ValueError):
        Desert.set_land_params({"f_max": f_max})
    # area = Desert()
    # assert area.fodder == f_max
    # assert area.f_max == f_max


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
        Desert.set_land_params({"f_max": f_max})


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
        Desert.set_land_params({"ff_max": 100})


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
        Desert.set_land_params(["ff_max", 100])


@pytest.mark.parametrize("h_val, c_val", [(10, 5), (200, 100)])
@pytest.mark.parametrize("herb_dict, carn_dict",
                         [({"species": "Herbivore",
                            "age": "30",
                            "weight": "50"},
                           {"species": "Carnivore",
                            "age": "5",
                            "weight": "20"})])
def test_insert_pop_initial(herb_dict, carn_dict, h_val, c_val):
    """
    Inserting animal population list test

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

    Notes
    -----
    - We insert h_val amount of herbivore in herb_dict into Highland object
    - We insert c_val amount of carnivore in herb_dict into Highland object
    - assert herbivore and carnivore population list is equal to h_val and c_val
    - assert Average weight of herbivores and carnivores inserted is equal
      to weight value in herb_dict and carn_dict
    - assert Average age of herbivores and carnivores inserted is equal
      to age value in herb_dict and carn dict

    Returns
    -------

    """
    terra = Desert()
    terra.pop_herbivore = []
    terra.pop_carnivore = []
    terra.insert_pop([herb_dict for _ in range(h_val)])
    terra.insert_pop([carn_dict for _ in range(c_val)])

    assert len(terra.pop_herbivore) == h_val
    assert len(terra.pop_carnivore) == c_val

    assert sum([herb.age for herb
                in terra.pop_herbivore]) / len(terra.pop_herbivore) \
           == float(herb_dict["age"])
    assert sum([herb.weight for herb
                in terra.pop_herbivore]) / len(terra.pop_herbivore) \
           == float(herb_dict["weight"])

    assert sum([carn.age for carn
                in terra.pop_carnivore]) / len(terra.pop_carnivore) \
           == float(carn_dict["age"])
    assert sum([carn.weight for carn
                in terra.pop_carnivore]) / len(terra.pop_carnivore) \
           == float(carn_dict["weight"])


class TestDesert:
    """
    The test class for the Desert object
    """
    @pytest.fixture(autouse=True)
    def create(self):
        """
        Create a Desert object for the test class

        Notes
        -----
        - Create a Desert object
        - Set highland neighbours
        - insert 20 herbivores
        - insert 5 carnivores
        - update class parameters
        Returns
        -------
        """
        self.terra = Desert()
        self.terra.neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.terra.insert_pop([{"species": "Herbivore",
                                "age": "20",
                                "weight": "40"} for _ in range(20)])
        self.terra.insert_pop([{"species": "Carnivore",
                                "age": "15",
                                "weight": "35"} for _ in range(5)])
        Desert.update_animal_values()

    @pytest.fixture
    def reset_params(self):
        yield
        Desert.set_land_params({"f_max": 0})
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
    def test_insert_pop(self, h_val, c_val, herb_dict, carn_dict, reset_params):
        """
        Testing insert_pop function

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

        Notes
        -----
        - store current number of herbivores and carnivores in variables
        - insert h_val number of herbivores
        - insert c_val number of carnivores
        - assert new number of species = old number + h_val or c_val

        Returns
        -------
        len(self.terra.pop_herbivore) == current_size_herb + h_val is True
        len(self.terra.pop_carnivore) == current_size_carn + c_val is True

        """
        current_size_herb = len(self.terra.pop_herbivore)
        current_size_carn = len(self.terra.pop_carnivore)

        self.terra.insert_pop([herb_dict for _ in range(h_val)])
        self.terra.insert_pop([carn_dict for _ in range(c_val)])

        assert len(self.terra.pop_herbivore) == current_size_herb + h_val
        assert len(self.terra.pop_carnivore) == current_size_carn + c_val

    @pytest.mark.parametrize("years", [1, 5, 7, 13])
    def test_aging_cycle(self, years, reset_params):
        """
        Testing Highland object aging cycle

        Parameters
        ----------
        years: int
            Number of years to run aging cycle

        reset_params: dict
                Parameters reset

        Notes
        ------
        - Save current average age for herbivore and carnivore
        - Run aging cycle for N number of years
        - Save average age for herbivore and carnivore in different variables
        - assert new average age = old age + N

        Returns
        -------
        new_age_herb == current_age_herb + years is True
        new_age_carn == current_age_carn + years is True
        """
        current_age_herb = sum([herb.age
                                for herb in self.terra.pop_herbivore]) \
                           / len(self.terra.pop_herbivore)
        current_age_carn = sum([carn.age
                                for carn in self.terra.pop_carnivore]) \
                           / len(self.terra.pop_carnivore)

        for _ in range(years):
            self.terra.aging_cycle()

        new_age_herb = sum([herb.age
                            for herb in self.terra.pop_herbivore]) \
                       / len(self.terra.pop_herbivore)
        new_age_carn = sum([carn.age
                            for carn in self.terra.pop_carnivore]) \
                       / len(self.terra.pop_carnivore)

        assert new_age_herb == current_age_herb + years
        assert new_age_carn == current_age_carn + years

    def test_death_cycle_dead(self, reset_params, mocker):
        """
        Test death cycle all animals die

        Parameters
        ----------
        reset_params: dict
            Parameters reset
        mocker: float
            Randomness control

        Notes
        ------
        - Set mocker value to 0.00001

        ..code::

                probability = self.params["mu"] * self.phi
                if random.random() < probability:
                    return True
                else:
                    return False

        - Ensures every animal dies
        - Run death cycle
        - assert Herbivore and Carnivore list is empty
        - assert Migration lists are empty

        Returns
        -------
        len(self.terra.pop_herbivore) == 0 is True
        len(self.terra.pop_carnivore) == 0 is True

        """
        mocker.patch('random.random', return_value=0.00001)
        self.terra.death_cycle()

        assert len(self.terra.pop_herbivore) == 0
        assert len(self.terra.pop_carnivore) == 0

    def test_death_cycle_alive(self, reset_params, mocker):
        """

        Parameters
        ----------
        reset_params: dict
            Parameters reset
        mocker: float
            Randomness control

        Notes
        ------
        - save current number of animals in populations list
        - Set mocker value to 0.7

        ..code::

                        if self.weight == 0:
                            return True
                        elif random.random() < (self.params['omega'] * (1 - self.phi)):
                            return True
                        else:
                            return False


        - Run death cycle
        - assert Herbivore and Carnivore list is the same with initial list
        - assert Migration lists is the same with initial list

        Returns
        -------
        len(self.terra.pop_herbivore) == current_herb_pop
        len(self.terra.pop_carnivore) == current_carn_pop
        """

        mocker.patch('random.random', return_value=0.7)
        current_herb_pop = len(self.terra.pop_herbivore)
        current_carn_pop = len(self.terra.pop_carnivore)

        self.terra.death_cycle()

        assert len(self.terra.pop_herbivore) == current_herb_pop
        assert len(self.terra.pop_carnivore) == current_carn_pop

    @pytest.mark.parametrize("years", [10, 50, 100, 200])
    def test_death_cycle_parametric_alive(self, years, reset_params):
        """
        Testing death cycle
        no animal dies, controlling omega and eta

        Parameters
        ----------
        years: int
            Iteration number
        reset_params: dict
                Parameters reset

        Notes
        ------
        - set Omega to 0, this means the random value will always be higher
        - set eta to 0.1, reduces weight loss in animals

         ..code::

                        if self.weight == 0:
                            return True
                        elif random.random() < (self.params['omega'] * (1 - self.phi)):
                            return True
                        else:
                            return False

        - save current number of carnivores and herbivores
        - Run aging and death cycle for N number of years
        - assert number of carnivores and herbivores does not change

        Returns
        -------
        len(self.terra.pop_herbivore) == current_herb_pop is True
        len(self.terra.pop_carnivore) == current_carn_pop is True

        """
        self.terra.set_animal_params("Herbivore", {"omega": 0,
                                                   "eta": 0.1})
        self.terra.set_animal_params("Carnivore", {"omega": 0,
                                                   "eta": 0.1})

        current_herb_pop = len(self.terra.pop_herbivore)
        current_carn_pop = len(self.terra.pop_carnivore)
        current_migrate_herb = len(self.terra.migrate_pop_herbivore)
        current_migrate_carn = len(self.terra.migrate_pop_carnivore)

        for _ in range(years):
            self.terra.aging_cycle()
            self.terra.death_cycle()

        assert len(self.terra.pop_herbivore) == current_herb_pop
        assert len(self.terra.pop_carnivore) == current_carn_pop
        assert len(self.terra.migrate_pop_herbivore) == current_migrate_herb
        assert len(self.terra.migrate_pop_carnivore) == current_migrate_carn

    @pytest.mark.parametrize("years", [50, 100])
    def test_death_cycle_parametric_dead(self, years, reset_params):
        """
        Testing death cycle
        every animal die, controlling omega

        Parameters
        ----------
        years: int
            Iteration number
        reset_params: dict
                Parameters reset

        Notes
        ------
        - set Omega to 0.5, this means the random value will always be lower
          than death probability

         ..code::

                        if self.weight == 0:
                            return True
                        elif random.random() < (self.params['omega'] * (1 - self.phi)):
                            return True
                        else:
                            return False

        - save current number of carnivores and herbivores
        - Run aging and death cycle for N number of years
        - assert number of carnivores and herbivores is less than old number

        Returns
        -------
        len(self.terra.pop_herbivore) < current_herb_pop is True
        len(self.terra.pop_carnivore) < current_carn_pop is True
        """
        self.terra.set_animal_params("Herbivore", {"omega": 0.5})
        self.terra.set_animal_params("Carnivore", {"omega": 0.5})

        current_herb_pop = len(self.terra.pop_herbivore)
        current_carn_pop = len(self.terra.pop_carnivore)

        for _ in range(years):
            self.terra.aging_cycle()
            self.terra.death_cycle()

        assert len(self.terra.pop_herbivore) < current_herb_pop
        assert len(self.terra.pop_carnivore) < current_carn_pop

    @pytest.mark.parametrize("years", [10, 50, 100])
    def test_birth_cycle_no_child(self, reset_params, mocker, years):
        """
        Testing Birth cycle no child is born

        Parameters
        ----------
        reset_params: dict
                Parameters reset
        mocker: float
                Randomness control
        years: int
                Interation number

        Notes
        ------
        - Set random to 1.1 using mocker

        ..code::

                        prob_birth = random.random()


                        land_birth_prob = min(1, animal.params["gamma"] *
                                              animal.phi * (len(pop) - 1))

                        if prob_birth < land_birth_prob:

        - Save current number carnivore and herbivore
        - Run birth cycle for N number of years
        - assert no child is born

        Returns
        -------
        len(self.terra.pop_herbivore) == current_herb_pop is True
        len(self.terra.pop_carnivore) == current_carn_pop is True

        """

        mocker.patch('random.random', return_value=1.1)
        current_herb_pop = len(self.terra.pop_herbivore)
        current_carn_pop = len(self.terra.pop_carnivore)

        for _ in range(years):
            self.terra.birth_cycle()

        assert len(self.terra.pop_herbivore) == current_herb_pop
        assert len(self.terra.pop_carnivore) == current_carn_pop

    @pytest.mark.parametrize("years", [10, 50, 100])
    def test_birth_cycle_child_born(self, reset_params, mocker, years):

        """

        Testing Birth cycle child is born

        Parameters
        ----------
        reset_params: dict
                Parameters reset
        mocker: float
                Randomness control
        years: int
                Interation number

        Notes
        ------
        - Set random to 0.1 using mocker

        ..code::

                        prob_birth = random.random()


                        land_birth_prob = min(1, animal.params["gamma"] *
                                              animal.phi * (len(pop) - 1))

                        if prob_birth < land_birth_prob:

        - Save current number carnivore and herbivore
        - Run birth cycle for N number of years
        - assert  child is born

        Returns
        -------
        len(self.terra.pop_herbivore) > current_herb_pop is True
        len(self.terra.pop_carnivore) > current_carn_pop is True

        """
        mocker.patch('random.random', return_value=0.5)
        current_herb_pop = len(self.terra.pop_herbivore)
        current_carn_pop = len(self.terra.pop_carnivore)

        for _ in range(years):
            self.terra.birth_cycle()

        assert len(self.terra.pop_herbivore) > current_herb_pop
        assert len(self.terra.pop_carnivore) > current_carn_pop

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
        - Save current fodder value
        - For N number of years run feeding cycle and regrow function
        - assert each year that fodder value has been reset to initial value

        Returns
        -------
        self.terra.fodder == fodder_max is True
        """
        fodder_max = self.terra.fodder

        for _ in range(years):
            self.terra.feeding_cycle()
            self.terra.regrow()
            assert self.terra.fodder == fodder_max

    @pytest.mark.parametrize("years", [10, 50])
    def test_feeding_cycle(self, reset_params, years):
        """
         Testing feeding cycle

         Parameters
         -----------

         reset_params: dict
                 Parameters reset

         years: int
                 Interation number

         Notes
         ------
         - Set random seed value to 123
         - Save current average weight of Carnivores and herbivores
         - Save current number carnivores and herbivores
         - Run feeding cycle for N number of years
         ..code::

                 self.weight += self.params["beta"] * food

         - assert new average weight > previous average weight for
           carnivores and herbivores
         - assert herbivores count > old count
         - assert number of carnivores does not change
         - assert all fodder is eaten

         Returns
         -------
         new_avg_weight_herb > current_avg_weight_herb is True
         new_avg_weight_carn > current_avg_weight_carn is True

         new_size_herb < current_size_herb is True
         new_size_carn == current_size_carn is True

         self.terra.fodder == 0 is True
         """
        # fodder_max = self.terra.fodder
        random.seed(123)
        current_avg_weight_herb = sum([herb.weight
                                       for herb in self.terra.pop_herbivore]) \
                                  / len(self.terra.pop_herbivore)

        current_avg_weight_carn = sum([carn.weight
                                       for carn in self.terra.pop_carnivore]) \
                                  / len(self.terra.pop_carnivore)

        current_size_herb = len(self.terra.pop_herbivore)
        current_size_carn = len(self.terra.pop_carnivore)

        for _ in range(years):
            self.terra.feeding_cycle()

        new_avg_weight_herb = sum([herb.weight
                                   for herb in self.terra.pop_herbivore]) \
                              / len(self.terra.pop_herbivore)

        new_avg_weight_carn = sum([carn.weight
                                   for carn in self.terra.pop_carnivore]) \
                              / len(self.terra.pop_carnivore)

        new_size_herb = len(self.terra.pop_herbivore)
        current_size_carn = len(self.terra.pop_carnivore)
        new_size_carn = len(self.terra.pop_carnivore)

        assert new_avg_weight_herb == current_avg_weight_herb
        assert new_avg_weight_carn > current_avg_weight_carn

        assert new_size_herb < current_size_herb
        assert new_size_carn == current_size_carn

    @pytest.mark.parametrize("years", [10, 50])
    def test_migration_cycle(self, reset_params, years):
        """
        Testing Migration cycle

        Parameters
        ----------
        reset_params: dict
                Parameters reset

        years: int
                Interation number

        Notes
        ------
        - Save current number of carnivores and herbivores
        - Run migration cycle for N number of years
        - assert at least one animal migrates

        Returns
        -------
        len(self.terra.pop_herbivore) < current_size_herb is True
        len(self.terra.pop_carnivore) < current_size_carn is True

        """

        current_size_herb = len(self.terra.pop_herbivore)
        current_size_carn = len(self.terra.pop_carnivore)

        for _ in range(years):
            self.terra.migration_cycle()

        assert len(self.terra.pop_herbivore) < current_size_herb
        assert len(self.terra.pop_carnivore) < current_size_carn

    @pytest.mark.parametrize("coordinates", [(1, 0), (-1, 0), (0, 1), (0, -1)])
    def test_migration_cycle_coordinates(self, reset_params, mocker, coordinates):
        """
        Testing Migration cycle coordinates selection

        Parameters
        ----------
        reset_params: dict
                Parameters reset
        mocker: float
            Randomness control
        coordinates: tuple
                migration locations


        Returns
        -------
        len(migration_herb) == 1 is True
        len(migration_carn) == 1 is True
        dict_location_herb[0] == coordinates is True
        dict_location_carn[0] == coordinates is True
        """
        mocker.patch("random.choice", return_value=coordinates)

        migration_herb, migration_carn = self.terra.migration_cycle()

        assert len(migration_herb) == 1
        assert len(migration_carn) == 1

        dict_location_herb = [key for key in migration_herb]
        dict_location_carn = [key for key in migration_carn]

        assert dict_location_herb[0] == coordinates
        assert dict_location_carn[0] == coordinates
