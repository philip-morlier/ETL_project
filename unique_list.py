import pandas as pd

class UniqueList():
    
    def __init__(self):
        self.df=None
        
    def make_df(self,csv):
        self.df=pd.read_csv(csv)
        
    def set_df(self,df):
        self.df=df

    def make_list_from_df(self,df,column):
        self.df=df
        return self.make_list(column)
        
    def make_list(self,column):
        if self.df is None:
            return ('you must call set_df or make_df')
        return list(self.df[column].unique())  

    def make_list_from_csv(self,csv,column):
        self.make_df(csv)
        return self.make_list(column)