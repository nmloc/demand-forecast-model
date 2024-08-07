import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class JSONToDataFrame(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Convert JSON to DataFrame
        df = pd.DataFrame(X)
        return df