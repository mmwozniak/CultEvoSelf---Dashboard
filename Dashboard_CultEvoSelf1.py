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
import statsmodels.formula.api as smf
import pickle

#%% SETUP

# Load data
df_ALL_noSeeds = pd.read_csv('All_CultEvoSelf_Exp1_noSeeds.csv')
df_ALL = pd.read_csv('All_CultEvoSelf_Exp1_withSeeds.csv')
df_Occurr = pd.read_csv('DATA_CultEvo_Occurences.csv')
df_Valence = pd.read_csv('DATA_CultEvo_Valences.csv')
df_allTraits = pd.read_csv("DATA_CultEvo_Chains_TraitsLong.csv")

# Create dictionaries with trait and valence labels
trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
trait_labels = {
    'Add1': 'Attractive','Add2': 'Political','Add3': 'Religious',
    'Neg1': 'Corrupt','Neg2': 'Dishonest','Neg3': 'Lazy','Neg4': 'Without empathy','Neg5': 'Impolite','Neg6': 'Cowardly',
    'Neu1': 'Trendy','Neu2': 'Busy','Neu3': 'Traditional','Neu4': 'Predictable','Neu5': 'Introverted','Neu6': 'Mystical',
    'Pos1': 'Friendly','Pos2': 'Intelligent','Pos3': 'Honorable','Pos4': 'Skillful','Pos5': 'Charismatic','Pos6': 'Creative'
    }
# Inverted trait_labels dictionary
inv_map = {v: k for k, v in trait_labels.items()}
# List of traits from the dictionary
traits_list  = list(trait_labels.values())
traits_codes = list(trait_labels.keys())


# Prepare the valences data
df_Valence = df_Valence.loc[:,traits_list]
df_Valence['Negative'] = df_Valence.loc[:,['Corrupt','Dishonest','Lazy','Without empathy','Impolite','Cowardly']].mean(axis=1)
df_Valence['Neutral'] = df_Valence.loc[:,['Trendy','Busy','Traditional','Predictable','Introverted','Mystical']].mean(axis=1)
df_Valence['Positive'] = df_Valence.loc[:,['Friendly','Intelligent','Honorable','Skillful','Charismatic','Creative']].mean(axis=1)
val_summary = df_Valence.describe()    
val_median = df_Valence.median()

# Prepare the occurences data
occ_summary = df_Occurr.describe()    
occ_median = df_Occurr.median()


#%% DASHBOARD

### SIDEBAR

st.sidebar.markdown('# **Cultural Evolution of Group Identity study** **([preprint](https://osf.io/preprints/psyarxiv/ta9rq))**')

button_radio = st.sidebar.radio("Choose what you want to see:", 
                                ["Introduction", 
                                 "Task description", 
                                 "Traits: estimated valence",
                                 "Traits: estimated occurrence", 
                                 "Analysis of macro-patterns", 
                                 "Analysis of valences",
                                 "Analysis of individual traits"])

# button_1 = st.sidebar.button("Introduction")
# button_2 = st.sidebar.button("Task description")
# button_3 = st.sidebar.button("Analysis of valences")
# button_4 = st.sidebar.button("Analysis of traits")
selected_selectbox = "Attractive"
selected_selectbox = st.sidebar.selectbox('Which trait do you want to analyze?', traits_list)
# selected_selectbox = "Attractive"
# selected_selectbox = st.sidebar.selectbox('Which trait do you want to analyze?', traits_list)



#%% NO BUTTON PRESSED

# if (button_1 == False & button_2 == False & button_3 == False & button_4 == False):
#     st.title('Dashboard for the result of the CultEvoSelf study')
#     st.markdown('This is a dashboard allowing you to explore the results of the CultEvoSelf study .')


#%% BUTTON == 'Introduction' or none pressed

