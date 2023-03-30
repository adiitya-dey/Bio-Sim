import pytest
from biosim.animals.herbivore import Herbivore
import math
import scipy.stats as stats


@pytest.fixture
def re_update_params():
    """
    Tests update_params function in the animal class, using a set of values

    Returns
    -------

    """
    yield
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


@pytest.mark.parametrize("age, weight", [(-1, 8.0),
                                         (14, -1.0),
                                         (1.1, 8.0)])
def test_create_non_negative(age, weight, re_update_params):
    """
    Test to see if the checks for age and weight are working properly by parsing negative age
    and weight


    Parameters
    ----------
    age:int
        age of animal
    weight:float
        weight of animal
    re_update_params:dict
         reset class parameters

    Returns
    -------

    Raises
    ------
    ValueError: str
                Age cannot be less than zero when initialized.
    """
    with pytest.raises(ValueError):
        Herbivore(age, weight)


@pytest.mark.parametrize("age, weight", [(None, 8.0)])
def test_create_with_age_none(age, weight, re_update_params):
    """
    Check if the code throws an error for a None age

    Parameters
    ----------
    age: int
        age of animal
    weight: float
        weight of animal
    re_update_params: dict
            reset class parameters

    Returns
    -------
    assert herb1.age == 0  is True
    assert herb1.weight == weight is True
    """
    herb1 = Herbivore(age, weight)
    assert herb1.age == 0
    assert herb1.weight == weight


@pytest.mark.parametrize("age, weight", [(5, None)])
def test_create_with_weight_none(age, weight, re_update_params):
    """
     Check if the code throws an error for a None weight

    Parameters
    ----------
    age : int
        age of animal
    weight : float
        weight of animal
    re_update_params : dict
        reset class parameters

    Returns
    -------

    Raises
    ------
    ValueError: str
            Weight cannot be None. Please enter a positive real number.
    """
    with pytest.raises(ValueError):
        Herbivore(age, weight)


@pytest.mark.parametrize("age, weight", [("abc", 8.0),
                                         (14, "abc")])
def test_create_with_strings(age, weight, re_update_params):
    """
    check if the code throws an error for string values

    Parameters
    ----------
    age: int
        age of animal
    weight:float
        weight of animal
    re_update_params: dict
        reset class parameters

    Returns
    -------

    Raises
    ------
    ValueError:
            Weight needs to be a float or integer.
    """
    with pytest.raises(ValueError):
        Herbivore(age, weight)


@pytest.mark.parametrize("key", ["w_birth",
                                 "sigma_birth",
                                 "beta",
                                 "a_half",
                                 "phi_age",
                                 "w_half",
                                 "phi_weight",
                                 "mu",
                                 "gamma",
                                 "zeta",
                                 "xi",
                                 "omega",
                                 "F",
                                 ])
@pytest.mark.parametrize("value", [0, 0.5, 1, 2])
def test_set_params_success(key, value, re_update_params):
    """
    Testing success of setting parameters


    Parameters
    ----------
    key: str
        parameter keys
    value: float
        parameter values
    re_update_params: dict
        reset parameter values

    Returns
    -------
    Herbivore.params[key] == value is True

    """
    Herbivore.update_params({key: value})
    assert Herbivore.params[key] == value


@pytest.mark.parametrize("key", ["w_birth",
                                 "sigma_birth",
                                 "beta",
                                 "a_half",
                                 "phi_age",
                                 "w_half",
                                 "phi_weight",
                                 "mu",
                                 "gamma",
                                 "zeta",
                                 "xi",
                                 "omega",
                                 "F",
                                 ])
@pytest.mark.parametrize("value", [-1, "abc"])
def test_set_params_fail(key, value, re_update_params):
    """
    Testing failure of setting parameters

    Parameters
    ----------
    key: str
        parameter keys
    value: float
        parameter values
    re_update_params: dict
        reset parameter values

    Notes
    -----

    Should fail because a negative value and a string is parsed in

    Returns
    -------

    Raises
    ------
    ValueError:
        parameter value is not integer or float
        value has to be greater than 0

    """
    with pytest.raises(ValueError):
        Herbivore.update_params({key: value})


@pytest.mark.parametrize("key, value", [("DeltaPhiMax", 1),
                                        ("DeltaPhiMax", 0.1)])
