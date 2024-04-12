'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import utils.constants as constants
import src.conversions as conversions
import pandas as pd
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


def drop_columns(dataframe):
    return dataframe.drop(columns=['country', 'ethnicity', 'semer', 'caff', 'choc'])


def fix_errors(dataframe):
    return dataframe.rename(columns={'impuslive': 'impulsive'})


def convert_scores(dataframe):
    for conversion in conversions.CONVERSIONS:
        dataframe[conversion] = dataframe[conversion].map(
            conversions.CONVERSIONS[conversion])
    return dataframe


def is_consumer(cl):
    if cl == "CL0" or cl == "CL1" or cl == "CL2" or cl == "CL3":
        return False
    if cl == "CL4" or cl == "CL5" or cl == "CL6":
        return True
    return False


def is_sober(classes):
    for cl in classes:
        if cl == "CL2" or cl == "CL3" or cl == "CL4" or cl == "CL5" or cl == "CL6":
            return False
    return True


def personality_per_drug(dataframe):
    size = dataframe.id.count()

    columns = constants.DRUGS + ["sober"]
    df = pd.DataFrame(0, index=constants.PERSONNALITY, columns=columns)
    df_size = pd.DataFrame(0, index=["size"], columns=columns)

    for i in range(0, size):
        if is_sober(dataframe.loc[i]):
            df_size["sober"] += 1
            for personality in constants.PERSONNALITY:
                df["sober"][personality] += dataframe[personality][i]
        else:
            for drug in constants.DRUGS:
                if is_consumer(dataframe[drug][i]):
                    df_size[drug] += 1
                    for personality in constants.PERSONNALITY:
                        df[drug][personality] += dataframe[personality][i]

    for c in columns:
        for personality in constants.PERSONNALITY:
            df[c][personality] /= df_size[c]

    return df.transpose()

def consumption_per_drug(dataframe):
    count_df = pd.DataFrame(0, index=constants.DRUGS, columns=constants.CONSUMPTION_CLASSES)
    for i in dataframe.index:
        for drug in constants.DRUGS:
            consumption_class = dataframe[drug][i]
            count_df[consumption_class][drug] += 1

    order = []
    for drug in count_df.index:
        order.append((drug, count_df['CL0'][drug]))
    order.sort(key=lambda x: x[1], reverse=True)
    order = [x[0] for x in order]

    data = []
    size = dataframe.id.count()
    for drug in order:
        for consumption_class in constants.CONSUMPTION_CLASSES:
            percentage = count_df[consumption_class][drug] / size * 100
            data.append([drug, consumption_class, percentage])
    data.reverse()
    df = pd.DataFrame(data, columns=['drug', 'class', 'percentage'])

    return df

def drug_correlation(dataframe):
    size = dataframe.id.count()

    df = pd.DataFrame(0, index=constants.DRUGS, columns=constants.DRUGS)

    for i in range(0, size):
        finished_drugs = []
        for drug1 in constants.DRUGS:
            if is_consumer(dataframe[drug1][i]):
                for drug2 in constants.DRUGS:
                    if drug1 != drug2 and drug2 not in finished_drugs:
                        if is_consumer(dataframe[drug2][i]):
                            df[drug1][drug2] += 1
            finished_drugs.append(drug1)

    df = df.stack().reset_index()
    df.columns = ['source', 'target', 'weight']
    df['weight'] = df['weight'].astype(float) / df['weight'].sum() * 100
    df = df[df.weight != 0].reset_index(drop=True)

    return df


def generate_drogue_options(dataframe):
    """
    Generates a list of options for a dropdown selector, each representing a drug.

    Parameters:
    - dataframe: pandas.DataFrame - A DataFrame with columns for each drug.

    Returns:
    - options: list of dict - A list of dictionaries where each dictionary has 'label' and 'value' keys.
    """
    # List of drug columns, assuming the drug columns start from the 11th column in the DataFrame
    drug_columns = dataframe.columns[11:]

    # Generate dropdown options
    options = [{'label': drug.capitalize(), 'value': drug}
               for drug in drug_columns]

    # Check if there are any options to set a default value
    if options:
        default_value = options[0]['value']  # First drug's name
    else:
        default_value = None  # No default if the list is empty

    return options, default_value

def categorize_gender(value):
    return "Femme" if value < 0 else "Homme"

def b2b_barchart_sanitizing(dataframe):
    '''
        Creates the dataframe for the bar chart.

        Args:
            dataframe: The dataframe to use
    '''
    dataframe['gender_category'] = dataframe['gender'].apply(categorize_gender)
    drugs = ['alcohol', 'amphet', 'amyl', 'benzos', 'cannabis', 'coke', 'crack', 'ecstasy',
            'heroin', 'ketamine', 'legalh', 'lsd', 'meth', 'mushrooms', 'nicotine', 'vsa']
    for drug in drugs:
        dataframe[drug] = dataframe[drug].apply(is_consumer)

    # pick only the columns we need
    melted_df = pd.melt(dataframe, id_vars=['gender_category'], value_vars=[f'{drug}' for drug in drugs])

    # Group by gender and drug consumption variable, then count occurrences
    result_df = melted_df.groupby(['gender_category', 'variable'])['value'].sum().reset_index()

    # Rename the 'value' column to 'count'
    result_df.rename(columns={'value': 'count'}, inplace=True)

    return result_df

def gender_portion(dataframe):
    total_counts = dataframe.groupby('gender_category')['count'].transform('sum')
    # Calculating portion for each variable
    dataframe['percentage'] = ((100*dataframe['count']) / total_counts).round(1)
    dataframe = dataframe.pivot(index='variable', columns='gender_category', values='percentage').reset_index()
    return dataframe
    
def b2b_barchart(dataframe):
    '''
        Creates the horizontal back to back barchart.

        Args:
            dataframe: The dataframe to use to create the barchart

        Returns:
            The barchart figure
    '''
    dataframe = b2b_barchart_sanitizing(dataframe)
    dataframe = gender_portion(dataframe)
    return dataframe