if button_radio == 'Introduction':
    st.title('Introduction')
    st.markdown('This is a dashboard allowing you to explore the results of our [study on cultural evolution of group identity](https://osf.io/preprints/psyarxiv/ta9rq).')
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
    st.markdown(''' 
                Minimal group paradigm is an experimental method to study social identity in the lab. The main idea is to divide 
                participants into groups based on arbitrary and irrelevant features. For example, let’s say you’re in a school 
                class and the teacher randomly divides the class into two groups: one group wears red shirts and the other group 
                wears orange shirts. Other examples can be as simple as telling participants that they belong to a "triangle" group 
                and the other group are "squares". Such research found that when people belong to such minimal groups they behave 
                in a way that favours their ingroup over an outgroup (see: Dunham, 2018; van Bavel & Packer, 2021). For example,
                thay might want to help others in their group more than those in the other group.
                ''')
    st.image(image='img/Villages - colors 01.png')
    st.markdown('### Cultural evolution')
    st.markdown(''' 
                Minimal groups allows us to investigate the processes at play when a new social identity is created. 
                However, our social identity is primarily formed by groups that have existed for years, centuries or even 
                millenia (for example nations and religions). These large-scale identities often emerged as a consequence of 
                relatively small distinctions, but relatively small initial differences accumulated and led to huge cultural 
                differences. For example, it is assumed that the majority of European languages come from the same root: the 
                protoindoeuropean language. It subsequently evolved into such diverse contemporary languages like English, 
                Italian, Polish, Albanian, Hindi and Persian. It means that small group divisions that happened thousands of 
                years ago evolved into full-blown languages, and consequently language-based identites. Such large identities 
                are not only social, but also cultural phenomena. And the field of cultural evolution investigates what drives
                processes of emergence and development of culture.
                ''')
    st.markdown('### What is a transmission chain')
    st.markdown(''' 
                Transmission chain is a method to investigate how information changes when it is repeatedly transmitted between 
                people. It is very similar to the children's game "Chinese whispers", known also as "Deaf telephone" in some countries.
                In this game, the first person (a seed) transmits some information to another person. Then that second person transmits 
                this information to another person and so on... until it reaches the last person. A sequence of people through 
                which this information travelled is called a **chain**, and each person in this chain is known as a **generation**.
                Transmission chains allow us to see how information changes if it is repeatedly transmitted to another person and what 
                kind of distortions can emerge during that process.  
                ''')
    st.image(image='img/fig0_transmissionchain.png')
    st.markdown('### What we found')
    st.markdown('''
                What allows culture to change over time are mistakes that people make when they transmit information to each other. 
                In our study we observed two types of mistakes among our participants. First, we found that when representing numbers 
                on a line our participants had the tendency to indicate position that was lower than the real one. For example, if 
                they were told that 40% of members of a group have some trait, they would on average indicate a position on the line 
                that corresponds to 37%. This small response bias would then lead all traits to steadily decrease over time.  
                The second type of errors happened when participants confused which number described which group. This happened when 
                for example I saw that 70% of the outgroup and 40% of my ingroup are friendly, and then I indicated that 70% of my 
                ingroup and 40% of the outgroup are friendly. This mistake most likely happened when participants misremembered the 
                numbers, but it is also possible that in some cases they made this mistake on purpose.
                
                
                We discovered that when people transmit information about positive and neutral traits describing their ingroup then 
                these mistakes were slightly smaller than when they were transmitting information about the outgroup. As a result, 
                at the end of the transmission chains positive and neutral traits were on average more common in ingroup than in the 
                outgroup. For example, if both groups were perceived as equally intelligent in the beginning (50% of people are 
                rated as intelligent in both groups) then after 10 generations, 43% remained intelligent in the ingroup and only 36% 
                in the outgroup. Similar effect happened for the neutral traits, but not for the negative traits. Negative traits 
                at generation 10 were not different between the groups (negative traits were slightly more frequent in the outgroup, 
                but this effect was not strong enough to be statistically significant).

                Why does it happen? We propose that this came as a result of two processes:
                (1) Participants were more motivated to be accurate when transmitting information about the ingroup than outgroup
                (2) Participants had the tendency to slightly distort transmitted information to make the ingroup more positive and
                less negative than the outgroup  (so called "ingroup-bias")
                If these two processes are at play at the same time then they should cancel each other out leading to no differences 
                between groups for negative traits, and work in the same direction for positive and neutral traits - just like we 
                observed.

                Our results illustrate how even unconscious small biases can accumulate over time and lead to increased group 
                polarization. While we did not find such an effect for negative traits, we did find it for positive traits what 
                might also be the driver behind seeing another group in a comparatively worse light. 
                
                ''')
    st.image(image='img/Chinese whispers2.png')
    st.markdown(''' 
                This dashboard allows you to have a closer look at the results of our study. For a longer discussion of our 
                results check our scientific paper, which you can find under the following link: 
                **[Preprint](https://osf.io/preprints/psyarxiv/ta9rq)**. 
                However, an article does not allow to present full results in an interactive manner. Here you can do just that.
                ''')
    st.markdown('''
                In the section "Task description" you can familiarize yourself with the procedure of our experiment, and 
                in the "Analysis..." sections you can look at our results. 
                ''')
    st.markdown('### References')
    st.markdown(''' 
                van Bavel, J., Packer, D.J. (2021). *The power of Us. Harnessing our shared identities to improve performance, increase cooperation, and promote social harmony*. Little, Brown Spark.  
                Boyd, R., Richerson, P.J. (1985). *Culture and the evolutionary process*. The University of Chicago Press.  
                Dunham, Y. (2018). Mere Membership. *Trends in Cognitive Sciences*, 22(9), 780-793.  
                Mesoudi, A. (2011). *Cultural evolution*. The University of Chicago Press.  
                Morin, O. (2016). *How traditions live and die*. Oxford University Press.  
                ''')

