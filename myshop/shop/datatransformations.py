import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.decomposition import PCA

class data_transformations(object):
    def init(self):
        return self
    def to_numeric(self, dataview_df, variable):
        output = pd.to_numeric(dataview_df[[variable]])
        return output
    def indicator_conv(self, dataview_df, variable):
        output = 2 - dataview_df[[variable]].values
        return output
    def categorical_conv(self, dataview_df, variable):
        y = pd.to_numeric(dataview_df[[variable]])
        enc = OneHotEncoder(dtype=np.int64, sparse = False)
        feature = y.values.reshape(-1,1)
        enc.fit(feature)
        binary_features = enc.transform(feature)
        output = pd.DataFrame(binary_features)
        return output
    def to_datetime(self, dataview_df, variable):
        output = pd.to_datetime(dataview_df[[variable]])
        return output
    def age_convert(self, dataview_df, birth_date, start_year, start_month, start_day):
        convert = lambda x: relativedelta(datetime.date(int(start_year), int(start_month), int(start_day)), datetime.date(int(x[0:4]), int(x[4:6]), int(x[6:8]))).years
        output = dataview_df[[birth_date]].map(convert)
        return output
    def top_indicator(self, dataview_df, variable, risk_threshold):
        y = pd.DataFrame(dataview_df[[variable]])
        y.columns = ['target']
        lvl = y.quantile(risk_threshold)
        f = lambda x: 1 if x > lvl[0] else 0
        output = y['target'].map(f)
        return output
    def extract_rows(self, dataview_df, variable, risk_threshold):
        y = pd.DataFrame(dataview_df[[variable]])
        y.columns = ['target']
        lvl = y.quantile(risk_threshold)
        f = lambda x: 1 if x > lvl[0] else 0
        y['indicator'] = y['target'].map(f)
        y = y.drop('target',1)
        output = y[y.indicator != 0]
        return output
    def normalize(self, dataview_df, variable):
        obs_num = len(dataview_df[[variable]])
        output = normalize(dataview.df[[variable]],norm='max').reshape(obs_num,1)
        return output
    def accumulator(self, dataview_df, variables, group_by):
        dataview = pd.DataFrame(dataview_df[[variables]])
        original = dataview.groupby([group_by]).sum()
        data = originial.reset_index()
        data2 = data.set_index([group_by])
        cumusum = data2.groupby(level=[0,1]).sum().groupby(level=[0]).cumsum()
        output = cumusum - original
        return output
    def pca_transform(self, dataview_df, variable, components):
        x = dataview_df[[variable]]
        pca = PCA(n_components = int(components))
        output = pca.fit_transform(x)
        return output
    def sortvalues(self, dataview_df, variables):
        z = pd.DataFrame(dataview_df[[variable]])
        output = z.sort_values(variables, 0)
        return output
        
        
