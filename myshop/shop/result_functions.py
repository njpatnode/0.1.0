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