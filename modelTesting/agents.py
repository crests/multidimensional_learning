import sys
sys.path.append('..')


import model # model.py in the same dir

import pandas as pd
import numpy as np
from scipy import stats

import os
import sys
import time
import csv
import datetime
import math

import matplotlib.pyplot as plt
import seaborn as sns
from ptitprince import PtitPrince as pt


from IPython.html.widgets import interact, interactive, fixed
from IPython.html import widgets
'''
/anaconda3/lib/python3.6/site-packages/IPython/html.py:14: ShimWarning: 
The `IPython.html` package has been deprecated since IPython 4.0. 
You should import from `notebook` instead. 
`IPython.html.widgets` has moved to `ipywidgets`.
  "`IPython.html.widgets` has moved to `ipywidgets`.", ShimWarning)
'''

import random as rd
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

class AgentSample(model.Agent):
    agent_name = ""
    value_range = 1
    option_type = ""
    legend = ""
    
    def __init__(self, alpha = .1,  beta = .8, value_length=8, init_value = .7):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    #def update(self, option_chosen, reward) # reward is int(0 or 1)
    #def get_values(self, ops)
    #def get_value(self, op)
    #def get_choice_probs(self, ops)
    #def get_choice(self, ops)
    #def get_init_val(self)
    

    
##################################################################
#  AgentGreedyRandom
##################################################################
class AgentGreedyRandom(model.Agent):
    agent_name = "greedy_random"
    value_range = 1
    option_type = "array2*2*2"
    legend = ['000', '001', '010', '011', '100', '101', '110', '111']
    
    def __init__(self, alpha = .1,  beta = .8, value_length=8, init_value = .7):
        super().__init__(alpha=-1, beta=-1, value_length=0, init_value=-1)
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    def update(self, option_chosen, reward): # do noting
        return -1
    def get_values(self, ops):
        return -1
    #def get_value(self, op)
    def get_choice_probs(self, ops):
        idx = self.if_competitive(ops[0],ops[1],ops[2])
        prob = 100.0/sum(idx)
        return np.array(idx)*prob
    #def get_choice(self, ops):
    #def get_init_val(self)
        
    def compare(self, a,b):
        # both a, b should be np.array
        diff = a-b
        if ((diff >= [0,0,0]).all()):
            return "left_is_bigger"
        if ((diff <= [0,0,0]).all()):
            return "right_is_bigger"
        return "these_are_comparable"
    
    def if_competitive(self, a,b,c): 
        #順序列で最大の要素の項で1となる配列を返す。
        #左が最大ならば[1,0,0]。中央と右が同等で最大ならば[0,1,1]
        ret = [1,1,1]
        aa = np.array(a)
        bb = np.array(b)
        cc = np.array(c)
        ab = self.compare(aa,bb)
        bc = self.compare(bb,cc)
        ca = self.compare(cc,aa)
        if (ab=="right_is_bigger" or ca=="left_is_bigger"):
            ret[0] = 0
        if (bc=="right_is_bigger" or ab=="left_is_bigger"):
            ret[1] = 0
        if (ca=="right_is_bigger" or bc=="left_is_bigger"):
            ret[2] = 0
        return ret
    

##################################################################
#  AgentSimpleRL
##################################################################
class AgentSimpleRL(model.Agent):
    agent_name = "simpleRL"
    value_range = 1
    option_type = 'int'
    legend = ['000', '001', '010', '011', '100', '101', '110', '111']
    
    #def op2int(self, op)
    #def ops2int(self, ops)
    def __init__(self, alpha = .1,  beta = .8, value_length=8, init_value = .7):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        return
    def update(self, option_chosen, reward):  # reward is int(0 or 1)
        option_chosen = self.op2int(option_chosen)
        before = self.value_table[option_chosen]
        self.value_table[option_chosen] = before + self.alpha * ( reward*self.value_range - before)
        return self.value_table
    #def get_values(self, ops)
    #def get_value(self, op)
    #def get_choice_probs(self, ops)
    #def get_choice(self, ops)
    #def get_init_val(self)

    
