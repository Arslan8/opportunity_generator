import os 
import pandas as pd

from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings('ignore')

def get_index(string):
    """
    Helper function to extract the index from a line.
    get the index of the first alphabet in the string after the 9th index

    Args:
    line (str): Input line containing index information.

    Returns:
    int: Extracted index.
    """

    for i in range(9,len(string)):
        if string[i].isalpha():
            return i
    return -1

def extract_data():
    """
    Extracts data from .dat files in the OpportunityUCIDataset/dataset folder.

    Returns:
    pandas.DataFrame: Dataframe containing extracted data.
    """

    # Get all the .dat files in the dataset folder
    data_dir = 'OpportunityUCIDataset/dataset'
    files = os.listdir(data_dir)
    files = [f for f in files if f.endswith('.dat')]

    # Separate the ADL and Drill files
    list_of_files = [f for f in files if 'Drill' not in f]

    columns = []

    # Read column names from column_names.txt file
    with open(os.path.join(data_dir, "column_names.txt"), 'r') as f:
        lines = f.read().splitlines()

        for line in lines:
            if 'Column' in line:
                # Extract column names and append to the list
                columns.append(line[get_index(line):].split(";")[0])

    # Create an empty DataFrame with the extracted column names
    data_collection = pd.DataFrame(columns=columns)

    # Iterate over the list of files and concatenate data to the DataFrame
    for _, file in enumerate(list_of_files):
        proc_data = pd.read_table(os.path.join(data_dir, file), header=None, sep='\s+')
        proc_data.columns = columns
        data_collection = pd.concat([data_collection, proc_data])

    # Reset the DataFrame index
    data_collection.reset_index(drop=True, inplace=True)

    return data_collection


data_collection = extract_data()

from IPython import embed; embed()
