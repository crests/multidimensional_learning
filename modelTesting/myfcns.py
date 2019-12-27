"""
get_file_name(path)
    path(=dir)からfileのリストをgetする
    @path {string}
    return {string[]}

get_average_change(data, span=5, if_plot=False)
    data(Array)を、数回の四角窓でならす
    @data {Array}
    @span {Int}
    @if_plot {Boolean} プロットを作成するか。
 
plot4d(x,y,z,c,title="")
    xを3次元にscatter plotして、colorで示す
    @x,y,z {array}
    @c {array} colorに対応させる軸
    @title {String}
"""

def get_file_name(path):
    files = []
    for filename in os.listdir(path):
        files.append(os.path.join(path, filename))
    files = sorted(sorted(files))
    return [ret for ret in files if not ret.startswith(path + "/.")] # 隠しファイルを読み込まない、リスト表記

#平均的な変化を
def get_average_change(data, span=5, if_plot=False):
    ret = []
    for i in range(len(data) - span + 1):
        ret.append(np.mean(data[i:i+span]))
    if(if_plot):
        plt.figure()
        sns.lineplot(range(len(ret)), ret)
    return ret

def plot4d(x,y,z,c,title=""):
    fig = plt.figure()
    ax1 = fig.add_subplot(projection='3d')
    sc = ax1.scatter(x,y,z,zdir='z', c=c, cmap=plt.cm.binary) 
    plt.colorbar(sc)
    plt.title(title)
    return

##########################################
import sys
sys.path.append('..')

import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import rosen, differential_evolution, minimize, basinhopping
from mpl_toolkits.mplot3d import Axes3D

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