#%% BUTTON == 'Task description'

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
    
#%% BUTTON == 'Traits: estimated valence'

if button_radio == 'Traits: estimated valence':
    st.title("Traits: estimated valence")
    st.markdown('''This section shows how negative/positive each trait used in the study was judged. 
                Responses were given on a scale from 1 (very negative) to 7 (very positive).
                It shows the results of an additional study conducted with 26 participants. 
                ''')
    
    # Prepare the table
    traits_tab = val_summary#.iloc[:,2:23]
    traits_tab = traits_tab.loc[['mean', 'std', '25%', '50%', '75%'],:].transpose().round(2)
    
    # Tables - separately for each valence
    st.markdown("##### Negative traits")
    st.table(traits_tab.iloc[3:9,:].style.format("{:.2f}"))
    st.markdown("##### Neutral traits")
    st.table(traits_tab.iloc[9:15,:].style.format("{:.2f}"))
    st.markdown("##### Positive traits")
    st.table(traits_tab.iloc[15:21,:].style.format("{:.2f}"))
    st.markdown("##### Additional traits")
    st.markdown('''Attractive is an additional trait, because it is not a psychological trait (unlike the other positive traits). 
                Political and religious are additional traits, because they showed the greatest variability in whether they 
                were judged as positive, negative or neutral.''')
    st.table(traits_tab.iloc[0:3,:].style.format("{:.2f}"))
    
    # comparison between valences
    st.markdown('### Comparison between valences')
    
    # with st.echo():
    #     from statsmodels.stats.anova import AnovaRM
    #     # Perform ANOVA
    #     data_long = pd.melt(df_Occurr, 
    #                         id_vars='participant_num', 
    #                         value_vars=['Negative', 'Neutral', 'Positive'], 
    #                         var_name='Valence', value_name='Occurrence')
    #     resA = AnovaRM(data=data_long, 
    #                    depvar='Occurrence', 
    #                    subject='participant_num', 
    #                    within=['Valence']).fit()        
    # st.markdown('**Results:**')
    # st.code(resA)
        
        
    data_occ = df_Valence[['Negative', 'Neutral', 'Positive']]
    fig, ax = plt.subplots()
    sns.set(font_scale=2)
    sns.set_style('whitegrid')
    fig.set_size_inches(18.5, 10.5)
    plt.boxplot(data_occ[['Negative', 'Neutral', 'Positive']])
    ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])#, fontsize=20)
    st.pyplot(fig)
    

#%% BUTTON == 'Traits: estimated occurrence'

