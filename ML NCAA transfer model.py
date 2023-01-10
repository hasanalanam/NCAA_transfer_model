#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


ncaadata = pd.read_csv('/Users/HasanAlanam/Documents/Hasan/ncaa_transfer_data_source_2.csv')


# In[3]:


ncaadata.head()


# In[4]:


post = ['C']
forward = ['F']
guard = ['G']
postforward = ['F', 'C']
all  = ['G', 'F', 'C']
Years  = ['2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21']

#filtered_HM = MIN HM !=0
post_players = ncaadata[ncaadata['Position'].isin(all)] 


# In[5]:


from sklearn.linear_model import Ridge
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit


# In[6]:


rr = Ridge(alpha=1)
split = TimeSeriesSplit(n_splits=3)
sfs = SequentialFeatureSelector(rr, n_features_to_select=17, direction="forward", cv=split, n_jobs=4)


# In[7]:


removed_columns = ["Player", "SR_Code", "Nxt_season", "Nxt_season_start_yr", "Nxt_season_conf", "Nxt_VII", "Nxt_WS", "Nxt_MPG", "Nxt_PPG", "Nxt_RPG", "Nxt_APG", "Nxt_PER", "Nxt_USG%", "Nxt_BPM", "Season", "season_start_yr", "Position", "School", "Conf", "Lookup"]
selected_columns = post_players.columns[~post_players.columns.isin(removed_columns)]


# In[8]:


from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
post_players.loc[:,selected_columns] = scaler.fit_transform(post_players[selected_columns])


# In[9]:


post_players[selected_columns].head()


# In[10]:


post_players[selected_columns].describe()


# In[11]:


sfs.fit(post_players[selected_columns], post_players["Nxt_VII"])


# In[12]:


predictors = list(selected_columns[sfs.get_support()])


# In[13]:


print(predictors)


# In[14]:


def backtest(data, model, predictors, start=8, step=1):
    all_predictions = []
    
    years = sorted(data["season_start_yr"].unique())
    
    for i in range(start, len(years), step):
        current_year = years[i]
        train = data[data["season_start_yr"] < current_year]
        test = data[data["season_start_yr"] == current_year]
        
        model.fit(train[predictors], train["Nxt_VII"])
        
        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index)
        combined = pd.concat([test["Nxt_VII"], preds], axis=1)
        combined.columns = ["actual", "prediction"]
        
        all_predictions.append(combined)
    return pd.concat(all_predictions)


# In[15]:


predictions = backtest(post_players, rr, predictors)


# In[16]:


from sklearn.metrics import mean_squared_error

mean_error = mean_squared_error(predictions["actual"], predictions["prediction"])


# In[17]:


post_players["Nxt_VII"].describe()


# In[18]:


mean_error ** .5


# In[19]:


pd.Series(rr.coef_, index=predictors).sort_values()


# In[20]:


pd.Series(rr.intercept_)


# In[21]:


pd.Series(rr.n_features_in_)


# In[22]:


diff = predictions["actual"] - predictions["prediction"]


# In[23]:


merged = predictions.merge(post_players, left_index=True, right_index=True)


# In[24]:


merged["diff"] = (predictions["actual"] - predictions["prediction"]).abs()


# In[25]:


from sklearn.metrics import r2_score

rsquare = r2_score(predictions["actual"], predictions["prediction"])


# In[26]:


rsquare


# In[33]:


ncaapredictions = merged[["Player", "SR_Code", "Nxt_season", "Nxt_season_conf", "Season", "Position", "Conf", "Nxt_VII", "PER", "diff", "actual", "prediction", "HM MIN%", "AST Ratio HM", "TS% HM", "SR", "JR", "TOV per 30", "AST HM per 30", "OBPM", "TRB%", "DFL HM per 30", "AST TOV HM", "TRB HM per 30", "HM GP%", "TOV HM per 30", "BPM", "BOX HM", "PTS HM per 30"]].sort_values(["diff"])


# In[34]:


ncaapredictions


# In[35]:


import seaborn as sns
sns.boxplot(ncaapredictions['diff'])


# In[36]:


ncaapredictions.describe()


# In[37]:


ncaapredictions.to_csv('/Users/HasanAlanam/Documents/Hasan/ncaapredictions_dec13_17_2_features.csv', index=False)


# In[ ]:





# In[ ]:




