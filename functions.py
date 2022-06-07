import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


###### helper functions. Use them when needed #######
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]
##################################################

##Step 1: Read CSV File
df = pd.read_csv("movie_dataset.csv")
#print df.columns
##Step 2: Select Features

features = ['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print("Error:", row	)

df["combined_features"] = df.apply(combine_features,axis=1)

# def suggest():
# 	return

##Step 4: Create count matrix from this new combined column
# cv = CountVectorizer()

# count_matrix = cv.fit_transform(df["combined_features"])

# ##Step 5: Compute the Cosine Similarity based on the count_matrix
# cosine_sim = cosine_similarity(count_matrix)