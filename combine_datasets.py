import pandas as pd
  
data1 = pd.read_csv('datasets/All_Streaming_Shows.csv')
data2 = pd.read_csv('datasets/tv_shows.csv')
  
output = pd.merge(data1, data2, 
                   on='Title', 
                   how='left')

# remove and rename columns
output = output.loc[:, ~output.columns.duplicated()]
output = output.drop(columns=['ID', 'Netflix',	'Hulu', 'Prime Video', 'Disney+', 'type', 'Year_y', 'Content Rating_y'])
output = output.rename(columns={"Year_x": "Year", "Content Rating_x": "Content Rating"})

output.to_csv('kaggle_data.csv')