if button_radio == 'Traits: estimated occurrence':
    st.title("Traits: estimated occurrence")
    st.markdown('''This section shows how frequent each trait is believed to be in a general population.
                Responses were given as percentages.            
                It shows the results of an additional study conducted with 51 participants. 
                ''')
    
    # Prepare the table
    traits_tab = occ_summary.iloc[:,2:23]
    traits_tab = traits_tab.loc[['mean', 'std', '25%', '50%', '75%'],:].transpose().round(2)
    
    # Tables - separately for each valence
    st.markdown("##### Negative traits")
    st.table(traits_tab.iloc[3:9,:].style.format("{:.2f}"))
    st.markdown("##### Neutral traits")
    st.table(traits_tab.iloc[9:15,:].style.format("{:.2f}"))
    st.markdown("##### Positive traits")
    st.table(traits_tab.iloc[15:21,:].style.format("{:.2f}"))
    st.markdown("##### Additional traits")
    st.markdown('''Attractive is an additional trait, because it is not a psychological trait (unlike the other positive traits). 
                Political and religious are additional traits, because they showed the greatest variability in whether they 
                were judged as positive, negative or neutral.''')
    st.table(traits_tab.iloc[0:3,:].style.format("{:.2f}"))
    
    #st.table(traits_tab.style.format("{:.2f}"))
    
    # comparison between valences
    st.markdown('### Comparison between valences')
    
    with st.echo():
        from statsmodels.stats.anova import AnovaRM
        # Perform ANOVA
        data_long = pd.melt(df_Occurr, 
                            id_vars='participant_num', 
                            value_vars=['Negative', 'Neutral', 'Positive'], 
                            var_name='Valence', value_name='Occurrence')
        resA = AnovaRM(data=data_long, 
                       depvar='Occurrence', 
                       subject='participant_num', 
                       within=['Valence']).fit()        
    st.markdown('**Results:**')
    st.code(resA)
        
    # Boxplot 
    data_occ = df_Occurr[['Negative', 'Neutral', 'Positive']]
    fig, ax = plt.subplots()
    sns.set(font_scale=2)
    sns.set_style('whitegrid')
    fig.set_size_inches(18.5, 10.5)
    plt.boxplot(data_occ[['Negative', 'Neutral', 'Positive']])
    ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])#, fontsize=20)
    st.pyplot(fig)
    
    
    
    # Correlation with generation 10
    df_gen10 = df_ALL.loc[df_ALL['id_exp_participant']==10]
    # Ingroup data
    gen10_in = df_gen10.loc[:,[i+'_In_response' for i in traits_codes] ]
    dict_in = { list(gen10_in.columns)[i]: traits_list[i] for i in range(len(traits_list)) }
    gen10_in.rename(columns=dict_in, inplace=True)
    gen10_in = gen10_in.mean()
    # Outgroup data
    gen10_out = df_gen10.loc[:,[i+'_Out_response' for i in traits_codes] ]
    dict_out = { list(gen10_out.columns)[i]: traits_list[i] for i in range(len(traits_list)) }
    gen10_out.rename(columns=dict_out, inplace=True)
    gen10_out = gen10_out.mean()
    
    # Occurence data
    df_occurence = occ_median[2:23,]
    
    # Concatenate
    df_occ_corr = pd.concat([df_occurence, gen10_in, gen10_out], axis=1)
    df_occ_corr.rename(columns={ 0:'Occurence', 1:'Generation 10: Ingroup', 2:'Generation 10: Outgroup' }, inplace=True)

    # Run correlation analyses
    st.markdown('### Correlation with generation 10')
    st.markdown('''Pearson r correlation between reported occurences in general population
                and frequency of occurence in generation 10 for minimal ingroup and outgroup.
                None of the correlations is statistically significant.''')
    st.table(df_occ_corr.corr().style.format("{:.2f}"))
    
    # Table for Occurrences and Generation 10 average
    # gen10 = (gen10_in + gen10_out)/2
    # st.markdown('### Means for averages in generation 10')
    # st.table(gen10.style.format("{:.2f}"))
    

#%% BUTTON == 'Analysis of macro-patterns'

