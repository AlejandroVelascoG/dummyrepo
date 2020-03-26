# -*- coding: utf-8 -*-

# MODELO COVID

import statistics as st
import scipy.stats as stats
import xlrd as rd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import csv
import copy as cp

wb = rd.open_workbook('covid_stats.xlsx')
sh = wb.sheet_by_name('Hoja1')
nr = sh.nrows
nc = sh.ncols

cont_dia = sh.col_values(2, 1)
tot_cont = sh.col_values(2, 1)
imp_dia = sh.col_values(3, 1)
tot_imp = sh.col_values(4, 1)
rel_dia = sh.col_values(5, 1)
tot_rel = sh.col_values(6, 1)

def integ(x):
    for i in range(0, len(x)-1):
        try:
            x[i] = int(x[i])
        except:
            x.pop(i)
    if x[-1] == u'':
          x.pop(-1)
    else:
        x[-1] = int(x[-1])
    return(x)

def equal(x, y):
    while(len(y) < len(x)):
        x.pop(-1)
    while(len(x) < len(y)):
        y.pop(-1)
    return x, y

def rate(x):
    rate_list = []
    for i in range(1, len(x)):
        if x[i-1]!= 0:
            rt =  float(x[i])/float(x[i-1])
        else:
            rt = x[i]
        rate_list.append(rt)
    for j in range(0, len(rate_list)):
        rate_list[j] = float(rate_list[j])
    return rate_list

def new_val(x, min, max, lim):
    while len(x) < lim:
        rate = random.uniform(min, max)
        print(rate)
        val = rate*x[-1]
        x.append(val)
    return x

# NUMEROS MINSALU0D

cont_dia = integ(cont_dia)
# imp_dia = integ(imp_dia)
# rel_dia = integ(rel_dia)

# TASAS DE CONTAGIO, IMPORTADOS, RELACIONADOS (NUMERO AL DIA / NUMERO DEL DIA ANTERIOR)

rate_cont = rate(cont_dia)
# rate_imp = rate(imp_dia)
# rate_rel = rate(rel_dia)

# print(rate_cont)
# print(rate_imp)
# print(rate_rel)

# equal(cont_dia, rel_dia)
# equal(cont_dia, imp_dia)
# equal(rel_dia, imp_dia)

### PROMEDIOS TASAS DE CONTAGIO, IMPORTADOS, RELACIONADOS

prom_cont_dia = st.mean(rate_cont)
# prom_imp_dia = st.mean(rate_imp)
# prom_rel_dia = st.mean(rate_rel)

### DESVIACIONES ESTÁNDAR TASAS DE CONTAGIO, IMPORTADOS, RELACIONADOS

stdev_cont_dia = st.pstdev(rate_cont)
# stdev_imp_dia = st.pstdev(rate_imp)
# stdev_rel_dia = st.pstdev(rate_rel)

# MINIMOS PARA INTERVALOS: PROMEDIO MENOS UN CUARTO DE DESVIACION ESTANDAR

minC = prom_cont_dia - (stdev_cont_dia/4)
# minI = prom_imp_dia - (stdev_imp_dia/4)
# minR = prom_rel_dia

# MAXIMOS PARA INTERVALOS: PROMEDIO MAS UN CUARTO DE DESVIACION ESTANDAR

maxC = prom_cont_dia + (stdev_cont_dia/4)
# maxI = prom_imp_dia + (stdev_imp_dia/4)
# maxR = prom_rel_dia + (stdev_rel_dia/4)

### PLOTS DISTRIBUCIONES NORMALES TASAS DE CONTAGIO, IMPORTADOS, RELACIONADOS

# norm_cont = np.linspace(prom_cont_dia - 3*stdev_cont_dia, prom_cont_dia + 3*stdev_cont_dia, 100)
# norm_imp = np.linspace(prom_imp_dia - 3*stdev_imp_dia, prom_imp_dia + 3*stdev_imp_dia, 100)
# norm_rel = np.linspace(stdev_rel_dia - 3*stdev_rel_dia, prom_rel_dia + 3*stdev_rel_dia, 100)

# plt.plot(norm_cont, stats.norm.pdf(norm_cont, prom_cont_dia, stdev_cont_dia))
# plt.plot(norm_imp, stats.norm.pdf(norm_imp, prom_imp_dia, stdev_imp_dia))
# plt.plot(norm_rel, stats.norm.pdf(norm_rel, prom_rel_dia, stdev_rel_dia))

# plt.show()

# MODELO

#new_val(cont_dia, minC, maxC, 30)
#cont_dia = integ(cont_dia)
#print(cont_dia)

store = []
i=0

while(i<99):
    aux = cp.deepcopy(cont_dia)
    new_val(aux, minC, maxC, 30)
    store.append(aux)
    i+=1

print(len(store[0]))

sets = []
for i in range(0, 30):
    l = []
    for s in store:
        l.append(s[i])
    sets.append(l)

proms = []
for s in sets:
    prom = st.mean(s)
    proms.append(prom)

proms = integ(proms)
print(proms)


data = zip(proms)

with open('mes.csv', 'wb') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    for d in data:
        wr.writerow(d)
