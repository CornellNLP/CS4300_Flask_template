import pandas as pd
  
# reading two csv files
data1 = pd.read_csv('datasets/All_Streaming_Shows.csv')
data2 = pd.read_csv('datasets/tv_shows.csv')
  
# using merge function by setting how='inner'
output = pd.merge(data1, data2, 
                   on='Title', 
                   how='left')

# remove columns
output = output.loc[:, ~output.columns.duplicated()]
output = output.drop(columns=['ID', 'Netflix',	'Hulu', 'Prime Video', 'Disney+', 'type', 'Year_y', 'Content Rating_y'])

# displaying result
print(output)

#output into file
output.to_csv('final_data.csv')
