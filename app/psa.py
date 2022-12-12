import pandas as pd
import random
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter
import copy



class Disease():
    """Disease class.

    The class provides genetic and clinical information about a disease and functionality
    to estimate the inheritance risk of a disease based on the carrier rate and the
    inheritance mechanisms (i.e: recessive,dominant,x-linked)

    Attributes:
        name: name of the disease
        carrier_rate: A float quantifying the in the carrier rate in the population.
        inheritance: A string specifying the genetic mechanism ('recessive' or 'X-linked recessive')
        cost: Healthcare cost related to disease management
        life_expectancy: life expectancy for individuals affected by disease (Years)
        p_risk: probability for the offspring to be affected by disease
    """

    def __init__(self, name, carrier_rate, life_expectancy, cost, inheritance='recessive'):
        self.name = name
        self.carrier_rate = carrier_rate
        self.life_expectancy = life_expectancy
        self.cost = cost
        self.inheritance = inheritance
        self.compute_risk()


    def compute_risk(self):
        """
        method to estimate the risk of being affected
        """

        if self.inheritance == 'recessive':
            self.p_risk = np.power(self.carrier_rate,2)
        elif self.inheritance == 'X-linked recessive':
            self.p_risk = self.carrier_rate
        else:
            raise NotImplementedError

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Disease: {}'.format(self.name)

class Strategy():
    """Strategy class.

    This class specify the screening strategy, providing information about the screened disease and the screening cost

    Attributes:
        strategy_name: name of the strategy
        testing_cost: cost of the screening
        disease_list: list of diseases screened by strategy
        disease_dict: dictionary specifying the disease space
    """

    def __init__(self, strategy_name='', disease_list=[], testing_cost=0, disease_dict = {}):
        self.strategy_name = strategy_name
        self.testing_cost = testing_cost
        self.disease_list = disease_list
        self.disease_dict = disease_dict

    def __repr__(self):
        return 'Strategy: {}'.format(self.strategy_name)

    def disease_probabilies(self, disease_name, eps_cs, rho_notint, eps_pgt):
        """Estimate the probability of intervention and the probability of affected offspring"""
        disease = self.disease_dict[disease_name]
        p_risk = disease.p_risk
        if disease_name in self.disease_list:
            p_intervention = p_risk * (1 - eps_cs) * (1 - rho_notint)
            p_affected = 0.25 * p_risk * (eps_cs + (1 - eps_cs) * (rho_notint + (1 - rho_notint) * eps_pgt))
        else:
            p_intervention = 0
            p_affected = 0.25 * p_risk

        return p_intervention, p_affected

    def assess_strategy(self, disease_space=None, life_expectancy_healthy=83, intervention_cost=3000,
                        eps_cs=0.02, rho_notint=0.23, eps_pgt=0.02):
        """quantitative assessment of the strategy in terms of probability of being affected by any disease in the
        disease space, life expectancy and total cost of the strategy        """

        if disease_space is None:
            disease_space = self.disease_list

        p_risk = {}
        p_intervention = {}
        p_affected = {}
        p_affected_total = 0
        for disease_name in disease_space:
            disease = self.disease_dict[disease_name]
            p_risk[disease_name] = disease.p_risk
            (p_intervention[disease_name], p_affected[disease_name]) = self.disease_probabilies(disease_name, eps_cs,
                                                                                                rho_notint, eps_pgt)
            # rare disease approx
            p_affected_total += p_affected[disease_name]
        p_healthy = 1 - p_affected_total

        # life exp
        life_exp = life_expectancy_healthy * p_healthy
        for disease_name in disease_space:
            disease = self.disease_dict[disease_name]
            life_exp_disease = disease.life_expectancy
            life_exp += p_affected[disease_name] * life_exp_disease

        # cost
        total_cost = self.testing_cost
        for disease_name in disease_space:
            disease = self.disease_dict[disease_name]
            cost_disease = disease.cost
            total_cost += p_affected[disease_name] * cost_disease + intervention_cost * p_intervention[disease_name]

        return {'p_affected_total': p_affected_total, 'life_exp': life_exp, 'total_cost': total_cost}


