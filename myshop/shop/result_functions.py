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
            ax.scatter(x, y, s=dot_size)
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
    def lasso(self, dataview_df, x_variables, y_variable=None, test_split=0.2, alpha_value=1):
        if y_variable is not None:
            from sklearn.linear_model import Lasso
            import seaborn as sns
            fig, ax = plt.subplots()
            lrg = Lasso(alpha = alpha_value)
            l_train, l_test, j_train, j_test = train_test_split(x_variables, dataview.df[y_variable], test_size = test_split)
            lrg.fit(l_train,j_train)
            lrg_pred = lrg.predict(l_test)
            ax = sns.regplot(j_test, lrg_pred, ci = None)
            lassoscore = str(lrg.score(l_train, j_train))
            ax.set_xlabel('Predicted Test Data')
            ax.set_ylabel('Input Test Data')
            ax.set_xlim(-0.05,)
            ax.set_ylim(-0.05,)
            ax.set_title('Lasso Regression \n Lasso Score equals: ' + lassoscore)
            fig_html = mpld3.fig_to_html(fig)
        else:
            fig_html = "Error: No y variable was provided."
        return fig_html
    def ridge(self, dataview.df, x_variables, y_variable=None, test_split=0.2, alpha_value=1):
        if y_variable is not None:   
            from sklearn.linear_model import Ridge
            import seaborn as sns
            fig, ax = plt.subplots()
            rdg = Ridge(alpha = alpha_value)
            r_train, r_test, s_train, s_test = train_test_split(x_variables, dataview.df[y_variable], test_size = test_split)
            rdg.fit(r_train, s_train)
            rdgscore = str(rdg.score(r_train, s_train))
            rdg_pred = rdg.predict(r_test)
            ax = sns.regplot(s_test, rdg_pred, ci = None)
            ax.set_xlabel('Predicted Test Data')
            ax.set_ylabel('Input Test Data')
            ax.set_xlim(-0.05,)
            ax.set_ylim(-0.05,)
            ax.set_title('Ridge Regression \n Ridge Score equals: ' + rdgscore)
            fig_html = mpld3.fig_to_html(fig)
        else:
            fig_html = "Error: No y variable was provided."   
        return fig_html
    def lin_reg(self, dataview.df, x_variables, y_variable=None, test_split=0.2):
        if y_variable is not None:
            import scipy
            from scipy import stats
            import pandas as pd
            import matplotlib.pyplot as plt
            import numpy as np
            from sklearn.linear_model import LinearRegression
            from sklearn.cross_validation import train_test_split
            from sklearn.metrics import r2_score
            from sklearn import metrics
            fig, ax = plt.subplots()
            x_train, x_test, y_train, y_test = train_test_split(x_variables, dataview.df[y_variable], test_size=test_split)
            regr = LinearRegression()
            regr.fit(x_train,y_train)
            y_pred = regr.predict(x_test)
            ax = sns.regplot(y_test, y_pred, ci=None)
            ax.set_xlabel('Predicted Test Data')
            ax.set_ylabel('Input Test Data')
            ax.set_xlim(-0.05,)
            ax.set_ylim(-0.05,)
            rsquared = str(r2_score(y_test,y_pred))
            ax.set_title('Linear Regression \n R^2 score: ' + rsquared)
            fig_html = mpld3.fig_to_html(fig)
        else:
            fig_html = "Error: No y variable was provided."           
        return fig_html