##################################################################
#  AgentDimensionRL
##################################################################
class AgentDimensionRL(model.Agent):
    agent_name = "dimensionRL"
    value_range = 1
    option_type = 'array(3)'
    legend = ['a','b','c']
    value_length = 3
    
    def __init__(self, alpha = .1,  beta = .8, value_length=3, init_value = .7):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    def update(self, option_chosen, reward=1):
        before = self.value_table
        self.value_table = before + self.alpha*option_chosen*(reward*self.value_range - before)
        return self.value_table
    def get_values(self, ops):
        ret = []
        for op in ops:
            ret.append(self.get_value(np.array(op)))
        return ret
    def get_value(self, op):
        return sum(self.value_table*op)
    #def get_choice_probs(self, ops)
    #def get_choice(self, ops)
    #def get_init_val(self)
        
##################################################################
#  AgentRuleBasedSimpleRL 1   epsilonを使う
##################################################################
class AgentRuleBasedSimpleRL1(AgentSimpleRL):
    agent_name = "ruleBasedSimpleRL"
    value_range = 1
    option_type = 'array(8)'
    legend = ['a','b','c']
    value_length = 8
    
    option_type = 'int'
    legend = ['000', '001', '010', '011', '100', '101', '110', '111']
    
    #def op2int(self, op)
    #def ops2int(self, ops)
    def __init__(self, alpha = .1,  beta = .8, value_length=8, epsilon=.06, init_value = .7):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        self.epsilon=epsilon
        return
    #def update(self, option_chosen, reward):  # reward is int(0 or 1)
    #def get_values(self, ops)
    #def get_value(self, op)
    def get_choice_probs(self, ops):
        order = np.array(self.if_competitive(ops[0], ops[1], ops[2]))
        vals = np.array(self.get_values(ops))
        vals_inf = 1.0 - order
        vals_inf[vals_inf == 1.0] = -np.inf
        vals1 = vals*order + vals_inf
        prob1 = self.sigmoid(vals1) * (1 - self.epsilon)
        prob2 = (1 - order) * self.epsilon 
        return prob1 + prob2
    #def get_choice(self, ops)
    #def get_init_val(self)


##################################################################
#  AgentRuleBasedSimpleRL 0    劣るopのvalを0にする
##################################################################
class AgentRuleBasedSimpleRL0(AgentSimpleRL):
    agent_name = "ruleBasedSimpleRL"
    value_range = 1
    option_type = 'array(8)'
    legend = ['a','b','c']
    value_length = 8
    
    option_type = 'int'
    legend = ['000', '001', '010', '011', '100', '101', '110', '111']
    
    #def op2int(self, op)
    #def ops2int(self, ops)
    def __init__(self, alpha = .1,  beta = .8, value_length=8, init_value = .7, **kwargs):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        return
    #def update(self, option_chosen, reward):  # reward is int(0 or 1)
    #def get_values(self, ops)
    #def get_value(self, op)
    def get_choice_probs(self, ops):
        order = np.array(self.if_competitive(ops[0], ops[1], ops[2]))
        vals = np.array(self.get_values(ops))
        return self.sigmoid(vals * order) #これで、0になってる。
    #def get_choice(self, ops)
    #def get_init_val(self)

    
##################################################################
#  AgentRuleBasedDimensionRL 0    劣るopのvalを0にする
##################################################################
class AgentRuleBasedDimensionRL0(AgentDimensionRL):
    agent_name = "RuleBasedDimensionRL0"
    value_range = 1
    option_type = 'array(3)'
    legend = ['a','b','c']
    value_length = 3
    
    def __init__(self, alpha = .1,  beta = .8, value_length=3, init_value = .7):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    def get_choice_probs(self, ops):
        order = np.array(self.if_competitive(ops[0], ops[1], ops[2]))
        vals = np.array(self.get_values(ops))
        return self.sigmoid(vals * order) #これで、0になってる。
    #def get_choice(self, ops)
    #def get_init_val(self)
    
