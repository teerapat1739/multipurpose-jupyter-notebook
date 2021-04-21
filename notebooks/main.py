import pandas as pd, numpy as np
import warnings
warnings.filterwarnings("ignore")

import seaborn as sns

#import the plotting libraries
import matplotlib.pyplot as plt
%matplotlib inline

df_rounds2 = pd.read_csv("private_data/rounds2.csv",encoding='ISO-8859-1')
df_companies = pd.read_csv("private_data/companies.csv",encoding='ISO-8859-1')

df_rounds2['company_permalink'] = df_rounds2['company_permalink'].str.lower()
df_companies['permalink'] = df_companies['permalink'].str.lower()

# Checkpoint 1: Data Cleaning 1

# How many unique companies are present in rounds2?
print(len(df_rounds2['company_permalink'].unique()))

# How many unique companies are present in companies?
print(len(df_companies["permalink"].unique()))


""" 
In the companies data frame, which column can be used as the unique key for each company? Write the name of the column
 - company_permalink for rounds2.csv
 - permalink for companies.csv
"""



"""
Are there any companies in the rounds2 file which are not present in companies? Answer yes or no: Y/N
 - No
"""


# Merge the two data frames so that all variables (columns) in the companies frame are added to the rounds2 data frame. Name the merged frame master_frame. How many observations are present in master_frame?
print(len(master_frame.index))

# Checkpoint 2: Funding Type Analysis


df_funding_type_venture = df_rounds2[df_rounds2['funding_round_type'] == 'venture']
df_funding_type_seed = df_rounds2[df_rounds2['funding_round_type'] == 'seed']
df_funding_type_angel = df_rounds2[df_rounds2['funding_round_type'] == 'angel']
df_funding_type_private_equity = df_rounds2[df_rounds2['funding_round_type'] == 'private_equity']


df_funding_type_venture["raised_amount_usd_million"] = df_funding_type_venture["raised_amount_usd"]/1000000
df_funding_type_seed["raised_amount_usd_million"] = df_funding_type_seed["raised_amount_usd"]/1000000
df_funding_type_angel["raised_amount_usd_million"] = df_funding_type_angel["raised_amount_usd"]/1000000
df_funding_type_private_equity["raised_amount_usd_million"] = df_funding_type_private_equity["raised_amount_usd"]/1000000


# describe amount funding_type_venture
df_funding_type_venture['raised_amount_usd_million'].describe() 
# 17,600,000,000

# describe amount df_funding_type_seed
df_funding_type_seed['raised_amount_usd_million'].describe()
# 200,000,000

# describe amount df_funding_type_angel
df_funding_type_angel['raised_amount_usd_million'].describe()
# 494,511,992

# describe amount df_funding_type_private_equity
df_funding_type_private_equity['raised_amount_usd_million'].describe()
# 4,745,460,219


"""
Considering that Spark Funds wants to invest between 5 to 15 million USD per investment round with mean each funding type

which investment type is the most suitable for it?

The answer is venture.
"""


# Checkpoint 3: Country Analysis

df_funding_type_venture = pd.merge(df_funding_type_venture, df_companies, how = 'left', left_on = 'company_permalink', right_on = 'permalink')

df_funding_type_venture[df_funding_type_venture["permalink"].isnull() == True]

df_funding_type_venture = df_funding_type_venture[df_funding_type_venture["permalink"].isnull() != True]

# Spark Funds wants to see the top nine countries which have received the highest total funding (across ALL sectors for the chosen investment type)
df_funding_type_venture['country_code'].unique()

df_groupby_country_code = df_funding_type_venture[['country_code', 'raised_amount_usd_million']].groupby(['country_code']).sum()

df_groupby_country_code = df_groupby_country_code.reset_index()
df_top9 = df_groupby_country_code.head(9)

print(df_top9)

"""
Analysing the Top 3 English-Speaking Countries
Top English-speaking country is United States of America (USA)
Second English-speaking country is United Kingdom (GBR)
Third English-speaking country is India (IND)
"""


# Checkpoint 4: Sector Analysis 1

