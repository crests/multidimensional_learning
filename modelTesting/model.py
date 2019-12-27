import sys
sys.path.append('..')


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




class Memory:
    
    def __init__(self, filename, agent_name, n_trial = 300, n_pattern = 3):
        self.options = []
        self.choice_probs = []
        self.option_chosen = []
        self.if_correct = []
        self.value_table = []
        self.n_trial = n_trial
        self.n_pattern = n_pattern
        self.filename = filename
        self.agent_name = agent_name
        self.value_table_flatten = []
        self.weight_table = []
        return
    
    def get_value_table(self):
        return self.value_table
    
    def i_trial(self):
        return len(options)
    
    def record(self, varname, value):
        exec('self.'+ varname + '.append(' + str(value)+')')
        return
    
    def save_options(self, value):
        self.options.append(value)
        return
    def save_option_chosen(self, value):
        self.option_chosen.append(value)
        return
    def save_if_correct(self, value):
        self.if_correct.append(value)
        return
    def save_value_table(self, value):
        #print(value)
        value = np.array(value).copy()
        self.value_table.append(value)
        self.value_table_flatten.append(value.flatten())
        #print(self.value_table[len(self.value_table)-1])
        return
    def save_choice_probs(self, value):
        self.choice_probs.append(value)
        return
    def save_weight_table(self, value):
        self.weight_table.append(value)
        return
    
    def save_data(self, init_val = []):  
        idx2 = ['options', 'selected_options', 'filename', 'agent_name', 'today']
        today = datetime.datetime.today()
        with open('data_table.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([today, self.n_trial, self.n_pattern, self.filename, self.agent_name, init_val])
        pd.DataFrame([options, selected_options, if_correct, value_table], index =idx2).transpose().to_csv('log/log_' + filename)
        return
        
    def clear_init_data(self):
        idx = ['time_stamp', 'n_trial', 'n_pattern', 'filename', 'agent_name', 'init_val']
        with open('data_table.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(idx)
            
class Game:
    
    def n_options(self): #used for making int options
        return 2**self.n_pattern
    def __init__(self, filename, n_trial = 300, n_pattern = 3, n_option = 3, competitive_rate = .85):
        self.i_trial = 1 #今、何トライアル目なのか。
        self.filename = filename
        self.rate_table = pd.read_csv(filename, header=None).transpose()
        
        self.n_trial = n_trial
        self.n_pattern = n_pattern
        self.n_option = n_option
        self.competitive_rate = competitive_rate
        return
    
    def compare(self, a,b):
        # both a, b should be np.array
        diff = a-b
        if ((diff >= [0,0,0]).all()):
            return "left_is_bigger"
        if ((diff <= [0,0,0]).all()):
            return "right_is_bigger"
        return "these_are_comparable"
    def if_competitive(self, a,b,c):
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
    
    def get_options(self):
        table = self.get_options1()
        if(self.competitive_rate == -1):
            return table
        r = rd.random()
        if(r <= self.competitive_rate): # if true, it means it should be competitive
            while (sum(self.if_competitive(table[0],table[1],table[2])) == 1): #if not competitive, thus needed to re-generate
                # self.if_competitive(args[])は、選ばれる可能性のあるものを1とする配列を返す
                # 右が選ばれる場合には [1,0,0]が返る。そのため、sum()を取ると1になる。
                # このwhile内では、sum()==1、つまり、competitiveの場合に再度optionを生成する
                table = self.get_options1()
        else: # false condition, it means it should be non-competitive
            while (sum(self.if_competitive(table[0],table[1],table[2])) != 1): # if competitive, thus needed to re-generate
                table = self.get_options1()
        return table
    
    def get_options1(self):
        left = self.get_options0()
        middle = self.get_options0()
        right = self.get_options0()
        while((np.array(left) == middle).all()):
            middle = self.get_options0()
        while((np.array(left) == right).all() and (np.array(middle) == right).all()):
            right = self.get_options0()
        return [left, middle, right]
    def get_options0(self): #配列[0,0,1]などを返す
        ret = []
        for i in range(self.n_pattern):
            ret.append(rd.randint(0,1))
        return ret
    
    def get_options_int(self):
        arr = self.get_option_int3()
        return [self.arr2int(arr[0]), self.arr2int(arr[1]), self.arr2int(arr[2])]
    
    def arr2int(self, arr):
        return arr[0]*4+arr[1]*2+arr[2]
    
    def read_csv(self, filename):  # (i, trials, walkSize)
        # filename = 'rate/rateTable_size'+ str(walkSize) + '_' + str(trials) + 'trials_' + str(i).zfill(3) + '.csv'
        a = pd.read_csv(filename, header=None)
        a = a.transpose()
        a.columns =  ['a','b','c']
        self.rate_table = a
        return
    
    #何トライアル目で、何を選んだかで、当たり・ハズレを返す。
    def correct_or_not(self, option_chosen, if_int = False):
        if if_int:
            option_chosen = self.int2option(option_chosen)
        i = self.i_trial
        r = rd.random() * 100.0
        arr = self.rate_table[i-1 : i]
        rate = arr.dot(option_chosen)
        rate = rate[self.i_trial - 1] #選択肢から算出される当たり確率 
        self.i_trial += 1 #このトライアルの終了を意味する。
        return (r < rate)
    def compare(self, a,b):
        # both a, b should be np.array
        diff = a-b
        if ((diff >= [0,0,0]).all()):
            return "left_is_bigger"
        if ((diff <= [0,0,0]).all()):
            return "right_is_bigger"
        return "these_are_comparable"
    def if_competitive(self, a,b,c):
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
    
class GameFromLog():
    choice2idx = {"left":0, "middle":1, "right":2}
    
    def __init__(self, filename):
        self.filename = filename
        self.read_logfile()
        self.i_trial = 1 #今、何トライアル目なのか。
        self.rate_table = pd.read_csv(filename, header=None).transpose()
        
        #self.n_trial = n_trial
        #self.n_pattern = n_pattern
        #self.n_option = n_option
        #self.competitive_rate = competitive_rate
        return
   
    def str2option(self, str_table):
        ret = []
        for i in range(len(str_table)):
            ret.append(np.array(str_table[i].split(",")).astype(int))
        return ret
    def str2bool(self,str_arr):
        ret = []
        for i in range(len(str_arr)):
            if(str_arr[i] == "TRUE" or str_arr[i] == "true"):
                ret.append(True)
            else:
                ret.append(False)
        return ret
    def get_best_exp_option(self, prob_ls, prob_ms, prob_rs):
        ret = []
        for i in range(len(prob_ls)):
            ret.append(self.get_best_exp_option0(prob_ls[i], prob_ms[i], prob_rs[i]))
        return ret
    def get_best_exp_option0(self, prob_l, prob_m, prob_r):
        if(prob_l >= prob_m and prob_l>=prob_r):
            return "left"
        if(prob_m >= prob_l and prob_m>=prob_r):
            return "middle"
        if(prob_r >= prob_l and prob_r>=prob_m):
            return "right"
        
    def my_read_csv(self):
        a = pd.read_csv(self.filename, header=None)
        a = a.transpose()
        a.columns =  ['option_left','option_middle','option_right',
                      'prob_left','prob_middle','prob_right',
                      'choice','hit_or_blow','sum_score', 'rt']
        return a
    def read_logfile(self):
        a = self.my_read_csv()
        a['option_left_str'] = a.option_left
        a['option_middle_str']  = a.option_middle
        a['option_right_str']  = a.option_right
        a.option_left = self.str2option(a.option_left)
        a.option_middle = self.str2option(a.option_middle)
        a.option_right = self.str2option(a.option_right)
        a.prob_left = a.prob_left.astype(float)/100.0
        a.prob_middle = a.prob_middle.astype(float)/100.0
        a.prob_right = a.prob_right.astype(float)/100.0
        a['best_option'] = self.get_best_exp_option(a.prob_left, a.prob_middle, a.prob_right)
        a.hit_or_blow = self.str2bool(a.hit_or_blow)
        a.sum_score = a.sum_score.astype(int)
        a.rt = a.rt.astype(float)
        self.log = a
        return a
    def get_options(self):
        a = self.log
        return [a.option_left[self.i_trial-1], a.option_middle[self.i_trial-1], a.option_right[self.i_trial-1]]
    def get_prob(self, op = "all"):
        a = self.log
        if op == "left":
            return a.prob_left[self.i_trial-1]
        if op == "middle":
            return a.prob_middle[self.i_trial-1]
        if op == "right":
            return a.prob_right[self.i_trial-1]
        if op == "all":
            return [a.prob_left[self.i_trial-1], a.prob_middle[self.i_trial-1], a.prob_right[self.i_trial-1]]
        return "blank"
    def get_choice(self):
        return self.log.choice[self.i_trial-1]
    def get_option_chosen(self):
        choice = self.log.choice[self.i_trial-1]
        return self.log["option_" + choice][self.i_trial-1]
    def get_hit_or_blow(self):
        return self.log.hit_or_blow[self.i_trial-1]
    def to_next_trial(self):
        self.i_trial = 1 + self.i_trial
        return self.i_trial
    def get_i_trial(self):
        return self.i_trial
    def compare(self, a,b):
        # both a, b should be np.array
        diff = a-b
        if ((diff >= [0,0,0]).all()):
            return "left_is_bigger"
        if ((diff <= [0,0,0]).all()):
            return "right_is_bigger"
        return "these_are_comparable"
    def if_competitive(self, a,b,c):
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


    
class Agent:
    choice2idx = {"left":0, "middle":1, "right":2}
    agent_name = "parent"
    def __init__(self, alpha = .1,  beta = .8, value_length=8, init_value = .7):
        # params
        self.alpha = alpha
        self.beta = beta
        self.value_table = np.ones(value_length)*init_value
        self.init_value_table = self.value_table
        return
    def op2int(self, op): # to explain this fcn, trans op to idx_of_value_table
        return op[0]*4+op[1]*2+op[2]
    def ops2int(self, ops):
        return [self.op2int(ops[0]), self.op2int(ops[1]), self.op2int(ops[2])]
    def update(self, option_chosen, reward): # td learning
        before = self.value_table[option_chosen]
        self.value_table[option_chosen] = before + self.alpha * ( reward*self.value_range - before)
        return self.value_table
    
    def get_values(self, ops): # get values of options now shown
        ops = self.ops2int(ops)
        ret = []
        for op in ops:
            ret.append(self.get_value(op))
        return np.array(ret)
    def get_value(self, op):
        return self.value_table[op]
    
    def get_choice_probs(self, ops): # get select_rate from values of options now shown
        vals= np.array(self.get_values(ops)) # in the fcn, ops2int
        return self.sigmoid(vals)
    
    def get_choice(self, ops): # get random float. using select_rate, get_choice
        r = rd.random()*100.0
        probs = self.get_choice_probs(ops)
        for prob, option in zip(probs, ops):
            if(r < prob):
                return option
            r -= prob
        return options[-1]
                
    def get_init_val(self):
        return list('alpha', self.alpha, 'beta', self.beta, 'value_table', str(self.init_value_table))
    
    def compare(self, a,b):
        # both a, b should be np.array
        diff = a-b
        if ((diff >= [0,0,0]).all()):
            return "left_is_bigger"
        if ((diff <= [0,0,0]).all()):
            return "right_is_bigger"
        return "these_are_comparable"
    def if_competitive(self, a,b,c):
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
    def sigmoid(self, vals):
        #print("\r{}: {}".format(vals, self.beta * vals), end="")
        a = np.array(self.beta * vals).astype(np.float128)
        ex = np.exp(a)
        below = sum(ex)/100.0
        return ex/below
