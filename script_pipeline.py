# -*- coding: utf-8 -*-
"""


@author: Safa Eladib
"""

# Problem Definition:
## Deduce TOP-10 most dangerous beaches in the world
import pandas as pd
year=int(input('Please enter the year: '))

def acquisition():
    df = pd.read_csv("data_set/GSAF5.csv",encoding = "ISO-8859-1")
    return df

def wrangle(df):
    global year
    filtered=df[df.Year>=year]
    return filtered

def clean(df):
    # remmoving usless columns
    print("---------------------------------begin cleaning---------------------------")
    df.drop(['Case Number','href formula','Unnamed: 22','Unnamed: 23','original order','href','pdf','Case Number.1','Case Number.2','Area','Name','Sex ','Injury','Date','Time','Species ','Investigator or Source'],axis=1, inplace=True)
    # check the column containing null value and remove all rows of those columns
    null_df = df.isna().sum()
    drop_cols_names = null_df[null_df>0].index.values
    list_columns = [i for i in drop_cols_names]
    # drop all nan values in the data set 
    df.dropna(subset=list_columns,inplace=True)
    print('---------------------------------End cleaning---------------------------')
    return df

def prepare_fatal_data(df):
    print("---------------------------------Begin preparation data for dangerousness level---------------------------")
    # preparing fatal column
    # rename the column Fatal (Y/N)
    df.rename(columns={'Fatal (Y/N)':'Fatal'},inplace=True)
    # check different value of fatal column
#     df.Fatal.unique()
    # delete all rows that fatal equal UNKNOWN
    df_index = df[df['Fatal']=='UNKNOWN'].index
    df.drop(df_index,inplace=True)

    df.Fatal = df.Fatal.str.replace(' N','N')
    # create dummies from fatal datas
    df = pd.get_dummies(df,columns=['Fatal'])
    print("---------------------------------End preparation data for dangerousness level---------------------------")
    return df
    
    
def analyze(df):
    print("---------------------------------Begin analyze data -------------------------------------")
    # analyze to determine the most dangerous beach in selectd year
    grouped = df.groupby(['Location','Country'])
    fatality = grouped.Fatal_Y.sum()
    # returned value mortality is a series
    fatality = fatality.to_frame(name='fatalities')

    # build a dataframe with grouped data in series grouped
    Fatality=pd.DataFrame()
    Fatality['Location']= [i for i in fatality.index]
    Fatality['Fatalities']= fatality.values
    dangerous = Fatality.sort_values('Fatalities', ascending=False).head(10)
    print("---------------------------------End analyze data-----------------------------------------")
    return dangerous

def viz(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    global year
    fig,ax=plt.subplots(figsize=(50,8))
    barchart=sns.barplot(data=df, x='Location',y='Fatalities')
    tit = "The most 10 dangerous beaches in the world since "+ str(year)
    plt.title(tit)
    return barchart

def save_viz(plot):
    fig=plot.get_figure()
    global year
    tit_fig = "The most 10 dangerous beaches in the world since "+ str(year)+".png"
    fig.savefig(tit_fig)
    
    
if __name__=='__main__':
    data=acquisition()
    filtered=wrangle(data)
    cleaned = clean(filtered)   
    prepared = prepare_fatal_data(cleaned)
    results=analyze(prepared)
    barchart=viz(results)
    save_viz(barchart)  