def test_set_params_delta_phi_max_not_success(key, value, re_update_params):
    """
    updating DeltaPhiMax test

    Parameters
    ----------

    key: str
        parameter keys
    value: float
        parameter values
    re_update_params: dict
        reset parameter values

    Returns
    -------
    Herbivore.params[key] == value is True

    """
    with pytest.raises(ValueError):
        Herbivore.update_params({key: value})


@pytest.mark.parametrize("key, value", [("DeltaPhiMax", 0),
                                        ("DeltaPhiMax", -1),
                                        ("DeltaPhiMax", "abc")])
def test_set_params_delta_phi_max_fail(key, value, re_update_params):
    """
    Testing Deltaphimax parameter update failure

    Parameters
    ----------
    key: str
        parameter keys
    value: float
        parameter values
    re_update_params: dict
        reset parameter values

    Notes
    -----
    - Negative value and string parsed in should pop out an error

    Returns
    -------

    Raises
    ------
    ValueError:

        parameter value is not integer or float
        value has to be greater than 0
    """

    with pytest.raises(ValueError):
        Herbivore.update_params({key: value})


@pytest.mark.parametrize("key, value", [("eta", 0.4),
                                        ("eta", 0),
                                        ("eta", 1)])
def test_set_params_eta_success(key, value, re_update_params):
    """
    Testing Eta parameter update success

    Parameters
    ----------
    key: str
        parameter keys
    value: float
        parameter values
    re_update_params: dict
        reset parameter values


    Returns
    -------
    Herbivore.params[key] == value is True
    """
    Herbivore.update_params({key: value})
    assert Herbivore.params[key] == value


@pytest.mark.parametrize("key, value", [("eta", -1),
                                        ("eta", 1.1),
                                        ("eta", "abc")])
def test_set_params_eta_fail(key, value, re_update_params):
    """
    Testing Eta parameter update failure

    Parameters
    ----------
    key: str
        parameter keys
    value: float
        parameter values
    re_update_params: dict
        reset parameter values

    Returns
    -------

    Raises
    ------
    ValueError:
        parameter value is not integer or float
        value has to be greater than 0
        Eta value has to be less than equal to 1.
    """
    with pytest.raises(ValueError):
        Herbivore.update_params({key: value})


@pytest.mark.parametrize("parameters", [{"eta": 0.9, "w_birth": 30.0}])
def test_update_params(parameters, re_update_params):
    """
    Testing update parameters function

    Parameters
    ----------
    parameters: dict
            Parameters for update
    re_update_params: dict
            reset parameter values

    Returns
    -------
    Herbivore.params["eta"] == parameters["eta"] is True
    Herbivore.params["w_birth"] == parameters["w_birth"] is True
    """
    # params = parameters
    Herbivore.update_params(parameters)

    assert Herbivore.params["eta"] == parameters["eta"]
    assert Herbivore.params["w_birth"] == parameters["w_birth"]


@pytest.mark.parametrize("age, weight", [(1, 8.0),
                                         (5, 20.5),
                                         (20, 40),
                                         (40, 30)])
