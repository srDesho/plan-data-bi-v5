# basic packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from scipy.stats import chi2_contingency
from scipy.stats import zscore
from summarytools import dfSummary
from itertools import combinations
import random
from collections import Counter
from sklearn.preprocessing import PowerTransformer

#statistics packages

from statsmodels.stats.weightstats import ztest
from scipy.stats import normaltest, kstest,wilcoxon,shapiro,chi2_contingency

# ml packages

from sklearn.model_selection import train_test_split

# set up

pd.set_option('display.max_columns', 500)
random.seed(42)
np.random.seed(42)
warnings.filterwarnings('ignore')

# global variable

UNIQUE_KEY = 'nro_cuenta'
CHURN_VARIABLE = 'PRE2POS'

# functions

def cleaning_up(x,umbral):

    if pd.isna(x):
        return np.nan
    else:
        if x >umbral:
            return umbral
        else:
            return x


def variability(variable):
    try:
        std = np.std(np.abs(variable))
        rng = np.max(np.abs(variable))-np.min(np.abs(variable))
        x = std/rng
        return x 
    except ZeroDivisionError:
        return 0

def categorize(variable, bins):
    new_var = pd.cut(variable, bins = bins)
    return new_var

def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x,y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))

def multcorr(df, method = 'pearson'):
    df_corr = round(df.corr(method=method),2) # befone spearman method was applied
    mask = np.triu(np.ones_like(df_corr, dtype=bool))
    
    sns.heatmap(df_corr, annot = True, mask=mask)
    plt.show()

def interval_zscore(x):
    if x <=3 and x>=-3:
        return 'INSIDE'
    elif x >3:
        return 'UPPER'
    elif x<-3:
        return 'LOWER' 

def save_sample(limit,real_value,inf_value,sup_value):
    if limit == 'INSIDE':
        return real_value
    elif limit == 'UPPER':
        return sup_value
    elif limit == 'LOWER':
        return inf_value

def remove_observations_by_normalization_for_closing(dataframe_joined, variable_name):
   """Funcion que limpia los datos con base a normalizacion, donde todo lo que esta a +-3 desviaciones estandares, se retira

    Parameters
    ----------
    dataframe_joined : dataframe
        Es el dataframe que tiene las identificaciones de las filas y todas las variables
    
    variable_name : str
        Es el nombre de la variable de la cual se quiere remover las observaciones con base a la normalizacion

    Returns
    -------
    list
        Es una lista con las observaciones que fueron removidas
    """

   df_sample = dataframe_joined[[variable_name]]
   df_sample['Z_NORM'] = zscore(df_sample[variable_name])

   df_sample['LIMIT'] = df_sample.Z_NORM.apply(lambda x: interval_zscore(x))

   inf_limit = df_sample[df_sample.LIMIT == 'INSIDE'][variable_name].min()
   sup_limit = df_sample[df_sample.LIMIT == 'INSIDE'][variable_name].max()

   df_sample[variable_name] = df_sample.apply(lambda x: save_sample(x['LIMIT'],x[variable_name],inf_limit,sup_limit), axis = 1)

   return df_sample.drop(['Z_NORM','LIMIT'],axis =1)

def churn_dist_cat(x_name,df_sample,y_name,id_obs,intervals=10,clear_table='no',lower_y = 0, equals_part = 'no'):

    """Function that graphs and displays a table with info about cross two variables, commonly for churn explorations 

    Parameters
    ----------
    x_name : str
        name x variable for exploration
        
    df_sample : dataframe
        dataframe with all data avaialbe

    y_name : str
        name y variable for exploration, it might be churn variable
    
    id_obs : str
        variable name that identify unique obs 
    
    intervals : int
        define intervals for study churn based on subsets

    clear_table : str
        apply a method for remove outliers based on normalization  

    Returns
    -------
    dataframe
        dataframe with intervals vs variable y
    """
    
    df_sample = df_sample.copy()

    if clear_table == 'yes':
        df_sample[x_name] = remove_observations_by_normalization_for_closing(df_sample, x_name)
        print(f'cleanning {x_name} variable.')

    if intervals !=0:
        if equals_part == 'no':
            df_sample[x_name] = pd.cut(df_sample[x_name],intervals)
            print(f'cutting into not equal parts, the {x_name} variable in {intervals} parts.')
        else:
            df_sample[x_name] = pd.qcut(df_sample[x_name],intervals,duplicates='drop')
            print(f'cutting into equal parts, the {x_name} variable in {intervals} parts.')


    a = pd.crosstab(index = df_sample[x_name], columns = df_sample[y_name], values = df_sample[id_obs], aggfunc = 'nunique', normalize = 'index')
    # display(a)

    contingency_table = pd.crosstab(df_sample[x_name], df_sample[CHURN_VARIABLE])
    # display(contingency_table)

    chi2, p, _, _ = chi2_contingency(contingency_table)

    print(f'chi2 data, p : {p}, chi2: {chi2}')

    b = df_sample[[id_obs,x_name]].groupby(x_name).count()
    c = a.join(b, on = x_name)
    # # d = dfSummary(df_sample[[x_name]])

    fig = a.plot(kind="bar", stacked=True, rot=90, grid=True, title=a.index.name) 
    plt.ylim(lower_y, 1)
    plt.show()
    # # display(c,d)EDAD
    display(c)

    del df_sample

