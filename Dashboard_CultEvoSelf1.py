# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 19:45:21 2022

STREAMLIT DASHBOARD for CultEvoSelf project

To run locally type this in Anaconda Prompt:
    streamlit run Dashboard_CultEvoSelf1.py



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

#%% SETUP

# Load data
df_ALL_noSeeds = pd.read_csv('All_CultEvoSelf_Exp1.csv')
df_ALL = pd.read_csv('All_CultEvoSelf_Exp1_S.csv')
df_Occurr = pd.read_csv('DATA_CultEvo_Occurences.csv')

# Create dictionaries with trait and valence labels
trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
trait_labels = {
    'Add1': 'Attractive','Add2': 'Political','Add3': 'Religious',
    'Neg1': 'Corrupt','Neg2': 'Dishonest','Neg3': 'Lazy','Neg4': 'Without empathy','Neg5': 'Impolite','Neg6': 'Cowardly',
    'Neu1': 'Trendy','Neu2': 'Busy','Neu3': 'Traditional','Neu4': 'Predictable','Neu5': 'Introverted','Neu6': 'Mystical',
    'Pos1': 'Friendly','Pos2': 'Intelligent','Pos3': 'Honorable','Pos4': 'Skilful','Pos5': 'Charismatic','Pos6': 'Creative'
    }
# Inverted trait_labels dictionary
inv_map = {v: k for k, v in trait_labels.items()}
# List of traits from th dictionary
traits_list  = list(trait_labels.values())

# Prepare the occurences data
occ_summary = df_Occurr.describe()    
occ_median = df_Occurr.median()


#%% DASHBOARD

### SIDEBAR

st.sidebar.markdown('# **CultEvoSelf study**')

button_radio = st.sidebar.radio("Choose what you want to see:", ["Introduction", "Task description", "Analysis of valences", "Analysis of individual traits"])

# button_1 = st.sidebar.button("Introduction")
# button_2 = st.sidebar.button("Task description")
# button_3 = st.sidebar.button("Analysis of valences")
# button_4 = st.sidebar.button("Analysis of traits")
selected_selectbox = "Attractive"
selected_selectbox = st.sidebar.selectbox('Which trait do you want to analyze?', traits_list)
# selected_selectbox = "Attractive"
# selected_selectbox = st.sidebar.selectbox('Which trait do you want to analyze?', traits_list)

# st.write(button_1)
# st.write(button_2)
# st.write(button_3)
# st.write(button_4)

#%% NO BUTTON PRESSED

# if (button_1 == False & button_2 == False & button_3 == False & button_4 == False):
#     st.title('Dashboard for the result of the CultEvoSelf study')
#     st.markdown('This is a dashboard allowing you to explore the results of the CultEvoSelf study .')


#%% BUTTON == 1 or none pressed

# if ((button_1 == True)): # | (button_1 == False & button_2 == False & button_3 == False & button_4 == False)):
if button_radio == 'Introduction':
    st.title('Introduction')
    st.markdown('This is a dashboard allowing you to explore the results of the **CultEvoSelf study**.')
    st.markdown('''In this study we investigated whether cultural transmission of information about a minimal ingroup
                and minimal outgroup differs. Specifically, we focused on transmission of information about 
                traits displayed by members of each group.
                ''')
    st.markdown('### What is social identity and why it matters')
    st.markdown(''' 
                Our social identity is what defines our place in society. It reflects the groups that we belong to:
                which country or nation we represent (national identity), which religion we belong to (religious identity),
                which gender we have (gender identity). It also involves smaller groups: our family, our circle of friends, 
                a village, town, or city we live in, and many others.
                ''')
    st.markdown(''' All of the groups that we belong to compose our **social identity**.  ''')
    st.markdown('### Minimal group paradigm')
    st.markdown(''' x ''')
    st.markdown('### What is a transmission chain')
    st.markdown(''' 
                Transmission chain is a method to investigate how information changes when it is repeatedly transmitted between 
                people. It is very similar to the children game "Chinese whispers", known also as "Deaf telephone" in some countries.
                In this game the first person (a seed) transmits an information to some other person. Then that second person transmits 
                this information to another person and so on... until it reaches the last person. A sequence of people through 
                which this information travelled is called a **chain**, and each person in this chain is known as a **generation**.
                ''')
    st.image(image='img/fig0_transmissionchain.png')
    st.markdown('### What we found')
    st.markdown(''' 
                This dashboard allows you to have a closer look at the results of our study. For a longer discussion of our 
                results you look at our scientific paper, which you can find under the following link: ____________. 
                However, an article does not allow to present full results in an interactive manner. Here you can do just that.
                ''')
    st.markdown('''
                In the section "Task description" you can familiarize yourself with the procedure of our experiment, and 
                in the "Analysis..." sections you can look at our results. 
                ''')
    st.markdown('''
                What did we find?
                We discovered that...
                ''')
    st.markdown('### References')
    st.markdown(''' 
                Boyd, R., Richerson, P.J. (1985). *Culture and the evolutionary process*. The University of Chicago Press.  
                Mesoudi, A. (2011). *Cultural evolution*. The University of Chicago Press.  
                Morin, O. (2016). *How traditions live and die*. Oxford University Press.  
                ''')

#%% BUTTON == 2

# if button_2 == True:
if button_radio == 'Task description':
    st.title("Task description")    
    st.markdown(''' 
                ### Experimental task  
                At the beginning of the experiment participants were presented with task instructions, 
                which are displayed in Figure 1A. The task instructions first told participants to memorize which of two villages 
                is “their” village, and which is a village of “strangers” (Green and Blue village – the assignment of colors was 
                counterbalanced across transmission chains). Afterwards, they read that each group has been previously rated on 
                a number of traits and that they will see how frequent each trait is in each group. Their task will be to memorize 
                these frequencies and then send them send them to the next participant, which can be either from the same or 
                different village as them. ''')
    st.image(image='img/fig1_task.png')
    st.markdown(''' 
                Afterwards, they proceeded to complete the task, which consisted of 21 trials, reflecting 21 traits that were used 
                in the study. Each trial started with a screen presenting the name of the trait, together with frequencies of its 
                occurrence of the trait (FOT) in both villages (Figure 1B). FOTs were always natural percentage numbers between 1 
                and 100. After participants read and memorized the frequencies they had to press a button confirming it. This led 
                to presentation of two subsequent screens in which participants had to indicate the frequency of that trait for 
                their and the strangers’ village (displayed in random order) on a continuous line on which only the ending points 
                were labeled. Clicking on a line left a mark, which participants could correct before confirming their response 
                by pressing a button below the line.
                ''')
    st.image(image='img/fig2_task.png')
    st.markdown('''
                ### The procedure of transmission chains  
                The experiment involved 18 transmission chains with 10 generations (10 instances 
                of information transmission) in each of them. Seed values for transmission chains were generated before the experiment 
                using the following rules: (1) the average frequency of occurrence of traits (FOT) within each valence (negative, 
                neutral, positive) had to be 50%, (2) the average standard deviation of FOT within each valence had to be 
                approximately 10, (3) the FOTs within each valence cannot repeat, what also ensured requirement (4) that the FOT for 
                any given trait could not be the same for ingroup and outgroup. Seed values created using these rules were then 
                assigned to traits. The assignment of traits was counterbalanced across participants to ensure that the same 
                combination of seed values is equally often used for ingroup and outgroup traits, and equally often used for 
                negative, neutral and positive traits. The same rules were also applied to seed values of the three additional 
                traits (religious, political, attractive). ''')
    st.markdown(''' 
                The first participant in each transmission chain had to transmit the assigned seed values. For each subsequent 
                participant in a transmission chain the responses from the previous participant were rounded to a natural number 
                and used as FOTs to be transmitted. 
                ''')  
    st.image(image='img/transmission_chains.png')
    
#%% BUTTON == 3

