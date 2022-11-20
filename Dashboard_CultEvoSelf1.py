# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 19:45:21 2022

STREAMLIT DASHBOARD for CultEvoSelf project

@author: mgwoz
"""

#%% import packages
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # only import this one function from matplotlib
import statsmodels as sm         # 
import seaborn as sns            # 
import scipy as sp               #  
import pingouin as pg
import os                        # operating system
import glob

#%% Load data

df_ALL_noSeeds = pd.read_csv('All_CultEvoSelf_Exp1.csv')
df_ALL = pd.read_csv('All_CultEvoSelf_Exp1_S.csv')


#%% 1C. Create dictionaries with trait and valence labels

trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}

trait_labels = {
    'Add1': 'Attractive','Add2': 'Political','Add3': 'Religious',
    'Neg1': 'Corrupt','Neg2': 'Dishonest','Neg3': 'Lazy','Neg4': 'Without empathy','Neg5': 'Impolite','Neg6': 'Cowardly',
    'Neu1': 'Trendy','Neu2': 'Busy','Neu3': 'Traditional','Neu4': 'Predictable','Neu5': 'Introverted','Neu6': 'Mystical',
    'Pos1': 'Friendly','Pos2': 'Intelligent','Pos3': 'Honorable','Pos4': 'Skilful','Pos5': 'Charismatic','Pos6': 'Creative'
    }

inv_map = {v: k for k, v in trait_labels.items()}
traits_list  = list(trait_labels.values())

#%% Build the dashboard

st.title('Investigate individual traits in the CultEvoSelf study')

st.markdown('Select a trait from the list on the left that you want to investigate.')

selected_sidebar = "Attractive"
selected_sidebar = st.sidebar.selectbox('Which trait do you want to analyze?', traits_list)

st.markdown('## TRAIT: '+selected_sidebar)

st.markdown('Below you will see several plots. Each plot will be separately described.')

#%% Display the line plot

st.markdown('### Line plots showing averages at each generation:')

trait = inv_map[selected_sidebar]

# Rearrange the data
df_lmm2 = pd.melt(df_ALL, 
                  id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                  value_vars=[trait+'_In_response', trait+'_Out_response'], 
                  var_name ='group', 
                  value_name ='Avg_'+trait)

# Set plot style
sns.set(font_scale=1.5)
sns.set_style('whitegrid')

fig_dims = 11.7,8.27

fig, ax1 = plt.subplots()#figsize=fig_dims)

# Lineplot + scatter (stripplot)
ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] ) # also: col, row ; ,x_jitter=0, truncate - limit the data to min-max
ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait, data=df_lmm2, hue='group', palette = ['g', 'r'] )
ax1.get_legend().remove()
ax1.set(title='Trait: '+trait_labels[trait], xlabel='Generation', ylabel='FOT [%]')

#from matplotlib import rcParams
#fig = rcParams['figure.figsize'] = 11.7,8.27
#ax1 = sns.set(rc={'figure.figsize':(5, 5)})

st.pyplot(fig)


#%% Display the vector plot

st.markdown('### Vector plot showing transmission chains trajectories:')

trait = inv_map[selected_sidebar]

# Prepare the vector data
x = df_ALL[trait+'_In_correct_response']
y = df_ALL[trait+'_Out_correct_response']
u = df_ALL[trait+'_In_response'].round() - df_ALL[trait+'_In_correct_response']
v = df_ALL[trait+'_Out_response'].round() - df_ALL[trait+'_Out_correct_response']

c = df_ALL['id_exp_chain']

#arrow_widths = np.sqrt( (u)**2+(v)**2 )/40
arrow_widths = 0.003

fig, ax = plt.subplots()

plt.rcParams['figure.figsize'] = [10, 10]
#fig = plt.figure()
plt.xlim([0, 100])
plt.ylim([0, 100])
# draw vertical line from (70,100) to (70, 250)
plt.plot([0, 100], [0, 100], 'k-')
ax = plt.quiver(x,y,u,v,c, cmap='tab20', width=arrow_widths, scale=100) #, linewidths=arrow_widths)
# Axes labels
# Which trait
plt.xlabel('Occurrence in the ingroup [%]', fontsize=20) # , fontsize=24)
plt.ylabel('Occurrence in the outgroup [%]', fontsize=20)
plt.title(trait+': '+trait_labels[trait], fontsize=20)
# Set tick font size
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

st.pyplot(fig)


