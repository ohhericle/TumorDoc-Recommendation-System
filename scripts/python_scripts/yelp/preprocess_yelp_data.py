import os
import boto3
import subprocess
import pandas as pd
from smart_open import smart_open

def extract_and_split():

    '''
    Routine to execute extract_yelp_data.sh, splitter.sh, and runner.sh
    
    inputs:
        None
    
    outputs:
        yelp_bid.csv
        yelp_business_ids
        yelp_bid_name.csv
        yelp_business_ids_dir
    '''

    # Extract the yelp data to make yelp_contains_doctor.json and yelp_bid.csv
    subprocess.run(['./bash_scripts/extract_yelp_data.sh'])

    # Run splitter to create the yelp_business_ids_dir
    subprocess.run(['./bash_scripts/splitter.sh'])

    # Execute runner.sh to get the business names.
    print('Fetching Business Names From Yelp. May take a while......')
    subprocess.run(['./bash_scripts/runner.sh'])


def combine_bid_rev(yelp_bid, yelp_review_text):

    '''
    Combine all the various data joining into one function

    inputs
        yelp_bid.csv (input 1)
        yelp_review_text.txt (input 2)
    '''

    output_frame = pd.DataFrame()
    data = []
    
    ids = pd.read_csv(yelp_bid)
    with smart_open(yelp_review_text) as f:
    
        for line in f:
            data.append(line)
    
    for i in data:
        print(len(i))
    
    output_frame['business_id'] = ids['business_id']
    output_frame['review'] = data
    
    output_frame.to_csv(
        's3://trecs-data-s3/data/clean_data/yelp_bid_reviews.csv', index=False
    )

if __name__ == '__main__':

    yelp_bid = 's3://trecs-data-s3/data/processed_raw_data/yelp_bid.csv'
    yelp_review_text = 's3://trecs-data-s3/data/processed_raw_data/yelp_review_text.txt'

    extract_and_split()
    combine_bid_rev(yelp_bid, yelp_review_text)