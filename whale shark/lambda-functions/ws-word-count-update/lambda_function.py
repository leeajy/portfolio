import pandas as pd
import awswrangler as wr
import os
from collections import Counter
import ast
from datetime import datetime

# global variables
bucket= 'whale-shark'
counter_path = f"s3://{bucket}/word-counts"

def drop_common_words(counter):
	blacklist = ['','and','i', None, 'to','do','the','a','so','u','a','on','is','you',
				'be','in','that', 'for', 'it', 'like', 'of', 'this', 'me', 'my', 'but',
				'was', 'have', 'with', 'not', 'be', 'he', 'no', 'lol', 'what', 'how',
				'are', 'if', 'yeah', 'wait', 'at', 'some', 'can', 'know', 'too', 'or',
				'about', 'we', 'its', 'your', 'out', 'they', 'she', 'im', 'her', 'tho',
				'thats']
	for key in blacklist:
		counter.pop(key,'-1')
	return counter

def transform_to_counter(df):
	df['content'] = df['content'].transform(lambda x: str(x).lower())
	df['words'] = df['content'].str.split(' ', expand=False)
	df = df[["author","words"]].groupby('author').agg(['sum'])
	df.columns = ['Word List']
	df["Counter"] = df["Word List"].transform(lambda x: Counter(x))
	df["Counter"] = df["Counter"].transform(lambda x: drop_common_words(x))
	df = df.drop('Word List', axis=1)
	df = df.reset_index()
	return df
	
def update_counters(df):
	try:
		df2 = wr.s3.read_csv(path=counter_path)
		df2["Counter"] = df2["Counter"].transform(lambda x: Counter(ast.literal_eval(x)))
		df2 = pd.concat([df, df2]).groupby(['author']).sum()
		df2 = df2.reset_index()
		return df2
	except Exception as e:
		# if there is no existing counter, return the current df.
		return df

def lambda_handler(event, context):
	key = "events-v2/" + datetime.utcnow().strftime("%Y-%m-%d")
	df = wr.s3.read_csv(path=f's3://{bucket}/{key}')
	df = transform_to_counter(df)
	df = update_counters(df)
	df["Counter"] = df["Counter"].transform(lambda x: dict(x))
	wr.s3.to_csv(df, counter_path, index=False, mode="overwrite", dataset=True)