class TestHerbivore:
    """
    Herbivore Class Testing
    """

    @pytest.fixture(autouse=True)
    def create(self, age, weight):
        """
         Testing Herbivore creation

        Parameters
        ----------
        age: int
            Herbivore age
        weight: float
            Herbivore weight

        Notes
        -----

        - We create 4 Herbivores

        - With ages and weight set using parametrize

        ..code::

                @pytest.mark.parametrize("age, weight", [(1, 8.0),(5, 20.5),(30, 40),(35, 30)])


        - We store the age and weight of each carnivore
        - This will be used in other tests


        Returns
        -------

        """
        self.herb = Herbivore(age, weight)

        self.age = age
        self.weight = weight

    @pytest.fixture
    def reset_params(self):

        """
        Testing Herbivore class parameter update

        Returns
        -------

        """
        yield

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

    def test_create(self):

        """
        Testing age and weight values for created herbivore

        Notes
        ------
        - We assert that the created Carnivore has same age and weight expected

        Returns
        -------
        self.herb.age == self.age is True
        self.herb.weight == self.weight is True
        """
        assert self.herb.age == self.age
        assert self.herb.weight == self.weight

    @pytest.mark.parametrize("years", [1, 10, 23, 40])
    def test_aging(self, years):
        """
        Testing Herbivore aging

        Parameters
        ----------

        years: int
             Number of years for iteration

        Notes
        ------

        - We run aging for multiple values of years
        - We assert that the carnivore age is its current age + years

        ..code::

                self.age += 1

        Returns
        -------
        self.herb.age == self.age + years (True)
        """
        for _ in range(years):
            self.herb.aging()

        assert self.herb.age == self.age + years

    @pytest.mark.parametrize("years", [1, 7])
    @pytest.mark.parametrize("beta", [0.6, 1.2])
    @pytest.mark.parametrize("food", [0.0, 5.0, 10.0, 30.0])
    def test_increase_weight(self, food, beta, years, reset_params):
        """
        Testing Herbivore Increase weight function

        Parameters
        ----------
        food: float
                fodder eaten
        beta: float
                parameter value beta
        years: int
                Number of years for test
        reset_params: dict
                update parameter values

        Notes
        -----

        - We use parametrize to set multiple values for years, food
          and beta

        ..code::

                     @pytest.mark.parametrize("years", [1, 7])
                     @pytest.mark.parametrize("beta", [0.6, 1.2])
                     @pytest.mark.parametrize("food", [0.0, 5.0, 10.0, 30.0])

        - We check with the values to ensure the herbivore increases weight
          based on the values parsed in per time

        - The checks to ensure the right food value is parsed in the function
          comes in the feeding cycle


        Returns
        -------
        self.herb.weight == self.weight is True

        """
        self.herb.update_params({'beta': beta})

        for _ in range(years):
            self.herb.increase_weight(food)
            self.weight += beta * food

        assert self.herb.weight == self.weight

    @pytest.mark.parametrize("years", [1, 7])
    @pytest.mark.parametrize("eta", [0.9, 0.2])
    def test_decrease_weight(self, eta, years, reset_params):
        """
        Testing herbivore decrease weight function

        Parameters
        ----------
        eta: float
            parameter value eta
        years: int
                years for iteration
        reset_params: dict
                    reset parameter values

        Notes
        -----
        - We set the eta values and years using parametrize
        - parse in the new eta values using update_params function
        - we call the decrease weight function

        ..code::

              Herbivore.update_params({'eta': eta})

        - We calculate the expected weight

        ..code::

                self.weight -= eta * self.weight

        - We assert that the weight calculated and return from the function
          are the same

        Returns
        -------
        self.herb.weight == self.weight is True
        """
        Herbivore.update_params({'eta': eta})

        for _ in range(years):
            self.herb.decrease_weight()
            self.weight -= eta * self.weight

        assert self.herb.weight == self.weight

    @pytest.mark.parametrize("phi_age, a_half, phi_weight, w_half",
                             [(0.6, 40, 0.1, 10),
                              (0.3, 10, 0.2, 5)])
    def test_fitness(self, phi_age, a_half, phi_weight, w_half, reset_params):
        """
        Testing herbivore fitness

        Parameters
        ----------

        phi_age: float
                Parameter value

        a_half: float
                age half

        phi_weight: float
                phi weight parameter value

        w_half: float
                weight half

        reset_params: dict
                resetting parameters

        Notes
        ------

        - We set the parameter values for Phi_age, a_half, w_half, phi_weight
          using parametrize

        ..code::


                @pytest.mark.parametrize("phi_age, a_half, phi_weight, w_half",
                [(0.6, 40, 0.1, 10),
                (0.3, 10, 0.2, 5)])

        - update herbivore parameters with values

        ..code::

                        Carnivore.update_params({"phi_age": phi_age,
                                         "a_half": a_half,
                                         "phi_weight": phi_weight,
                                         "w_half": w_half})

        - Calculate fitness manually with values

        - Compare values and ensure they are the same.


        Returns
        -------
        0 <= self.herb.phi <= 1 is True

        self.herb.phi == c_phi is True
        """
        Herbivore.update_params({"phi_age": phi_age,
                                 "a_half": a_half,
                                 "phi_weight": phi_weight,
                                 "w_half": w_half})

        h_phi = (1 / (1 + math.exp(phi_age *
                                   (self.age - a_half)))) * \
                (1 / (1 + math.exp(-phi_weight *
                                   (self.weight - w_half))))

        for _ in range(5):
            self.herb.fitness()

        assert 0 <= self.herb.phi <= 1
        assert self.herb.phi == h_phi

    def test_death_alive(self, mocker, reset_params):
        r"""
        Testing Herbivore death status == alive

        Parameters
        ----------

        mocker: float
                control randomness

        reset_params: dict
                resetting parameters
        Notes
        ------
        - Set random to 0.8 using mocker

        - The random value is always greater than death probability

         .. math:: \omega * (1- \phi)

        - assert that all herbivores do not die

        ..code::

                if self.weight == 0:
                    return True
                elif random.random() < (self.params['omega'] * (1 - self.phi)):
                    return True
                else:
                    return False

        Returns
        -------

        self.herb.death() is False


        """
        mocker.patch('random.random', return_value=0.8)
        assert self.herb.death() is False

    def test_death_dead(self, mocker, reset_params):
        r"""
          Testing herbivore death status == dead

        Parameters
        ----------

        mocker: float
                control randomness

        reset_params: dict
                resetting parameters

        Notes
        ------
        - Set random to 0.001 using mocker

        - The random value is always less than death probability

        .. math:: \omega * (1- \phi)

        - assert that all herbivores  die

        ..code::

                if self.weight == 0:
                    return True
                elif random.random() < (self.params['omega'] * (1 - self.phi)):
                    return True
                else:
                    return False

        Returns
        -------
        self.herb.death() is True
        """
        # Random output is chosen as 0.01 because (20,30) is fit animal
        # condition with death probability as 0.04, hence had to choose
        #  much lower value.
        mocker.patch('random.random', return_value=0.01)
        assert self.herb.death()

    @pytest.mark.parametrize("food, food_max", [(5.0, 10.0),
                                                (10.0, 10.1),
                                                (0, 10.0)])
    def test_herbivore_feeding_low_food(self, food, food_max, reset_params):
        """
        Testing Herbivore feeding with low food values

        Parameters
        ----------
        food: float
                fodder available to herbivore
        food_max: float
                capacity of herbivore
        reset_params:dict
                reset parameter values

        Notes
        ------
        - Checks if the herbivore always eats the lower value, if its
        capacity is lower than the available fodder
        Returns
        -------
        self.herb.feeding(food) == food is True

        """
        Herbivore.update_params({'F': food_max})
        assert self.herb.feeding(food) == food

    @pytest.mark.parametrize("food, food_max", [(13.01, 13.0),
                                                (200.0, 10.0)])
    def test_herbivore_feeding_excess_food(self, food, food_max, reset_params):
        """
        Testing herbivore feeding with excess food values

        Parameters
        ----------
        food: float
                fodder available
        food_max: float
                capacity of herbivore
        reset_params: dict
                reset parameters

        Notes
        -----
        - Checks that the herbivore eats its capacity even if there is
        excess fodder available

        Returns
        -------
        self.herb.feeding(food) == food_max is True
        """
        Herbivore.update_params({'F': food_max})
        assert self.herb.feeding(food) == food_max

    def test_migration_prob(self, reset_params):
        """
        Testing herbivore migration probability


        Parameters
        ----------
        reset_params: dict
                update parameters

        Notes
        ------
        - We control the value of Mu to 2 and 0.01

        - This ensures all animals have probability less than random value
        with mu = 0.01 and greater with mu = 2

        ..code::

                probability = self.params["mu"] * self.phi
                if random.random() < probability:
                    return True
                else:
                    return False

        - We assert that when mu = 2 all animals migrate and when mu = 0.01
        all animals do not migrate

        Returns
        -------

        self.herb.migrate_prob() is False when mu = 0.01
         self.herb.migrate_prob() is True when mu = 2

        """
        Herbivore.update_params({"mu": 2})
        assert self.herb.migrate_prob()

        Herbivore.update_params({"mu": 0.01})
        assert self.herb.migrate_prob() is False

    def test_migration_prob_fail(self, mocker, reset_params):
        """
        Testing Migration probability failure with controlling random
        value

        Parameters
        ----------
        mocker: float
                Randomness control
        reset_params: dict
                update parameters

        Returns
        -------
        self.herb.migrate_prob == False

        Notes
        ------
        - This test sets the migration probability
          to ensure all animals choose not to migrate
        - We use Mocker to set the random value to 0.5

        ..code::

                probability = self.params["mu"] * self.phi
                if random.random() < probability:
                    return True
                else:
                    return False
        - We assert that the herbivores return False for migration


        """
        mocker.patch('random.random', return_value=0.5)
        assert self.herb.migrate_prob() is False

    def test_stat_migration(self, reset_params):

        num_trials = 100
        ALPHA = 0.01

        mu = self.herb.params['mu']
        migration_probability = mu * self.herb.phi

        num_migrants = sum(self.herb.migrate_prob()
                           for _ in range(num_trials))

        mean = num_trials * migration_probability
        var = num_trials * migration_probability * \
              (1 - migration_probability)
        z_score = (num_migrants - mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(z_score))
        assert phi > ALPHA

    def test_migration_prob_success(self, mocker, reset_params):
        """
        Testing Migration probability success

        Parameters
        ----------
        mocker: float
                control randomness
        reset_params: dict
                    update parameters

        Notes
        ------

        - This test sets the migration probability
          to ensure an animal chooses to migrate

        - We use Mocker to set the random value to 0.1

        ..code::

                probability = self.params["mu"] * self.phi
                if random.random() < probability:
                    return True
                else:
                    return False

        - We assert that the carnivores return True for migration

        Returns
        -------
        self.herb.migrate_prob == True

        """
        mocker.patch("random.random", return_value=0.1)
        assert self.herb.migrate_prob()

    def test_stat_death(self, reset_params):

        num_trials = 100
        ALPHA = 0.01

        omega = self.herb.params['omega']
        death_probability = omega * (1 - self.herb.phi)

        num_deaths = sum(self.herb.death() for _ in range(num_trials))  # True == 1, False == 0

        mean = num_trials * death_probability
        var = num_trials * death_probability * (1 - death_probability)
        z_score = (num_deaths - mean) / math.sqrt(var)
        phi = 2 * stats.norm.cdf(-abs(z_score))
        assert phi > ALPHA