df_mapping = pd.read_csv("private_data/mapping.csv")

df_funding_type_venture["category_list"] = df_funding_type_venture["category_list"].apply(lambda x: str(x).split('|')[0])


def handle_nan(val):
    if val == "nan":
        return np.nan
    else:
        return val
df_funding_type_venture["category_list"] = df_funding_type_venture["category_list"].apply(lambda x: handle_nan(x))
print(df_funding_type_venture)

df_mapping_for_find_main_sector = df_mapping.iloc[ : , 1: ]
print(df_mapping_for_find_main_sector)

df_mapping_for_find_main_sector["main sector"] = df_mapping_for_find_main_sector.idxmax(axis=1)

df_mapping["main sector"] = df_mapping_for_find_main_sector["main sector"]

df_mapping = df_mapping[['category_list','main sector']]

df_funding_type_venture = pd.merge(df_funding_type_venture, df_mapping, how = 'left', left_on='category_list', right_on='category_list')

"""
Expected Results: Code for a merged data frame with each primary sector mapped to its main sector (the primary sector should be present in a separate column)
"""

print(df_funding_type_venture)


# Checkpoint 5: Sector Analysis 2

df_funding_type_venture = df_funding_type_venture[(df_funding_type_venture["raised_amount_usd_million"] >= 5) & (df_funding_type_venture["raised_amount_usd_million"] <=15 )]

df_funding_type_venture = df_funding_type_venture[
    (df_funding_type_venture["country_code"] == "IND")
    | (df_funding_type_venture["country_code"] == "USA")
    |(df_funding_type_venture["country_code"] == "GBR")]

 df_funding_type_venture["country_code"].value_counts()   

print(round(df_funding_type_venture[df_funding_type_venture["country_code"] == "USA"]["raised_amount_usd_million"].sum(),2))
print(round(df_funding_type_venture[df_funding_type_venture["country_code"] == "GBR"]["raised_amount_usd_million"].sum(),2))
print(round(df_funding_type_venture[df_funding_type_venture["country_code"] == "IND"]["raised_amount_usd_million"].sum(),2))
 """
 total number of investments¶
    1. USA = 36139
    2. GBR = 2055
    3. IND = 824
 """


df_funding_type_venture_eng_contry = df_funding_type_venture
df_funding_type_venture_eng_contry


top_sector_usa = df_funding_type_venture[df_funding_type_venture["country_code"] == "USA"]["category_list"].value_counts()
print(top_sector_usa)

top_sector_gbr = df_funding_type_venture[df_funding_type_venture["country_code"] == "GBR"]["category_list"].value_counts()
print(top_sector_gbr)

top_sector_ind = df_funding_type_venture[df_funding_type_venture["country_code"] == "IND"]["category_list"].value_counts()
print(top_sector_ind)

"""
Top sector (based on count of investments) 
    1. USA = Biotechnology(1477)
    2. GBR = Biotechnology(70)
    3. IND = E-Commerce(37)


Second-best sector (based on count of investments) ¶
    1. USA = Software(1044)
    2. GBR = Software(45)
    3. IND = Software(19)

Third-best sector (based on count of investments) 
    1. USA = Advertising(691)
    2. GBR = Advertising(35)
    3. IND = Finance(15)
"""


df_top_sector_usa = df_funding_type_venture[(df_funding_type_venture["country_code"] == "USA") & (df_funding_type_venture["category_list"] == "Biotechnology")][["name","raised_amount_usd_million"]]
df_top_sector_usa = df_top_sector_usa.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_top_sector_usa.head())


df_top_sector_gbr = df_funding_type_venture[(df_funding_type_venture["country_code"] == "GBR") & (df_funding_type_venture["category_list"] == "Biotechnology")][["name","raised_amount_usd_million"]]
df_top_sector_gbr = df_top_sector_gbr.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_top_sector_gbr.head())

df_top_sector_ind = df_funding_type_venture[(df_funding_type_venture["country_code"] == "IND") & (df_funding_type_venture["category_list"] == "E-Commerce")][["name","raised_amount_usd_million"]]
df_top_sector_ind = df_top_sector_ind.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_top_sector_ind.head())