if button_radio == 'Analysis of macro-patterns':
    st.title("Analysis of macro-patterns")
    st.markdown('''Here you can see how all of the traits behaved across generations. It means that the data here comes from 
                all types of traits. Each individual trait can be displayed on a plot where x-axis represent the percentage of 
                occurrence of that trait in the ingroup and y-axis shows the percentage of occurrence of that trait in the 
                outgroup. Below you can see the locations of all traits at the begiining of the experiment: these are the 
                values that we gave to the first participants in each chain.''')
    st.markdown('### Data at Generation 0 (seed values)')
    st.image(image='img/All_Generation_0.png')
    st.markdown('''Initially all of these points were close to the centre. However, across generations these points started to 
                spread out, as you can see in teh gif below.''') 
    st.markdown('### Behaviour of data points across generations')
    st.image(image='img/unclastered_all_gens.gif')
    st.markdown('Below you can see the location of the datapoints when they reached the final generation.')
    st.markdown('### Data at the final generation (Generation 10)')
    st.image(image='img/All_Generation_10.png')
    st.markdown('''You can see that these points appear to head towards one of four places: centre, bottom-left corner, 
                left-centre and bottom-centre''')
    st.markdown('## Cluster analysis')
    st.markdown('''Cluster analysis is a statistical technique that allows to discover clusters in the data: groups
                of data points that are similar to each other. A silhouette score indicated that there were 4 clusters in 
                our data (max score=0.599), so we conducted K-means clustering on the data from the final generation to 
                classify all data points into these 4 clusters. Below you can see the results of our classification.''')
    st.markdown('### Cluster analysis of Generation 10')
    st.image(image='img/generation_10.png')
    st.markdown('''At the next step we decided to check whether the initial position of the data points was related to the 
                final position, so we applied the same classification but to the data from the seed values. Below you can 
                see the results which show that the initial position was strongly related to the final position at 
                generation 10 (our additional analysis using decision trees showed that by knowing the initial position 
                you can know the final position with 60.6% accuracy).''')
    st.markdown('### Detected clusters applied to the seed values')
    st.image(image='img/generation_00.png')
    st.markdown('''Below you can see how each cluster evolved over time.''')
    st.markdown('### Behaviour of clusters across generations')
    st.image(image='img/gif1.gif')
    
    
    # # Visualize the data to be clustered - Scatterplot of Gen10 values
    # df_allSeedGen10 = df_allTraits.loc[df_allTraits['Generation']==10]
    # #sns.scatterplot(data=df_gen10, x='In_response', y='Out_response')
    
    # # Set plot style
    # sns.set(font_scale=2)
    # sns.set_style('whitegrid')
    # fig, ax1 = plt.subplots()
    # fig.set_size_inches(10, 10)

    # # Produce Lineplot + Stripplot
    
    # # Add the 50% line
    # plt.plot([0, 10], [50, 50], color='grey')
    
    # plt.figure(2)
    # jittersize = 3
    # res = np.random.random_sample(size = len(df_allSeedGen10))*jittersize - 0.5*jittersize
    # df_allSeedGen10['In_Seed_jitter'] =  df_allSeedGen10['In_Seed'] + res
    # res = np.random.random_sample(size = len(df_allSeedGen10))*jittersize - 0.5*jittersize
    # df_allSeedGen10['Out_Seed_jitter'] =  df_allSeedGen10['Out_Seed'] + res
    # #g = sns.scatterplot(data=df_allSeedGen10, x='In_Seed_jitter', y='Out_Seed_jitter', hue=Y0, palette='Set1') # y0_predict
    # #voronoi_plot_2d(vor0,plt.gca())
    # #plt.scatter(cluster_centers0[:,0], cluster_centers0[:,1], marker='^', s=300, c='k', alpha=0.6)
    #g.set(xlim=(0,100))
    #g.set(ylim=(0,100))
    # plt.plot([0, 100], [50, 50], linewidth=2, color='k')
    # plt.plot([50, 50], [100, 0], linewidth=2, color='k')
    # plt.xlabel('Occurence in the ingroup [%]')
    # plt.ylabel('Occurence in the outgroup [%]')
    
    # # Display in streamlit
    # st.pyplot(fig)
    
    #st.image(image='img/Villages - colors 01.png')
        
#%% BUTTON == 'Analysis of valences'