######################################################
# Below test cases are special cases to identify birth
# by checking specific random for default params.
# General case would not satisfy all the criteria
# required.
######################################################
@pytest.mark.parametrize("age, weight", [(30, 33.0),
                                         (10, 36.0),
                                         (20, 1.0)])
def test_birth_no_child_herbivore(age, weight, mocker, re_update_params):
    """
    Testing herbivore does not give birth

    Parameters
    ----------
    age: int
        Animal age
    weight: float
            Animal weight

    mocker: float
            Randomness control

    re_update_params: dict
                update parameters

    Notes
    ------

    - We use pytest parameterize to set up a range of values for age and weight
      with age being parsed as an integer and weight as a float

    - Mocker controls the random.lognormvariate and sets the value at 30

    - for the animal with weight 1, this is less than the minimum weight 24
      the animal would be thrown out of the birth conditions

    ..code::

            if 0 < animal.weight >= animal.minimum_weight:


    - For the animal with weight 33 and 36, with the birth weight of the child at 30
      the weight loss of the mother would be above the conditions hence
      the animal is thrown out of the conditions

    ..code::

         weight_loss = self.params["xi"] * child_weight
         if (child_weight > 0) and (self.weight > weight_loss):




    Returns
    -------

    """
    # minimum_weight => 33 < 33.25 <- zeta * (w_birth + sigma_birth)
    # weight_loss => 35 < 36 <- xi * birth_weight
    # zero_weight => 0

    mocker.patch('random.lognormvariate', return_value=30.0)
    assert Herbivore(age, weight).birth() is None


@pytest.mark.parametrize("age, weight", [(10, 34.0),
                                         (30, 40.0)])
def test_birth_child_born(age, weight, mocker, re_update_params):
    """
    Testing herbivore meets child_birth conditions

    Parameters
    ----------
    age : int
        Carnivore age
    weight: float
            Carnivore weight
    mocker: float
            Random control
    re_update_params: dict
                Reset parameters

    Notes
    -----

    - Parametrize is used to set optimal values to ensure birth.
    - We use mocker to set the child weight value to always ensure
      the animal does not lose more than enough weight

    - For the first animal we set the weight at 34
      it is above the minimum animal weight at 24

    Returns
    -------

    """
    mocker.patch('random.lognormvariate', return_value=15.0)
    assert isinstance(Herbivore(age, weight).birth(), Herbivore)
