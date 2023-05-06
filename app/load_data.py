from psa import Disease,Strategy
import pandas as pd


class data_loader():

    def __init__(self,file_disease,file_strategy,file_costs = None):

        self.disease_dict = {}
        self.strategy_dict = {}

        df_disease = pd.read_excel(file_disease)
        df_strategy = pd.read_excel(file_strategy)
        self.load_disease(df_disease)
        self.load_strategies(df_strategy)

        if file_costs:
            df_costs = pd.read_excel(file_costs)
            self.update_strategy_costs(df_costs)



    def load_disease(self,df):

        disease_dict = {}

        for i, j in df.iterrows():
            name = j['Disease']
            carrier_rate = j['Carrier rate']
            cost = j['Cost Disease']
            life_exp = j['Life Expectancy']
            inheritance = j['Inheritance']
            disease_dict[name] = Disease(name=name, carrier_rate=carrier_rate, inheritance=inheritance,
                                              life_expectancy=life_exp, cost=cost)
        self.disease_dict.update(disease_dict)


    def load_strategies(self,df):

        strategy_dict = {}

        strategy_list = set(df.columns).difference(['Disease','#disease'])

        for strategy in strategy_list:
            disease_list = df.loc[df[strategy] == 1, 'Disease'].values
            strategy_dict[strategy] = Strategy(strategy_name=strategy, disease_list=disease_list,
                                                    disease_dict=self.disease_dict)


        strategy_dict['No testing'] = Strategy(strategy_name='No testing', disease_list=[], testing_cost=0,
                                                    disease_dict=self.disease_dict)

        self.strategy_dict.update(strategy_dict)

    def update_strategy_costs(self,df):
        for i,j in df.iterrows():
            strategy = j['strategy']
            cost = j['cost']
            self.strategy_dict[strategy].testing_cost_couple = cost
            self.strategy_dict[strategy].update_cost()