def remove_ouliers(df_sample,vars_to_clear):
   
    df_sample = df_sample.copy()

    for var_name in vars_to_clear:
        try:
            df_sample[var_name] = remove_observations_by_normalization_for_closing(df_sample, var_name)
            print(f'the variable {var_name} was cleaned.')
        except:
            print(f'the variable {var_name} cant be clear')
    
    return df_sample

def check_normal_distribution(df_sample,var_x_name,var_class_name,alpha = 0.05):
    
    #drop nan obs for current variable
    df_sample = df_sample.dropna(subset = [var_x_name])

    list_unique_class = df_sample[var_class_name].unique().tolist()

    list_shapiro, list_kstest, list_normal_scipy  = [],[],[]

    for current_class in list_unique_class:
        data = df_sample[df_sample[var_class_name] == current_class][var_x_name].values

        list_kstest.append(kstest(data, 'norm')[1])
        list_shapiro.append(shapiro(data)[1])
        list_normal_scipy.append(normaltest(data,nan_policy='omit')[1])

    list_unique_class.append('ALL DATA')
    list_shapiro.append(shapiro(df_sample[var_x_name])[1])
    list_kstest.append(kstest(df_sample[var_x_name],'norm')[1])
    list_normal_scipy.append(normaltest(df_sample[var_x_name],nan_policy='omit')[1])

    df_normal_test = pd.DataFrame({'class_name':list_unique_class, 'shapiro_test':list_shapiro, 'kolmov_test':list_kstest, 'scipy_test':list_normal_scipy})
    
    for var_col in df_normal_test.iloc[:,1:].columns.tolist():
        df_normal_test[var_col + '_hypo'] = df_normal_test[var_col].apply(lambda x: 'not normal distribution' if  x < alpha else 'normal distribution')

    return df_normal_test

def get_distributions(df_sample,var_x_name,var_class_name):

    #default_colors
    list_colors = ['orange','green','blue','red','purple','brown','gray','cyan']

    #unique name class
    list_unique_class = df_sample[var_class_name].unique().tolist()

    list_colors = random.sample(list_colors, k=len(list_unique_class))

    #create a kde plot
    fig, ax = plt.subplots(figsize=(12, 6))

    for class_name, color_name in zip(list_unique_class,list_colors):

        sns.kdeplot(data=df_sample[df_sample[var_class_name] == class_name][var_x_name], color = color_name, label = class_name, fill=True, ax=ax)

    ax.legend()
    plt.tight_layout()
    plt.show()

def get_balanced_dataframe(df_sample,var_x_name,var_class_name):

    list_unique_class = df_sample[var_class_name].unique().tolist()

    df_selecction = df_sample.dropna(subset = [var_x_name]).groupby(var_class_name).agg({var_x_name:'count'}).sort_values(var_x_name).head(1)

    # min_class_name = df_selecction.index[0]
    n_to_extract = df_selecction.iloc[0][0]

    list_all_obs = []

    for class_name in list_unique_class:
        list_all_obs.append(df_sample[df_sample[var_class_name] == class_name].sample(n_to_extract, random_state = 42))
    
    df_final = pd.concat(list_all_obs)
    
    return df_final

