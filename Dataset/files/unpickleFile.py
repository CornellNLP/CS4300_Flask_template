import os
import pickle

dataset = pickle.load(open('ingr_map.pkl', 'rb')) # Reads .pkl file

dataset = dataset.sort_values(by='id') # Sorts by id

relevant_dataset = dataset[['processed', 'id']] # Selects relevant columns

relevant_dataset.drop_duplicates(inplace=True) # Removes duplicates

relevant_dataset.to_csv('ingr_map.csv') # Saves result to .csv  file