"""
For the top sector count-wise , which company received the highest investment? 
    1. USA = Biotechnology(Arno Therapeutics company)
    2. GBR = Biotechnology(Onyvax company)
    3. IND = E-Commerce(Voylla Retail Pvt. Ltd)
"""

df_second_sector_usa = df_funding_type_venture[(df_funding_type_venture["country_code"] == "USA") & (df_funding_type_venture["category_list"] == "Software")][["name","raised_amount_usd_million"]]
df_second_sector_usa= df_second_sector_usa.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_second_sector_usa.head())

df_second_sector_gbr = df_funding_type_venture[(df_funding_type_venture["country_code"] == "GBR") & (df_funding_type_venture["category_list"] == "Software")][["name","raised_amount_usd_million"]]
df_second_sector_gbr = df_second_sector_gbr.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_second_sector_gbr.head())

df_second_sector_ind = df_funding_type_venture[(df_funding_type_venture["country_code"] == "IND") & (df_funding_type_venture["category_list"] == "Software")][["name","raised_amount_usd_million"]]
df_second_sector_ind = df_second_sector_ind.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_second_sector_ind.head())

"""
For the second-best sector count-wise, which company received the highest investment? 
    1. USA = Software(BTI Systems)
    2. GBR = Software(EnvironmentIQ)
    3. IND = Software(EximSoft-Trianz)
"""


df_third_sector_usa = df_funding_type_venture[(df_funding_type_venture["country_code"] == "USA") & (df_funding_type_venture["category_list"] == "Advertising")][["name","raised_amount_usd_million"]]
df_third_sector_usa= df_third_sector_usa.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_third_sector_usa.head())

df_third_sector_gbr = df_funding_type_venture[(df_funding_type_venture["country_code"] == "GBR") & (df_funding_type_venture["category_list"] == "Advertising")][["name","raised_amount_usd_million"]]
df_third_sector_gbr = df_third_sector_gbr.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_third_sector_gbr.head())

df_third_sector_ind = df_funding_type_venture[(df_funding_type_venture["country_code"] == "IND") & (df_funding_type_venture["category_list"] == "Finance")][["name","raised_amount_usd_million"]]
df_third_sector_ind = df_third_sector_ind.sort_values(by=['raised_amount_usd_million'], ascending=False)
print(df_third_sector_ind.head())

"""
For the third-best sector count-wise, which company received the highest investment? ¶
    1. USA = Advertising(AdRoll)
    2. GBR = Advertising(SimilarWeb)
    3. IND = Finance(Financial Information Network & Operations Pvt)
"""


FT  = df_rounds2['funding_round_type'].value_counts(sort=True).nlargest(5)
plt.figure(figsize=(10,5))
sns.barplot(FT.index, FT.values, alpha=0.8)
plt.title('Representative amount in top 5 funding type in the World')
plt.ylabel('Number of funding types', fontsize=12)
plt.xlabel('funding types', fontsize=12)
plt.show()


# A plot showing the top 9 countries against the total amount of investments of funding type FT. This should make the top 3 countries (Country 1, Country 2, and Country 3) very clear.

plot_top9 = df_top9.set_index("country_code")
plot_top9.plot.bar()
df_top9


sum_raised_amount_usd_million = round(df_groupby_country_code["raised_amount_usd_million"].sum() ,2)
print(sum_raised_amount_usd_million)


plt.figure(figsize=(10,5))
sns.barplot(data=df_top9, x="country_code", y="raised_amount_usd_million")
plt.show()

data_top3 = [["Biotechnology+E-Commerce",13406.3, 636.959, 343.87], ["Software", 9125.72, 383.817, 163.05], ["Biotechnology+E-Commerce",13406.3, 636.959,126.006]]
df_top3 = pd.DataFrame(data_top3, columns = ['SECTOR','USA', 'GBR', 'IND'])
df_top3

df_top3 = df_top3.set_index("SECTOR")
df_top3.plot.bar(logy=True)

df_top3.plot.bar(logy=True)