def wilconox_test(df_sample,var_x_name,var_class_name,alpha = 0.05):
    
    #drop nan obs for current variable
    df_sample = df_sample.dropna(subset = [var_x_name])
    
    #this test required that groups have the same distribution
    df_sample =  get_balanced_dataframe(df_sample,var_x_name,var_class_name)

    #unique name class
    list_unique_class = df_sample[var_class_name].unique().tolist()

    #all posibles combinations take 2 by group
    possible_combinations = combinations(list_unique_class,2)

    list_comb,list_hypothesis,list_p_values,list_diff_means = [],[],[],[]

    for comb in list(possible_combinations):
        x,y = comb
        _, p_value_ttest = wilcoxon(df_sample[df_sample[var_class_name] == x][var_x_name], df_sample[df_sample[var_class_name] == y][var_x_name])

        list_p_values.append(p_value_ttest)
        list_comb.append(comb)
        list_diff_means.append(df_sample[df_sample[var_class_name] == x][var_x_name].mean() - df_sample[df_sample[var_class_name] == y][var_x_name].mean())

        if p_value_ttest < alpha:
            list_hypothesis.append('statistical differents')
        else:
            list_hypothesis.append('statistical equals')
    
    df_wilconox_combinations = pd.DataFrame({'COMBINATIONS':list_comb,'HYPOTHESIS':list_hypothesis,'WILCONOX_P_VALUE':list_p_values,'DIFF_MEANS':list_diff_means})

    return df_wilconox_combinations

def ztest_test(df_sample,var_x_name,var_class_name,alpha = 0.05):

    #drop nan obs for current variable
    df_sample = df_sample.dropna(subset = [var_x_name])

    #unique name class
    list_unique_class = df_sample[var_class_name].unique().tolist()

    #all posibles combinations take 2 by group
    possible_combinations = combinations(list_unique_class,2)

    list_comb,list_hypothesis,list_p_values,list_diff_means = [],[],[],[]

    for comb in list(possible_combinations):
        x,y = comb
        _, p_value_ztest = ztest(df_sample[df_sample[var_class_name] == x][var_x_name], df_sample[df_sample[var_class_name] == y][var_x_name])

        list_p_values.append(p_value_ztest)
        list_comb.append(comb)
        list_diff_means.append(df_sample[df_sample[var_class_name] == x][var_x_name].mean() - df_sample[df_sample[var_class_name] == y][var_x_name].mean() )

        if p_value_ztest < alpha:
            list_hypothesis.append('statistical differents')
        else:
            list_hypothesis.append('statistical equals')
    
    df_wilconox_combinations = pd.DataFrame({'COMBINATIONS':list_comb,'HYPOTHESIS':list_hypothesis,'Z_TEST_P_VALUE':list_p_values,'DIFF_MEANS':list_diff_means})

    return df_wilconox_combinations

def chi2_test(df_sample,var_x_name,var_class_name,alpha = 0.05):

    #drop nan values
    df_sample = df_sample.dropna(subset = [var_x_name])

    #unique name class
    list_unique_class = df_sample[var_class_name].unique().tolist()

    #control count unique element 
    list_q_unique_values = []
    for class_name in list_unique_class:
        list_q_unique_values.append(df_sample[df_sample[var_class_name] == class_name ][var_x_name].unique().shape[0])
    
    if (np.array(list_q_unique_values) == df_sample[var_x_name].unique().shape[0]).all():

        list_comb,list_hypothesis,list_p_values = [],[],[]

        #all class for chi2 test
        matrix = df_sample.pivot_table(index = var_x_name, columns = var_class_name, values = UNIQUE_KEY, aggfunc='count').T.values #search another var (CLIENTENRO) for define the count var

        display(df_sample.pivot_table(index = var_x_name, columns = var_class_name, values = UNIQUE_KEY, aggfunc='count'))
        
        p_value_chi2 = chi2_contingency(matrix)[1]

        # print(matrix,p_value_chi2)

        list_comb.append('ALL DATA')
        list_p_values.append(p_value_chi2)
    
        if p_value_chi2 < alpha:
            list_hypothesis.append('statistical differents')
        else:
            list_hypothesis.append('statistical equals')
        

        #all binary combinations
        possible_combinations = combinations(list_unique_class,2)

        for comb in list(possible_combinations):
            x,y = comb

            matrix = df_sample[df_sample[var_class_name].isin([x,y])].pivot_table(index = var_x_name, columns = var_class_name, values = UNIQUE_KEY, aggfunc='count').T.values #search another var (CLIENTENRO) for define the count var

            p_value_chi2 = chi2_contingency(matrix)[1]

            list_p_values.append(p_value_chi2)
            list_comb.append(comb)

            if p_value_chi2 < alpha:
                list_hypothesis.append('statistical differents')
            else:
                list_hypothesis.append('statistical equals')
        
        df_chi2_combinations = pd.DataFrame({'COMBINATIONS':list_comb,'HYPOTHESIS':list_hypothesis,'CHI2_P_VALUE':list_p_values})

        return df_chi2_combinations

    else:
        print('unique values have a problem...')