##################################################################
#  AgentDimensionRLwithDecay 選んでいない特徴のvalueを減らす。
##################################################################
class AgentDimensionRLwithDecay(AgentDimensionRL):
    agent_name = "DimensionRLwithDecay"
    value_range = 1
    option_type = 'array(3)'
    legend = ['a','b','c']
    value_length = 3
    
    def __init__(self, alpha = .1,  beta = .8, value_length=3, init_value = .7, decay=.1):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        self.decay = decay
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    def update(self, option_chosen, reward=1):
        option_unchosen = np.ones(3) - option_chosen
        before = self.value_table
        after_chosen = (before + self.alpha*(reward*self.value_range - before))*option_chosen
        after_unchosen = before*(1 - self.decay)*option_unchosen
        self.value_table = after_chosen + after_unchosen
        return self.value_table
        
    #def get_choice_probs(self, ops):
    #def get_choice(self, ops)
    #def get_init_val(self)

##################################################################
#  AgentDimensionRLwithInfoBonus 情報量を加味したモデル
##################################################################
class AgentDimensionRLwithInfoBonus(AgentDimensionRL):
    agent_name = "AgentDimensionRLwithInfoBonus"
    value_range = 1
    option_type = 'array(3)'
    legend = ['a','b','c']
    value_length = 3
    
    def __init__(self, alpha = .1,  beta = .8, value_length=3, init_value = .7, info_weight=.1):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value)
        self.info_weight = info_weight
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    #def update(self, option_chosen, reward=1):  
    #def get_values(self, ops)
    def get_value(self, op):
        info = self.info_weight*self.get_infomation_bonus(self.value_table)
        return sum((self.value_table+info)*op) 
    def get_infomation_bonus(self, x):
        x = x + (x==np.zeros(len(x)))*1e-5 - (x==np.ones(len(x)))*1e-5
        f = lambda x: -x*np.log2(x)
        return f(x)+f(1-x)
    #def get_choice_probs(self, ops):

    #def get_choice(self, ops)
    #def get_init_val(self)
    
##################################################################
#  AgentDimensionRLwithDecaywithInfoBonus 情報量を加味したモデル
##################################################################
class AgentDimensionRLwithInfoBonus(AgentDimensionRLwithDecay):
    agent_name = "AgentDimensionRLwithDecaywithInfoBonus"
    value_range = 1
    option_type = 'array(3)'
    legend = ['a','b','c']
    value_length = 3
    
    def __init__(self, alpha = .1,  beta = .8, value_length=3, init_value = .7, decay=.1, info_weight=.1):
        super().__init__(alpha=alpha, beta=beta, value_length=value_length, init_value=init_value,decay=decay)
        self.info_weight = info_weight
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    #def update(self, option_chosen, reward=1):  
    #def get_values(self, ops)
    def get_value(self, op):
        info = self.info_weight*self.get_infomation_bonus(self.value_table)
        return sum((self.value_table+info)*op) 
    def get_infomation_bonus(self, x):
        x = x + (x==np.zeros(len(x)))*1e-5 - (x==np.ones(len(x)))*1e-5
        f = lambda x: -x*np.log2(x)
        return f(x)+f(1-x)
    #def get_choice_probs(self, ops):

    #def get_choice(self, ops)
    #def get_init_val(self)
    
    
##################################################################
#  AgentDimensionRLwithDecaywithInfoBonusWithoutBeta 情報量を加味したモデル
##################################################################
class AgentDimensionRLwithDecaywithInfoBonusWithoutBeta(AgentDimensionRLwithInfoBonus):
    agent_name = "AgentDimensionRLwithDecaywithInfoBonus"
    value_range = 1
    option_type = 'array(3)'
    legend = ['a','b','c']
    value_length = 3
    
    def __init__(self, alpha = .1, init_value = .7, decay=.1, info_weight=.1, beta = .6, value_length=3):
        super().__init__(alpha=alpha, beta=.6, value_length=value_length, init_value=init_value,decay=decay)
        self.info_weight = info_weight
        return
    #def op2int(self, op)
    #def ops2int(self, ops)
    #def update(self, option_chosen, reward=1):  
    #def get_values(self, ops)
    def get_value(self, op):
        info = self.info_weight*self.get_infomation_bonus(self.value_table)
        return sum((self.value_table+info)*op) 
    def get_infomation_bonus(self, x):
        x = x + (x==np.zeros(len(x)))*1e-5 - (x==np.ones(len(x)))*1e-5
        f = lambda x: -x*np.log2(x)
        return f(x)+f(1-x)
    #def get_choice_probs(self, ops):

    #def get_choice(self, ops)
    #def get_init_val(self)

    
    