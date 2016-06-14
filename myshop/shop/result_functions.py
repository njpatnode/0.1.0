import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import mpld3
import seaborn as sns
import numpy as np

### function class ####
class result_function(object):
    def init(self):
        return self
    def histogram(self, dataview_df, bins, variable):
        fig, ax = plt.subplots()
        x = np.array(dataview_df[variable])
        bins = int(bins)
        ax.hist(x, bins, normed = 1, alpha = 0.5)
        ax.set_xlabel(variable)
        ax.set_title(variable + ' Histogram')
        #ax.set_xlim(0, 1.01*max(x))
        fig_html = mpld3.fig_to_html(fig)
        return fig_html
    def scatterplot(self, dataview_df, x_variable, y_variable=None, dot_size=50):
        if y_variable is not None:
            fig, ax = plt.subplots()
            x = np.array(dataview_df[x_variable])
            y = np.array(dataview_df[y_variable])
            ax.scatter(x, y, s=int(dot_size))
            ax.set_xlabel(x_variable)
            ax.set_ylabel(y_variable)
            ax.set_title(x_variable + 'vs.' + y_variable + 'Scatterplot')
            ax.set_xlim(-0.025, 1.01*max(x))
            ax.set_ylim(-0.025, 1.01*max(y))
            ax.grid(True)
            fig_html = mpld3.fig_to_html(fig)
        else:
            fig_html = "Error: No y variable was provided."
        return fig_html