# if button_3 == True:
if button_radio == 'Analysis of valences':
    st.title("Analysis of valences")
    st.markdown('''Here you can see transmission chains for averages of traits representing three valences:
                positive, neutral, and negative. Green colour represents transmission chains for the minimal ingoup 
                (your village), and red lines represent the minimal outgroup (strangers' village). 
                Black dot on the right represents the median frequency in general population, as indicated 
                by our additional survey. Black dot on the left represents the seed value (50%).''')
    
    # Extract medians
    med_pos = occ_median['Positive']
    med_neu = occ_median['Neutral']
    med_neg = occ_median['Negative']
    
    ################ POSITIVE
    st.markdown('### Positive traits')
    st.markdown('Positive traits were: Friendly, Intelligent, Honorable, Skilful, Charismatic, Creative')    
    # Positive valence
    trait_valence = 'Pos'
    # Rearrange the data
    df_lmm2 = pd.melt(df_ALL, 
                      id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                      value_vars=['Avg_In_'+trait_valence, 'Avg_Out_'+trait_valence], 
                      var_name ='group', 
                      value_name ='Avg_'+trait_valence)
    # Set plot style
    sns.set(font_scale=1.5)
    sns.set_style('whitegrid')
    fig_dims = 11.7,8.27
    fig, ax1 = plt.subplots()#figsize=fig_dims)
    # Produce Lineplot + Stripplot
    ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait_valence, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] ) # also: col, row ; ,x_jitter=0, truncate - limit the data to min-max
    ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait_valence, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    ax1.get_legend().remove()
    trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
    ax1.set(title='Traits: '+trait_valence_labels[trait_valence], xlabel='Generation', ylabel='FOT: Frequency of occurrence of a trait [%]')    
    # Add median line
    plt.plot([0, 10], [50, med_pos], color='gray', marker='o', markersize=15, markerfacecolor='k', markeredgecolor='k')
    # Display in streamlit
    st.pyplot(fig)
    
    
    ################ NEUTRAL
    st.markdown('### Neutral traits')
    st.markdown('Neutral traits were: Trendy, Busy, Traditional, Predictable, Introverted, Mystical')    
    # Positive valence
    trait_valence = 'Neu'
    # Rearrange the data
    df_lmm2 = pd.melt(df_ALL, 
                      id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                      value_vars=['Avg_In_'+trait_valence, 'Avg_Out_'+trait_valence], 
                      var_name ='group', 
                      value_name ='Avg_'+trait_valence)
    # Set plot style
    sns.set(font_scale=1.5)
    sns.set_style('whitegrid')
    fig_dims = 11.7,8.27
    fig, ax1 = plt.subplots()#figsize=fig_dims)
    # Produce Lineplot + Stripplot
    ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait_valence, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] ) # also: col, row ; ,x_jitter=0, truncate - limit the data to min-max
    ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait_valence, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    ax1.get_legend().remove()
    trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
    ax1.set(title='Traits: '+trait_valence_labels[trait_valence], xlabel='Generation', ylabel='FOT: Frequency of occurrence of a trait [%]')    
    # Add median line
    plt.plot([0, 10], [50, med_neu], color='gray', marker='o', markersize=15, markerfacecolor='k', markeredgecolor='k')
    # Display in streamlit
    st.pyplot(fig)
    
    
    ################ POSITIVE
    st.markdown('### Negative traits')
    st.markdown('Negative traits were: Corrupt, Dishonest, Lazy, Without empathy, Impolite, Cowardly')    
    # Positive valence
    trait_valence = 'Neg'
    # Rearrange the data
    df_lmm2 = pd.melt(df_ALL, 
                      id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                      value_vars=['Avg_In_'+trait_valence, 'Avg_Out_'+trait_valence], 
                      var_name ='group', 
                      value_name ='Avg_'+trait_valence)
    # Set plot style
    sns.set(font_scale=1.5)
    sns.set_style('whitegrid')
    fig_dims = 11.7,8.27
    fig, ax1 = plt.subplots()#figsize=fig_dims)
    # Produce Lineplot + Stripplot
    ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait_valence, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] ) # also: col, row ; ,x_jitter=0, truncate - limit the data to min-max
    ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait_valence, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    ax1.get_legend().remove()
    trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
    ax1.set(title='Traits: '+trait_valence_labels[trait_valence], xlabel='Generation', ylabel='FOT: Frequency of occurrence of a trait [%]')    
    # Add median line
    plt.plot([0, 10], [50, med_neg], color='gray', marker='o', markersize=15, markerfacecolor='k', markeredgecolor='k')
    # Display in streamlit
    st.pyplot(fig)
    
    
#%% BUTTON == 4

# if button_4 == True:
if button_radio == 'Analysis of individual traits':
    
    st.title("Analysis of individual traits")

    # selected_selectbox = "Attractive"
    # selected_selectbox = st.selectbox('Which trait do you want to analyze?', traits_list)
    st.markdown('## TRAIT: '+selected_selectbox)
    st.markdown('Below you will see several plots illustrating the results for your chosen trait.')
    
    # Display the line plot
    
    st.markdown('### Line plots showing averages at each generation:')
    st.markdown('''This plot shows how the traits behaved across generations of a transmission chain. Generation 0 is the seed value that 
                was provided to the first participant in each chain and generation 10 is the last generation in our experiment. 
                The green line represents averages for participants' village (ingroup), and red line for the strangers' village (outgroup). 
                Each dot of the corresponding colour represents response from one person.''')
    st.markdown('''Black dot on the right represents the median frequency in general population, as indicated 
                by our additional survey. Black dot on the left represents the seed value (50%).''')
    
    trait = inv_map[selected_selectbox]
    
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
    
    # Add median line
    plt.plot([0, 10], [50, occ_median[trait_labels[trait]]], color='gray', marker='o', markersize=15, markerfacecolor='k', markeredgecolor='k')
    
    #from matplotlib import rcParams
    #fig = rcParams['figure.figsize'] = 11.7,8.27
    #ax1 = sns.set(rc={'figure.figsize':(5, 5)})
    
    st.pyplot(fig)
    
    ########% Display the vector plot
    
    st.markdown('### Vector plot showing transmission chains trajectories:')
    st.markdown('''This plot shows trajectories of transmission chains in a vactor space. Each colour represents one transmission chain. 
                Each vector represents one participant. The onset of each vector shows information that was provided to the participant, 
                and the end of each vector shows that participant's response. The value on the horizontal line (x-axis) represents 
                frequency of occurency in the ingroup, and the value on the vertical line (y-axis) represents it in the outgroup. ''')
    
    trait = inv_map[selected_selectbox]
    
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


