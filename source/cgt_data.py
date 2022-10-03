from psa import Disease, Strategy

# Disease Definitions
d1 = Disease(name='disease1',carrier_rate=0.01,life_expectancy=80,cost=10000)
d2 = Disease(name='disease2',carrier_rate=0.02,life_expectancy=60,cost=20000)
d3 = Disease(name='disease3',carrier_rate=0.005,life_expectancy=40,cost=100000)
disease_dict = {'disease1':d1,'disease2':d2,'disease3':d3}


# Strategies Definition
s0 = Strategy('no testing',disease_list=[],testing_cost=0,disease_dict=disease_dict)
s1 = Strategy('limited screening',disease_list=['disease2'],testing_cost=1000,disease_dict=disease_dict)
s2 = Strategy('full screening',disease_list=['disease1','disease2','disease3'],testing_cost=1200,disease_dict=disease_dict)

strategy_dict = {'no testing': s0, 'limited testing': s1, 'full testing': s2}