class Icer():
    """
    Class for deterministic comparison of two screening strategies and ICER (Incremental Cost-Effectiveness Ratio)
    estimation
    """

    def __init__(self, strategy1, strategy2, disease_space=None, life_expectancy_healthy=83, intervention_cost=3000,
                 eps_cs=0.02, rho_notint=0.23, eps_pgt=0.02, testing_cost1=None, testing_cost2=None):



        self.strategy1 = copy.deepcopy(strategy1)
        self.strategy2 = copy.deepcopy(strategy2)
        self.life_expectancy_healthy = life_expectancy_healthy
        self.intervention_cost = intervention_cost
        self.eps_cs = eps_cs
        self.rho_notint = rho_notint
        self.eps_pgt = eps_pgt

        if disease_space is None:
            self.disease_space = list(set(self.strategy1.disease_list).union(self.strategy2.disease_list))
        else:
            self.disease_space = disease_space

        if testing_cost1 is None:
            self.testing_cost1 = self.strategy1.testing_cost
        else:
            self.testing_cost1 = testing_cost1

        if testing_cost2 is None:
            self.testing_cost2 = self.strategy2.testing_cost
        else:
            self.testing_cost2 = testing_cost2

    def compute_icer(self):

        self.strategy1.testing_cost = self.testing_cost1
        self.strategy2.testing_cost = self.testing_cost2


        out1 = self.strategy1.assess_strategy(self.disease_space,
                                              self.life_expectancy_healthy, self.intervention_cost,
                                              self.eps_cs, self.rho_notint, self.eps_pgt)
        out2 = self.strategy2.assess_strategy(self.disease_space,
                                              self.life_expectancy_healthy, self.intervention_cost,
                                              self.eps_cs, self.rho_notint, self.eps_pgt)

        delta_years = out1['life_exp'] - out2['life_exp']
        delta_costs = out1['total_cost'] - out2['total_cost']
        try:
            icer = delta_costs / delta_years
        except:
            icer = None

        self.icer = icer
        self.delta_years = delta_years
        self.delta_costs = delta_costs
        self.life_exp1 = out1['life_exp']
        self.life_exp2 = out2['life_exp']
        self.total_cost1 = out1['total_cost']
        self.total_cost2 = out2['total_cost']


    def univariate_sensitivity(self, feature, feature_lb, feature_ub, nstep=10):

        univariate_curve = {}

        for value in np.linspace(feature_lb, feature_ub, nstep):
            setattr(self, feature, value)
            self.compute_icer()
            univariate_curve[value] = self.icer
        self.df_sensitivity = pd.DataFrame.from_dict(univariate_curve, orient='index').reset_index().rename(
            columns={'index': feature, 0: 'icer'})

    def plot_sensitivity(self):
        self.df_sensitivity.plot(x=self.df_sensitivity.columns[0], y='icer')
        plt.grid()


