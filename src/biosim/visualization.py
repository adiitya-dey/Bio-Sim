import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import subprocess
import os

_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'biosim_project'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


class Visualization:

    def __init__(self, geogr=None, y_max=None, c_max=None, img_years=None,
                 img_dir=None, img_base=None, img_fmt=None, vis_years=None,
                 hist_specs=None, img_name=None):
        self.map = geogr

        if vis_years is None:
            self.vis_years = 0
        else:
            self.vis_years = vis_years

        if y_max is None:
            self.y_max = 20000
        else:
            self.y_max = y_max

        if c_max is None:
            self.c_max = {'Herbivore': 200, 'Carnivore': 100}
        else:
            self.c_max = c_max

        if img_years is None:
            self.img_years = vis_years
        else:
            self.img_years = img_years

        if hist_specs is None:
            self.hist_specs = {'weight': {'max': 80, 'delta': 2},
                               'fitness': {'max': 1.0, 'delta': 0.05},
                               'age': {'max': 60, 'delta': 2}}
        else:
            self.hist_specs = {'weight': {'max': 80, 'delta': 2},
                               'fitness': {'max': 1.0, 'delta': 0.05},
                               'age': {'max': 60, 'delta': 2}}
            for key, outer_val in hist_specs.items():
                if key not in self.hist_specs.keys():
                    raise ValueError(f"{key} does not exists"
                                     f" in hist_specs.")

                for inner_key, inner_val in outer_val.items():
                    if inner_key not in self.hist_specs[key].keys():
                        raise ValueError(f"{inner_key} does not exists"
                                         f" in hist_specs[{key}].")
                    self.hist_specs[key][inner_key] = inner_val

        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt

        # if img_name is None:
        #     img_name = _DEFAULT_GRAPHICS_NAME
        #
        # # Create image directory if it does not exists
        #
        # if img_dir is not None:
        #     self._img_base = os.path.join(img_dir, img_name)
        # else:
        #     self._img_base = None

        self.year = 0

        self.herb_line = None
        self.carn_line = None

        self.img_ctr = 0
        # self.img_step = 1

        # Create Base layout of the Visualization.
        self.fig = plt.figure(constrained_layout=True, figsize=(6, 8))
        self.fig.suptitle("Bio Simulation", fontsize=12, fontweight="bold")
        self.fig.tight_layout(h_pad=2, w_pad=2)

        # Create base layout of Map Plot.
        self.map_plot = self.fig.add_axes([0.04, 0.67, 0.3, 0.3])
        self.map_plot.set_title("Island", fontsize=8)
        self.draw_map()

        # Create base layout of Animal Count.
        self.animal_count_plot = self.fig.add_axes([0.67, 0.65, 0.31, 0.3])
        self.animal_count_plot.set_title('Animal Count', fontsize=8)
        self.animal_count_plot.set_ylim(0, self.y_max)
        self.animal_count_plot.tick_params(axis='y', labelsize=6)

        # Create base layout for Age histogram.
        self.age_histogram = self.fig.add_axes([0.06, 0.04, 0.25, 0.15])
        self.age_histogram.set_title("Age", fontsize=8)
        self.age_histogram.set_ylim([0, self.hist_specs["age"]["max"]])
        self.age_histogram.tick_params(axis='both', labelsize=6)
        self.age_histogram.set_yticks(range(0,
                                            4800 + 1,
                                            600))
        self.age_histogram.set_yticklabels(range(0,
                                                 4800 + 1,
                                                 600))
        self.bin_edges_age = np.arange(0,
                                       (self.hist_specs["age"]["max"] +
                                        (self.hist_specs["age"]["delta"] / 2)),
                                       self.hist_specs["age"]["delta"])
        self.hist_counts_age = np.zeros_like(self.bin_edges_age[:-1], dtype=float)

        self.age_hist_herbivore = self.age_histogram.stairs(self.hist_counts_age,
                                                            self.bin_edges_age,
                                                            color='b',
                                                            lw=1,
                                                            label='Herbivore')
        self.age_hist_carnivore = self.age_histogram.stairs(self.hist_counts_age,
                                                            self.bin_edges_age,
                                                            color='r',
                                                            lw=1,
                                                            label='Carnivore')

        # Create base layout for Weight histogram.
        self.weight_histogram = self.fig.add_axes([0.39, 0.04, 0.25, 0.15])
        self.weight_histogram.set_title("Weight", fontsize=8)
        self.weight_histogram.tick_params(axis='both', labelsize=6)
        self.weight_histogram.set_ylim([0, self.hist_specs["weight"]["max"]])

        self.weight_histogram.set_yticks(range(0,
                                               4800 + 1,
                                               600))
        self.weight_histogram.set_yticklabels(range(0,
                                                    4800 + 1,
                                                    600))
        self.bin_edges_weight = np.arange(0,
                                          (self.hist_specs["weight"]["max"] +
                                           (self.hist_specs["weight"]["delta"] / 2)),
                                          self.hist_specs["weight"]["delta"])
        self.hist_counts_weight = np.zeros_like(self.bin_edges_weight[:-1], dtype=float)

        self.weight_hist_herbivore = self.weight_histogram.stairs(self.hist_counts_weight,
                                                                  self.bin_edges_weight,
                                                                  color='b',
                                                                  lw=1,
                                                                  label='Herbivore')
        self.weight_hist_carnivore = self.weight_histogram.stairs(self.hist_counts_weight,
                                                                  self.bin_edges_weight,
                                                                  color='r',
                                                                  lw=1,
                                                                  label='Carnivore')

        # Create base layout for Fitness histogram.
        self.fitness_histogram = self.fig.add_axes([0.73, 0.04, 0.25, 0.15])
        self.fitness_histogram.set_title("Fitness", fontsize=8)
        self.fitness_histogram.set_ylim([0, self.hist_specs["fitness"]["max"]])
        self.fitness_histogram.tick_params(axis='both', labelsize=6)
        self.fitness_histogram.set_yticks(range(0,
                                                4800 + 1,
                                                600))
        self.fitness_histogram.set_yticklabels(range(0,
                                                     4800 + 1,
                                                     600))
        self.bin_edges_fitness = np.arange(0,
                                           (self.hist_specs["fitness"]["max"] +
                                            (self.hist_specs["fitness"]["delta"] / 2)),
                                           self.hist_specs["fitness"]["delta"])
        self.hist_counts_fitness = np.zeros_like(self.bin_edges_fitness[:-1], dtype=float)

        self.fitness_hist_herbivore = self.fitness_histogram.stairs(self.hist_counts_fitness,
                                                                    self.bin_edges_fitness,
                                                                    color='b',
                                                                    lw=1,
                                                                    label='Herbivore')
        self.fitness_hist_carnivore = self.fitness_histogram.stairs(self.hist_counts_fitness,
                                                                    self.bin_edges_fitness,
                                                                    color='r',
                                                                    lw=1,
                                                                    label='Carnivore')

        # Identify map shape for heatmaps.
        map_shape = np.zeros(shape=(
            len(self.map.splitlines()),
            len(list(self.map.splitlines()[0]))))

        # Create base layout for Herbivore HeatMap
        self.herbivore_heatmap = self.fig.add_axes([0.15, 0.25, 0.3, 0.3])
        self.herbivore_heatmap.set_title("Herbivore Distribution", fontsize=8)
        # self.herbivore_heatmap.grid()
        self.herbivore_heatmap.set_xticks(range(1, 1 + map_shape.shape[1], 3))
        self.herbivore_heatmap.set_xticklabels(range(1, 1 + map_shape.shape[1], 3),
                                               fontsize=6)
        self.herbivore_heatmap.set_yticks(range(1, 1 + map_shape.shape[0], 3))
        self.herbivore_heatmap.set_yticklabels(range(1, 1 + map_shape.shape[0], 3),
                                               fontsize=6)
        self.herb_dist = self.herbivore_heatmap.imshow(map_shape,
                                                       cmap='magma',
                                                       interpolation='nearest',
                                                       vmin=0,
                                                       vmax=self.c_max["Herbivore"])

        self.fig.colorbar(self.herb_dist,
                          cax=self.fig.add_axes([0.01, 0.30, 0.01, 0.2]),
                          shrink=0.3,
                          )

        # Create base layout for Carnivore HeatMap
        self.carnivore_heatmap = self.fig.add_axes([0.54, 0.25, 0.3, 0.3])
        self.carnivore_heatmap.set_title("Carnivore Distribution", fontsize=8)
        # self.carnivore_heatmap.grid()
        self.carnivore_heatmap.set_xticks(range(1, 1 + map_shape.shape[1], 3))
        self.carnivore_heatmap.set_xticklabels(range(1, 1 + map_shape.shape[1], 3),
                                               fontsize=6)
        self.carnivore_heatmap.set_yticks(range(1, 1 + map_shape.shape[0], 3))
        self.carnivore_heatmap.set_yticklabels(range(1, 1 + map_shape.shape[0], 3),
                                               fontsize=6)
        self.carn_dist = self.carnivore_heatmap.imshow(map_shape,
                                                       cmap='magma',
                                                       interpolation='nearest',
                                                       vmin=0,
                                                       vmax=self.c_max["Carnivore"])
        self.fig.colorbar(self.carn_dist,
                          cax=self.fig.add_axes([0.91, 0.30, 0.01, 0.2]),
                          shrink=0.4)

        # Create base layout for Year Counting.
        self.time_counter = self.fig.add_axes([0.45, 0.7, 0.1, 0.1])
        self.time_counter.axis('off')  # turn off coordinate system

        self.template = 'Year : {:5d}'
        self.txt = self.time_counter.text(0.5, 0.5, self.template.format(0),
                                          horizontalalignment='center',
                                          verticalalignment='center',
                                          transform=self.time_counter.transAxes,
                                          fontsize=10)

    def show_plot(self):
        plt.pause(0.01)

    def final_plot(self):
        plt.show()

    def draw_heatmap(self, c_matrix=None, h_matrix=None):

        self.herb_dist = self.herbivore_heatmap.imshow(h_matrix,
                                                       cmap='magma',
                                                       interpolation='nearest',
                                                       vmin=0,
                                                       vmax=self.c_max["Herbivore"])

        self.carn_dist = self.carnivore_heatmap.imshow(c_matrix,
                                                       cmap='magma',
                                                       interpolation='nearest',
                                                       vmin=0,
                                                       vmax=self.c_max["Carnivore"])

    def draw_year_counter(self, year):

        self.txt.set_text(self.template.format(year))

    def draw_histogram(self, histogram_values):

        # Update age histogram values.
        hist_age_val_herbivore, _ = np.histogram(histogram_values["Herbivore"]["age"],
                                                 self.bin_edges_age)
        hist_age_val_carnivore, _ = np.histogram(histogram_values["Carnivore"]["age"],
                                                 self.bin_edges_age)
        self.age_hist_herbivore.set_data(hist_age_val_herbivore)
        self.age_hist_carnivore.set_data(hist_age_val_carnivore)

        # Update weight histogram values.
        hist_weight_val_herbivore, _ = np.histogram(histogram_values["Herbivore"]["age"],
                                                    self.bin_edges_weight)
        hist_weight_val_carnivore, _ = np.histogram(histogram_values["Carnivore"]["age"],
                                                    self.bin_edges_weight)
        self.weight_hist_herbivore.set_data(hist_weight_val_herbivore)
        self.weight_hist_carnivore.set_data(hist_weight_val_carnivore)
        # plt.pause(1)

        # Update fitness histogram values.
        hist_fitness_val_herbivore, _ = np.histogram(histogram_values["Herbivore"]["fitness"],
                                                     self.bin_edges_fitness)
        hist_fitness_val_carnivore, _ = np.histogram(histogram_values["Carnivore"]["fitness"],
                                                     self.bin_edges_fitness)
        self.fitness_hist_herbivore.set_data(hist_fitness_val_herbivore)
        self.fitness_hist_carnivore.set_data(hist_fitness_val_carnivore)
        # plt.pause(0.01)

    def draw_map(self):
        rgb_value = {'W': (0.0, 0.0, 1.0),
                     'L': (0.0, 0.6, 0.0),
                     'H': (0.5, 1.0, 0.5),
                     'D': (1.0, 1.0, 0.5)}
        map_rgb = [[rgb_value[column] for column in row] for row in self.map.splitlines()]
        self.map_plot.imshow(map_rgb)
        self.map_plot.set_xticks(range(1, 1 + len(map_rgb[0]), 4))
        self.map_plot.set_xticklabels(range(1, 1 + len(map_rgb[0]), 4), fontsize=6)
        self.map_plot.set_yticks(range(1, 1 + len(map_rgb), 4))
        self.map_plot.set_yticklabels(range(1, 1 + len(map_rgb), 4), fontsize=6)
        # self.map_plot.grid()

        water_patch = mpatches.Patch(color=(0.0, 0.0, 1.0), label="Water")
        desert_patch = mpatches.Patch(color=(1.0, 1.0, 0.5), label="Desert")
        highland_patch = mpatches.Patch(color=(0.5, 1.0, 0.5), label="Highland")
        lowland_patch = mpatches.Patch(color=(0.0, 0.6, 0.0), label="Lowland")
        self.map_plot.legend(bbox_to_anchor=(0.5, -0.1),
                             loc="upper center",
                             mode="expand",
                             ncol=2,
                             handles=[lowland_patch,
                                      highland_patch,
                                      desert_patch,
                                      water_patch],
                             fontsize=8)

    def get_plot_values(self, years):
        self.year += years

        # Prepare Animal Count Plotting Values.
        self.animal_count_plot.set_xlim([0, self.year])
        if self.herb_line is None:
            xdata = np.arange(0, self.year + 1, 1)
            x_data_size = len(xdata)
            self.herb_line = self.animal_count_plot.plot(xdata,
                                                         np.full_like(xdata,
                                                                      np.nan,
                                                                      dtype=float),
                                                         linestyle='-',
                                                         color='b',
                                                         label='Herbivore',
                                                         lw=1.5)[0]
            self.carn_line = self.animal_count_plot.plot(xdata, np.full_like(xdata,
                                                                             np.nan,
                                                                             dtype=float),
                                                         linestyle='-',
                                                         color='r',
                                                         label='Carnivore',
                                                         lw=1.5)[0]
        else:
            x_data_h, y_data_h = self.herb_line.get_data()
            x_data_c, y_data_c = self.carn_line.get_data()
            xdata = np.arange(x_data_h[-1] + 1, self.year + 1, 1)
            if len(xdata) > 0:
                ydata = np.full_like(xdata, np.nan, dtype=float)
                self.herb_line.set_data(np.hstack((x_data_h, xdata)), np.hstack((y_data_h, ydata)))
                self.carn_line.set_data(np.hstack((x_data_c, xdata)), np.hstack((y_data_c, ydata)))
                x_data_size = len(xdata) + len(x_data_h)

        if x_data_size <= 11:
            self.animal_count_plot.set_xticks(range(0,
                                                    x_data_size,
                                                    1))
            self.animal_count_plot.set_xticklabels(range(0,
                                                         x_data_size, 1),
                                                   fontsize=6)
            # self.animal_count_plot.grid(axis="both")
        elif 11 < x_data_size <= 51:
            self.animal_count_plot.set_xticks(range(0,
                                                    x_data_size,
                                                    3))
            self.animal_count_plot.set_xticklabels(range(0,
                                                         x_data_size,
                                                         3),
                                                   fontsize=6)
            # self.animal_count_plot.grid(axis="both")
        elif 51 < x_data_size <= 101:
            self.animal_count_plot.set_xticks(range(0,
                                                    x_data_size,
                                                    10))
            self.animal_count_plot.set_xticklabels(range(0,
                                                         x_data_size,
                                                         10),
                                                   fontsize=6)
            # self.animal_count_plot.grid(axis="both")
        elif 101 < x_data_size <= 501:
            self.animal_count_plot.set_xticks(range(0,
                                                    x_data_size,
                                                    20))
            self.animal_count_plot.set_xticklabels(range(0,
                                                         x_data_size,
                                                         20),
                                                   fontsize=6, rotation="vertical")
            # self.animal_count_plot.grid(axis="both")
        elif x_data_size > 501:
            self.animal_count_plot.set_xticks(range(0,
                                                    x_data_size,
                                                    100))
            self.animal_count_plot.set_xticklabels(range(0,
                                                         x_data_size,
                                                         100),
                                                   fontsize=6, rotation="vertical")
            # self.animal_count_plot.grid(axis="both")

    def draw_animal_count(self, animal_count, current_year):

        idx = int(current_year)  # integer division to get correct array location
        herb_ydata = self.herb_line.get_ydata()
        herb_ydata[idx] = animal_count["Herbivore"]
        self.herb_line.set_ydata(herb_ydata)

        idx = int(current_year)  # integer division to get correct array location
        carn_ydata = self.carn_line.get_ydata()
        carn_ydata[idx] = animal_count["Carnivore"]
        self.carn_line.set_ydata(carn_ydata)
        self.animal_count_plot.legend(fontsize=8)

    def save_fig(self, current_year):

        if current_year % self.img_years == 0:
            if self.img_base is not None and self.img_dir is not None:
                # os.chdir(self.img_dir)
                plt.savefig('{dir}/{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                                   num=self.img_ctr,
                                                                   type=self.img_fmt,
                                                                   dir=self.img_dir))
                self.img_ctr += 1

    def make_movie(self, movie_fmt=None):
        if self.img_base is None and self.img_dir is None:
            raise RuntimeError("No img_base and img_dir defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                img_path = '{dir}/{base}'.format(base=self.img_base,
                                                 dir=self.img_dir)

                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(img_path),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(img_path, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                img_path = '{dir}/{base}'.format(base=self.img_base,
                                                 dir=self.img_dir)
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(img_path),
                                       '{}.{}'.format(img_path, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)