if button_radio == 'Analysis of valences':
    st.title("Analysis of valences")
    st.markdown('''Here you can see transmission chains for averages of traits representing three valences:
                positive, neutral, and negative. Green colour represents transmission chains for the minimal ingoup 
                (your village), and red lines represent the minimal outgroup (strangers' village). 
                Black start on the right represents the median frequency in general population, as indicated 
                by our additional survey. ''')
    
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
    df_lmm2['group'] = df_lmm2['group'].map({ 'Avg_In_'+trait_valence: 'Ingroup', 'Avg_Out_'+trait_valence: 'Outgroup' })
    
    # Set plot style
    sns.set(font_scale=2)
    sns.set_style('whitegrid')
    fig, ax1 = plt.subplots()
    fig.set_size_inches(18, 10)

    # Produce Lineplot + Stripplot
    
    # Add the 50% line
    plt.plot([0, 10], [50, 50], color='grey')

    # SCATTERPLOT
    # SEABORN: ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait_valence, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    # Ingroup
    x = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'Avg_'+trait_valence]
    ax1 = plt.scatter(x=x, y=y, color='green')
    # Outgroup
    x = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'Avg_'+trait_valence]
    ax1 = plt.scatter(x=x, y=y, color='red')

    # LINEPLOT
    # SEABORN: #ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait_valence, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] )
    # Ingroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').mean().reset_index()
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait_valence]
    ax1 = plt.plot(x, y, color='green', label='Ingroup')
    # Confidence interval
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait_valence,'std')] / np.sqrt(df_sd[('Avg_'+trait_valence,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:green')
    
    # Outgroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').mean().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait_valence]
    ax1 = plt.plot(x, y, color='red', label='Outgroup')
    # Confidence interval
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait_valence,'std')] / np.sqrt(df_sd[('Avg_'+trait_valence,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:red')
    
    
    
    # Other settings
    trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
    #ax1.set(title='Traits: '+trait_valence_labels[trait_valence], xlabel='Generation', ylabel='FOT: Frequency of occurrence of a trait [%]')    
    fig.suptitle('Traits: '+trait_valence_labels[trait_valence])
    plt.xlabel('Generation')
    plt.ylabel('FOT: Frequency of occurrence of a trait [%]')
    plt.legend(loc="lower left")
    
    # Add the point of believed occurrence in general population
    plt.plot([10], [med_pos], marker='*', ls='none', ms=35, markerfacecolor='black')
    
    # Display in streamlit
    st.pyplot(fig)
    
    
    ################ NEUTRAL
    st.markdown('### Neutral traits')
    st.markdown('Neutral traits were: Trendy, Busy, Traditional, Predictable, Introverted, Mystical')    
    # Neutral valence
    trait_valence = 'Neu'
    # Rearrange the data
    df_lmm2 = pd.melt(df_ALL, 
                      id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                      value_vars=['Avg_In_'+trait_valence, 'Avg_Out_'+trait_valence], 
                      var_name ='group', 
                      value_name ='Avg_'+trait_valence)
    df_lmm2['group'] = df_lmm2['group'].map({ 'Avg_In_'+trait_valence: 'Ingroup', 'Avg_Out_'+trait_valence: 'Outgroup' })
    
    # Set plot style
    sns.set(font_scale=2)
    sns.set_style('whitegrid')
    fig, ax1 = plt.subplots()
    fig.set_size_inches(18, 10)

    # Produce Lineplot + Stripplot
    
    # Add the 50% line
    plt.plot([0, 10], [50, 50], color='grey')

    # SCATTERPLOT
    # SEABORN: ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait_valence, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    # Ingroup
    x = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'Avg_'+trait_valence]
    ax1 = plt.scatter(x=x, y=y, color='green')
    # Outgroup
    x = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'Avg_'+trait_valence]
    ax1 = plt.scatter(x=x, y=y, color='red')

    # LINEPLOT
    # SEABORN: #ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait_valence, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] )
    # Ingroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').mean().reset_index()
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait_valence]
    ax1 = plt.plot(x, y, color='green', label='Ingroup')
    # Confidence interval
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait_valence,'std')] / np.sqrt(df_sd[('Avg_'+trait_valence,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:green')
    
    # Outgroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').mean().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait_valence]
    ax1 = plt.plot(x, y, color='red', label='Outgroup')
    # Confidence interval
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait_valence,'std')] / np.sqrt(df_sd[('Avg_'+trait_valence,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:red')
    
    
    
    # Other settings
    trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
    #ax1.set(title='Traits: '+trait_valence_labels[trait_valence], xlabel='Generation', ylabel='FOT: Frequency of occurrence of a trait [%]')    
    fig.suptitle('Traits: '+trait_valence_labels[trait_valence])
    plt.xlabel('Generation')
    plt.ylabel('FOT: Frequency of occurrence of a trait [%]')
    plt.legend(loc="lower left")
    
    # Add the point of believed occurrence in general population
    plt.plot([10], [med_neu], marker='*', ls='none', ms=35, markerfacecolor='black')
    
    # Display in streamlit
    st.pyplot(fig)
    
    
    ################ NEGATIVE
    st.markdown('### Negative traits')
    st.markdown('Negative traits were: Corrupt, Dishonest, Lazy, Without empathy, Impolite, Cowardly')    
    # Negative valence
    trait_valence = 'Neg'
    # Rearrange the data
    df_lmm2 = pd.melt(df_ALL, 
                      id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                      value_vars=['Avg_In_'+trait_valence, 'Avg_Out_'+trait_valence], 
                      var_name ='group', 
                      value_name ='Avg_'+trait_valence)
    df_lmm2['group'] = df_lmm2['group'].map({ 'Avg_In_'+trait_valence: 'Ingroup', 'Avg_Out_'+trait_valence: 'Outgroup' })
    
    # Set plot style
    sns.set(font_scale=2)
    sns.set_style('whitegrid')
    fig, ax1 = plt.subplots()
    fig.set_size_inches(18, 10)

    # Produce Lineplot + Stripplot
    
    # Add the 50% line
    plt.plot([0, 10], [50, 50], color='grey')

    # SCATTERPLOT
    # SEABORN: ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait_valence, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    # Ingroup
    x = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'Avg_'+trait_valence]
    ax1 = plt.scatter(x=x, y=y, color='green')
    # Outgroup
    x = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'Avg_'+trait_valence]
    ax1 = plt.scatter(x=x, y=y, color='red')

    # LINEPLOT
    # SEABORN: #ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait_valence, data=df_lmm2, hue='group', err_style='band', ci=95, palette = ['g', 'r'] )
    # Ingroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').mean().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait_valence]
    ax1 = plt.plot(x, y, color='green', label='Ingroup')
    # Confidence interval
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait_valence,'std')] / np.sqrt(df_sd[('Avg_'+trait_valence,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:green')
    
    # Outgroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').mean().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait_valence]
    ax1 = plt.plot(x, y, color='red', label='Outgroup')
    # Confidence interval
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait_valence] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait_valence,'std')] / np.sqrt(df_sd[('Avg_'+trait_valence,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:red')
    
    # Other settings
    trait_valence_labels = {'Pos': 'Positive', 'Neu': 'Neutral', 'Neg': 'Negative'}
    #ax1.set(title='Traits: '+trait_valence_labels[trait_valence], xlabel='Generation', ylabel='FOT: Frequency of occurrence of a trait [%]')    
    fig.suptitle('Traits: '+trait_valence_labels[trait_valence])
    plt.xlabel('Generation')
    plt.ylabel('FOT: Frequency of occurrence of a trait [%]')
    plt.legend(loc="lower left")
    
    # Add the point of believed occurrence in general population
    plt.plot([10], [med_neg], marker='*', ls='none', ms=35, markerfacecolor='black')
    
    # Display in streamlit
    st.pyplot(fig)
    
    
#%% BUTTON == 'Analysis of individual traits'

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
    st.markdown('''Black star on the right represents the median frequency in general population, as indicated 
                by our additional survey. ''')
    
    trait = inv_map[selected_selectbox]
    
    # Rearrange the data
    df_lmm2 = pd.melt(df_ALL, 
                      id_vars=['participant_exp_code', 'id_exp_chain', 'id_exp_participant'], 
                      value_vars=[trait+'_In_response', trait+'_Out_response'], 
                      var_name ='group', 
                      value_name ='Avg_'+trait)
    
    df_lmm2['group'] = df_lmm2['group'].map({ trait+'_In_response': 'Ingroup', trait+'_Out_response': 'Outgroup' })
    
    # Set plot style
    sns.set(font_scale=2)
    sns.set_style('whitegrid')
    fig, ax1 = plt.subplots()
    fig.set_size_inches(18, 10)
    
    # LINEPLOT + SCATTERPLOT (stripplot)
    
    # Add the 50% line
    plt.plot([0, 10], [50, 50], color='grey')
    
    # SCATTERPLOT
    # SEABORN: ax1 = sns.stripplot(x="id_exp_participant", y='Avg_'+trait, data=df_lmm2, hue='group', palette = ['g', 'r'] )
    # Ingroup
    x = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Ingroup', 'Avg_'+trait]
    ax1 = plt.scatter(x=x, y=y, color='green')
    # Outgroup
    x = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'id_exp_participant']
    y = df_lmm2.loc[ df_lmm2['group']=='Outgroup', 'Avg_'+trait]
    ax1 = plt.scatter(x=x, y=y, color='red')


    # LINEPLOT
    # SEABORN: #ax1 = sns.lineplot(x='id_exp_participant', y='Avg_'+trait, data=df_lmm2) #, hue='group') #, err_style='band', ci=95, palette = ['g', 'r'] )
    # Ingroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait] ].groupby('id_exp_participant').mean().reset_index()    
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait]
    ax1 = plt.plot(x, y, color='green', label='Ingroup')
    
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Ingroup', ['id_exp_participant', 'Avg_'+trait] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait,'std')] / np.sqrt(df_sd[('Avg_'+trait,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:green')
    # Outgroup
    df_mean = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait] ].groupby('id_exp_participant').mean().reset_index()
    x = df_mean['id_exp_participant']
    y = df_mean['Avg_'+trait]
    ax1 = plt.plot(x, y, color='red', label='Outgroup')
    
    df_sd = df_lmm2.loc[ df_lmm2['group']=='Outgroup', ['id_exp_participant', 'Avg_'+trait] ].groupby('id_exp_participant').describe().reset_index()
    conf_int = (df_sd[('Avg_'+trait,'std')] / np.sqrt(df_sd[('Avg_'+trait,'count')]) ) * 1.96
    plt.fill_between(x, y-conf_int, y+conf_int, alpha=0.1, color='tab:red')
    
    # Adjust the figure
    plt.ylim([0,100])
    fig.suptitle('Trait: '+trait_labels[trait])
    plt.xlabel('Generation')
    plt.ylabel('FOT: Frequency of occurrence of a trait [%]')
    plt.legend(loc="lower left")
    #ax1.set(title='Trait: '+trait_labels[trait], xlabel='Generation', ylabel='FOT [%]')
    

    # Add the point of believed occurrence in general population
    plt.plot([10], [occ_median[trait_labels[trait]]], marker='*', ls='none', ms=35, markerfacecolor='black')
    
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
    
    
    # TABLE OF PERCENTAGES AT EACH GENERATION
    st.markdown('### Average percentage of occurrence in each generation')
    st.markdown(f'''The table shows average percentage of occurrence of the trait {trait_labels[trait]} in each generation
                separately for ingroup and outgroup.''')
    
    # Calculate and print table
    averages = df_lmm2.groupby(['group', 'id_exp_participant']).mean()['Avg_'+trait].reset_index()
    averages = pd.pivot(averages, index='group', columns='id_exp_participant')
    averages.columns = averages.columns.droplevel(0)
    st.table(averages.style.format("{:.1f}"))
    
    
    
    # MIXED MODEL 
    st.markdown('### Linear mixed model results')
    st.markdown('''The table below shows the results of a linear mixed model analysis performed for Group and Generation. 
                Chain was treated as a random factor.''')
                
    df_lmm = df_lmm2.rename({'participant_exp_code':'Participant', 'id_exp_chain':'Chain', 'id_exp_participant':'Generation', 'group':'Group', 'Avg_'+trait:'Average'}, axis=1) 
    # Specify the model
    md = smf.mixedlm("Average ~ Group + Generation + Group*Generation", data=df_lmm, groups=df_lmm["Chain"]) # , vc_formula = {"Generation" : "0"})
    
    # Model with random slope and intercept - with uncorrelated random slope and intercept
    #md = smf.mixedlm("Average ~ Group + Generation + Group*Generation", data=df_lmm, groups=df_lmm["Chain"], vc_formula = {"Generation" : "0 + Generation"})
    # Model with random slope and intercept - with correlated random slope and intercept
    #md = smf.mixedlm("Average ~ Group + Generation + Group*Generation", data=df_lmm, groups=df_lmm["Chain"], vc_formula = {"Generation" : "1 + Generation"})
    
    # Fit the model
    mdf = md.fit()
    
    
    st.code(mdf.summary())
    
    
    # ADDITIONAL INFORMATION
    st.markdown('### Additional information')
    
    st.markdown(f'''A table showing the number of flips in one and the other direction.''')
    t = df_ALL[trait+'_InOut_change_YesNo'].value_counts()
    t = t.rename({0:'No flip', 1:'Flip: Ingroup becomes bigger', -1:'Flip: Outgroup becomes bigger', 3:'Values were the same'}, axis=0)
    t = t.sort_index()
    st.table(t)
    
    # # CLUSTERING
    # filename = "CultEvo_kmeans.pickle"
    # kmeans = pickle.load(open(filename, "rb"))
    # X = df_ALL.loc[df_ALL['id_exp_participant']==10,:].loc[:,[trait+'_In_response', trait+'_Out_response']]
    # X = X.rename({
    #     trait+'_In_response':'In_Gen10',
    #     trait+'_Out_response':'Out_Gen10'
    #     }, axis=1)
    # y_predict = kmeans.predict(X)
    # cluster_centers = kmeans.cluster_centers_
    
    # clusters_table = np.array([
    #     [np.count_nonzero(y_predict == 1), np.count_nonzero(y_predict == 2)],
    #     [np.count_nonzero(y_predict == 3), np.count_nonzero(y_predict == 0)]
    #     ])
    # df_clusters = pd.DataFrame(clusters_table, 
    #                            index=['Outgroup = 50%', 'Outgroup = 10%'], 
    #                            columns=['Ingroup = 10%', 'Ingroup = 50%'])


    # st.markdown(f'''A table showing the number of chains that finished close to each attractor, as determined 
    #             by k-means cluster analysis.''')
    # st.table(df_clusters)
    
    
#%% TEST

# df_ALL = pd.read_csv('All_CultEvoSelf_Exp1_S.csv')

# df_test =  df_ALL.loc[:,:] #df_ALL.loc[:, ['id_exp_chain', 'participant_exp_code']] # creates a deep copy
# df_test2 = df_test
# df_test3 = df_test.copy()

# df_test.iloc[0,1] = 9999

# print('df_ALL: '+str(df_ALL.iloc[0,1]))
# print('df_test: '+str(df_test.iloc[0,1]))
# print('df_test2: '+str(df_test2.iloc[0,1]))
# print('df_test3: '+str(df_test3.iloc[0,1]))