def ttest_with_shapiro(df_sample,var_x_name,var_class_name,alpha = 0.05,class_selector = 'any', clear_x = 'no', intervals = 10, lower_y = 0, apply_trans = 'no', equals_part = 'no'):

    # init process

    print('----------------------------- start --------------------------------', end = "\n\n")

    print(f'variable: {var_x_name}')

    df_sample = df_sample.dropna(subset = [var_x_name]) #drop nan values for the current variable

    unique_values = df_sample[var_x_name].unique().shape[0]

    print(f'count unique values for {var_x_name} is: {unique_values}')

    if  unique_values <= 15: # check if a variable has at least 10 unique values for cast to str
        
        print(f'cast to str, {var_x_name}')
        
        df_sample[var_x_name] = df_sample[var_x_name].astype(str)
        clear_x = 'no'
    
    if apply_trans == 'yes':

        pt = PowerTransformer()

        df_sample[var_x_name] = pt.fit_transform(df_sample[[var_x_name]])

    if clear_x == 'yes':
        
        df_sample = remove_ouliers(df_sample,[var_x_name]) # clear variable
        # print(f'clearing {var_x_name} variable.')
    
    df_summary = dfSummary(df_sample[[var_x_name]])
    display(df_summary)

    if df_sample[var_x_name].dtype == 'float' or df_sample[var_x_name].dtype == 'int' or df_sample[var_x_name].dtype == 'int64':

        print(f'the variable: {var_x_name} is quantitative. Run check normal distribution, z/t test and descriptive stats...')

        df_normal_distribution = check_normal_distribution(df_sample,var_x_name,var_class_name,alpha = alpha)

        if class_selector == 'any':
            current_flag = (df_normal_distribution['scipy_test_hypo'] == 'normal distribution').any()

        elif class_selector == 'all':
            current_flag = (df_normal_distribution['scipy_test_hypo'] == 'normal distribution').all()
        
        else:
            print('you choosed a incorrect option. Applying .any() method by default')
            current_flag = (df_normal_distribution['scipy_test_hypo'] == 'normal distribution').any()
        
        if current_flag:
            df_comparative_test = wilconox_test(df_sample,var_x_name,var_class_name) #the data have normal distribution
            print('the data have normal distribution, wilconox test applied')
        else:
            df_comparative_test = ztest_test(df_sample,var_x_name,var_class_name) #the data dont have normal distribution
            print('the data dont have normal distribution, ztest applied')

        # show descriptive statistics
        display(df_sample.groupby(var_class_name).agg({var_x_name:['mean','std','min','max']}),df_normal_distribution,df_comparative_test)
        
        get_distributions(df_sample,var_x_name,var_class_name)

        sns.displot(df_sample, x = var_x_name, hue=var_class_name, kind="ecdf")

        churn_dist_cat(var_x_name,df_sample,var_class_name,UNIQUE_KEY,intervals=intervals,clear_table='no',lower_y = lower_y, equals_part=equals_part)
 
    else:

        print(f'the variable: {var_x_name} is qualitative. Run chi2 test...')

        # df_chi2_frame =  chi2_test(df_sample,var_x_name,var_class_name,alpha = 0.05)
        # df_cross = pd.crosstab(index = df_sample[var_x_name], columns = df_sample[var_class_name], values=df_sample[UNIQUE_KEY], aggfunc='count')
        df_cross_pct = pd.crosstab(index = df_sample[var_x_name], columns = df_sample[var_class_name], values=df_sample[UNIQUE_KEY], aggfunc='count', normalize='index')
        # df_summary = dfSummary(df_sample[[var_x_name]])
        # display(df_chi2_frame,df_cross,df_cross_pct,df_summary)
        
        churn_dist_cat(var_x_name,df_sample,var_class_name,UNIQUE_KEY,0,clear_table='no',lower_y = lower_y,equals_part='no')
        sns.countplot(data = df_sample, x = var_x_name, hue = var_class_name)
        plt.xticks(rotation=90)
        plt.show()

        # display(df_cross_pct,df_summary)
        display(df_cross_pct)

    del df_sample
    print('----------------------------- end --------------------------------', end = "\n\n")