class Psa():
    """
    Class to perform Probabilistic Sensitivity Analysis
    """

    def __init__(self, strategy1, strategy2):

        self.strategy1 = strategy1
        self.strategy2 = strategy2
        #self.disease_dict = strategy1.disease_dict

    def run_mc(self,
               intervention_cost_lb, intervention_cost_ub,
               testing_cost1_lb, testing_cost1_ub,
               testing_cost2_lb, testing_cost2_ub,
               eps_cs_lb, eps_cs_ub,
               eps_pgt_lb, eps_pgt_ub,
               rho_notint_lb, rho_notint_ub,
               nsim=1000, disease_space = None
               ):

        if disease_space is None:
            disease_space = list(
                set(self.strategy1.disease_list).union(self.strategy2.disease_list))  # ['disease1', 'disease2', 'disease3']

        self.nsim = nsim

        strategy1 = self.strategy1
        strategy2 = self.strategy2

        mc_samples = []
        intervention_cost = {}
        testing_cost1 = {}
        testing_cost2 = {}
        rho_notint = {}
        eps_cs = {}
        eps_pgt = {}

        life_expectancy_healthy = 83

        for i in range(nsim):
            intervention_cost[i] = random.uniform(intervention_cost_lb, intervention_cost_ub)
            testing_cost1[i] = random.uniform(testing_cost1_lb, testing_cost1_ub)
            testing_cost2[i] = random.uniform(testing_cost2_lb, testing_cost2_ub)
            rho_notint[i] = random.uniform(rho_notint_lb, rho_notint_ub)
            eps_cs[i] = random.uniform(eps_cs_lb, eps_cs_ub)
            eps_pgt[i] = random.uniform(eps_pgt_lb, eps_pgt_ub)

            strategy1.testing_cost = testing_cost1[i]
            strategy2.testing_cost = testing_cost2[i]
            out_mc = Icer(strategy1, strategy2,
                          disease_space,
                          life_expectancy_healthy=life_expectancy_healthy,
                          intervention_cost=intervention_cost[i],
                          eps_cs=eps_cs[i],
                          rho_notint=rho_notint[i],
                          eps_pgt=eps_pgt[i])
            out_mc.compute_icer()
            mc_samples.append(out_mc.icer)

        intervention_cost_avg = np.mean(list(intervention_cost.values()))
        testing_cost1_avg = np.mean(list(testing_cost1.values()))
        testing_cost2_avg = np.mean(list(testing_cost2.values()))
        rho_notint_avg = np.mean(list(rho_notint.values()))
        eps_cs_avg = np.mean(list(eps_cs.values()))
        eps_pgt_avg = np.mean(list(eps_pgt.values()))

        strategy1.testing_cost = testing_cost1_avg
        strategy2.testing_cost = testing_cost2_avg
        out_avg = Icer(strategy1, strategy2,
                       disease_space,
                       life_expectancy_healthy=life_expectancy_healthy,
                       intervention_cost=intervention_cost_avg,
                       eps_cs=eps_cs_avg,
                       rho_notint=rho_notint_avg,
                       eps_pgt=eps_pgt_avg)
        out_avg.compute_icer()

        self.icer_mc_samples = mc_samples
        self.icer_deterministic = out_avg.icer
        self.total_cost1_deterministic = out_avg.total_cost1
        self.total_cost2_deterministic = out_avg.total_cost2
        self.life_exp1_deterministic = out_avg.life_exp1
        self.life_exp2_deterministic = out_avg.life_exp2


    def plot_ceac_hist(self, bins=None, labels='', range=None,outfile=None):

        if bins is None:
            bins = np.int(np.log2(self.nsim) * 5)
        fig = plt.figure(figsize=(10, 7))
        ax = plt.axes()
        ax_bis = ax.twinx()

        color1 = 'blue'
        color2 = 'orange'
        color3 = 'red'

        values, base, _ = ax_bis.hist(self.icer_mc_samples, bins=bins, alpha=0.5, color=color2, range=range,
                                      label="MonteCarlo samples", density=True)
        values = np.append(values, 0)
        ax.plot(base, np.cumsum(values) / np.cumsum(values)[-1], color=color1, marker='o', linestyle='-', markersize=1,
                label="Cost-effectivness probability")
        # plt.xlabel(labels)
        # plt.ylabel("Proportion")
        plt.title('CEAC diagram: {} vs {}'.format(self.strategy1.strategy_name, self.strategy2.strategy_name))
        # ax_bis.legend();
        # ax.legend();
        ax.grid()
        plt.axvline(self.icer_deterministic, c=color3, ls='--', label='deterministic ICER')

        plt.ticklabel_format(axis='x', style='', scilimits=[-10, 10])

        ax.set_xlabel('Willingness to pay (Euros/Year)')
        ax.set_ylabel('Probability', color=color1)
        ax.set_ylim([0,1])
        ax_bis.set_ylabel('ICER prob density function', color=color2)
        plt.legend()
        ax.legend()


        if outfile is None:
            plt.show()
        else:
            plt.savefig(outfile)

        return

    def plot_ceac(self):
        sns.ecdfplot(data=self.icer_mc_samples, label='mc samples')
        plt.grid()
        plt.title('CEAC diagram: {} vs {}'.format(self.strategy1.strategy_name, self.strategy2.strategy_name))
        plt.xlabel('ICER threshold (Euros/Year)')
        plt.ylabel('Cost-effectivness probability')
        plt.ticklabel_format(axis='both', style='', scilimits=[-10, 10])
        plt.axvline(self.icer_deterministic, c='r', ls='--', label='deterministic')
        plt.legend()



