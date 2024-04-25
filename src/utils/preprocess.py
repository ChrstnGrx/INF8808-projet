'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import src.utils.constants as constants
import src.utils.conversions as conversions
import pandas as pd
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


def drop_columns(dataframe):
    # Remove unnecessary columns from the dataframe
    return dataframe.drop(columns=['country', 'ethnicity', 'semer', 'caff', 'choc'])

def fix_errors(dataframe):
    # Correct the spelling of a column name
    return dataframe.rename(columns={'impuslive': 'impulsive'})

def convert_scores(dataframe):
    # Retrive correct values for NEO-scores, by mapping each encoded value to it's real value.
    for conversion in conversions.CONVERSIONS:
        dataframe[conversion] = dataframe[conversion].map(conversions.CONVERSIONS[conversion])
    return dataframe

def is_consumer(cl):
    # Determine if the classification is that of a consumer based on the consumption class
    return cl in {"CL4", "CL5", "CL6"}

def is_sober(classes):
    # Check sobriety (Not a regular consumer)
    return not any(cl in {"CL2", "CL3", "CL4", "CL5", "CL6"} for cl in classes)

def create_age_labels(age: str):
    if age == "18-24":
        return '18-24', 'Plus de 24 ans'
    elif age == "65+":
        return '18-64', 'Plus de 64 ans'
    else:
        lower_bound, upper_bound = age.split('-')
        return f'18-{int(lower_bound) - 1}', age, f'Plus de {upper_bound} ans'


def personality_per_drug(dataframe):
    """
    Calculates and returns a DataFrame containing normalized personality metrics (e.g., escore, nscore)
    for each drug and for sober individuals. Each column represents a drug or sober status, and each row
    represents a personality trait metric.

    Parameters:
    dataframe (DataFrame): The source DataFrame with drug consumption data and personality metrics.

    Returns:
    DataFrame: A transposed DataFrame with drugs and sober as columns, and personality traits as rows,
               where values are normalized averages per consumption status.
    """
    # Generates a dataframe with average personality metrics (like escore, nscore, etc.)
    # for each drug and for sober individuals. Metrics are normalized per consumption status.
    size = dataframe.id.count()
    columns = constants.DRUGS + ["sober"]
    df = pd.DataFrame(0, index=constants.PERSONNALITY, columns=columns)
    df_size = pd.DataFrame(0, index=["size"], columns=columns)

    # Accumulate personality scores based on drug consumption    
    for i in range(0, size):
        if is_sober(dataframe.loc[i]):
            df_size["sober"] += 1
            for personality in constants.PERSONNALITY:
                df.at[personality, "sober"] += dataframe.at[i, personality]
        else:
            for drug in constants.DRUGS:
                if is_consumer(dataframe[drug][i]):
                    df_size[drug] += 1
                    for personality in constants.PERSONNALITY:
                        df.at[personality, drug] += dataframe.at[i, personality]

    # Normalize personality scores by the number of entries for each drug or sober status
    for c in columns:
        for personality in constants.PERSONNALITY:
            df[c][personality] /= df_size[c]

    return df.transpose()

def consumption_per_drug(dataframe):
    """
    Generates a DataFrame listing the percentage of users in each consumption class
    for each drug. Drugs are sorted by the count of non-users descending, and consumption classes
    are ordered from recently used (CL6) to never (CL0).

    Parameters:
    dataframe (DataFrame): The source DataFrame with drug consumption data.

    Returns:
    DataFrame: A DataFrame where each row contains a drug, consumption class, and the percentage
               of users in that class, sorted from most recent usage to least.
    """
    # Calculate and return the percentage of individuals in each consumption class
    # for every drug, sorted by usage from recent to old (CL6 to CL0).
    count_df = pd.DataFrame(0, index=constants.DRUGS, columns=constants.CONSUMPTION_CLASSES)

    # Accumulate counts for each consumption class per drug
    for i in dataframe.index:
        for drug in constants.DRUGS:
            consumption_class = dataframe[drug][i]
            count_df[consumption_class][drug] += 1

    # Calculate percentages and sort drugs by the count of non-users descending
    order = sorted([(drug, count_df.loc[drug, 'CL0']) for drug in count_df.index], key=lambda x: x[1], reverse=True)
    order = [x[0] for x in order]

    # Calculate percentages and prepare data for output
    data = []
    size = dataframe.id.count()
    for drug in order:
        for consumption_class in constants.CONSUMPTION_CLASSES:
            percentage = count_df[consumption_class][drug] / size * 100
            data.append([drug, consumption_class, percentage])

    # Reverse the list to start from most recent usage
    data.reverse()
    df = pd.DataFrame(data, columns=['drug', 'class', 'percentage'])

    return df

def drug_correlation(dataframe):
    """
    Computes co-consumption relationships between drugs as percentage weights.

    Parameters:
    dataframe (DataFrame): Input data with drug consumption records.

    Returns:
    DataFrame: Co-consumption weights between drug pairs.
    """
    # Calculate and return the percentage weight of co-consumption relationships between different drugs.
    size = dataframe.id.count()
    df = pd.DataFrame(0, index=constants.DRUGS, columns=constants.DRUGS)

    # Collect co-consumption data for all pairings of drugs
    for i in range(size):
        finished_drugs = []
        for drug1 in constants.DRUGS:
            if is_consumer(dataframe[drug1][i]):
                for drug2 in constants.DRUGS:
                    if drug1 != drug2 and drug2 not in finished_drugs:
                        if is_consumer(dataframe[drug2][i]):
                            df[drug1][drug2] += 1
                finished_drugs.append(drug1)

    # Convert raw counts to percentages and format for output
    df = df.stack().reset_index()
    df.columns = ['source', 'target', 'weight']
    df = df[df.weight != 0].reset_index(drop=True)
    df['weight'] = df['weight'].astype(float) / df['weight'].sum() * 100

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

def b2b_barchart_sanitizing(dataframe):
    '''
        Creates the dataframe for the bar chart.

        Args:
            dataframe: The dataframe to use
    '''
    for key, value in constants.DRUG_INFO.items():
        dataframe[value['french']] = dataframe[key].apply(is_consumer)

    # pick only the columns we need
    melted_df = pd.melt(dataframe, id_vars=['gender'], value_vars=[f"{value['french']}" for (key, value) in constants.DRUG_INFO.items()])

    # Group by gender and drug consumption variable, then count occurrences
    result_df = melted_df.groupby(['gender', 'variable'])['value'].sum().reset_index()

    # Rename the 'value' column to 'count'
    result_df.rename(columns={'value': 'count'}, inplace=True)

    return result_df

def gender_portion(dataframe):
    total_counts = dataframe.groupby('gender')['count'].transform('sum')

    # Calculating portion for each variable
    dataframe['percentage'] = ((100*dataframe['count']) / total_counts).round(1)
    dataframe = dataframe.pivot(index='variable', columns='gender', values='percentage').reset_index()
    
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

def create_age_dataframe(dataframe, selected_age):
    age_labels = create_age_labels(selected_age)
    df = convert_scores(dataframe)
    selected_columns_dataframe = df.iloc[:, 11:27]
    drugs = selected_columns_dataframe.columns
    
    # Data to construct the dataframe
    data_dict = {'drug': drugs}
    
    # Define colors for each bar in a cluster
    colors = []
    # BELOW
    if (selected_age != '18-24'):
        # Filter the DataFrame to keep only rows corresponding to ages below the selected age
        df_ages_below_selected = df[df['age'] < selected_age]
        
        # Calculate the number of people in the lower age ranges who consume each drug
        ages_below_count = df_ages_below_selected[drugs].applymap(is_consumer).sum()
        
        # Calculate the total number of people in the group
        total_below_ages = len(df_ages_below_selected)
        
        # Calculate the portion of people in the lower age ranges who consume each drug
        below_portion = ages_below_count / total_below_ages
        data_dict.update({age_labels[0]: below_portion})
        colors.append('lightgray')

    # SELECTED
    # Filter the DataFrame to keep only rows corresponding to the selected age
    df_selected_age = df[df['age'] == selected_age]
    
    # Calculate the number of people in the selected age range who consume each drug
    selected_age_count = df_selected_age[drugs].applymap(is_consumer).sum()
    
    # Calculate the total number of people in the group
    total_selected_age = len(df_selected_age)
    
    # Calculate the portion of people in the selected age range who consume each drug
    selected_age_portion = selected_age_count / total_selected_age
    selected_age_index = 0 if (selected_age == '18-24') else 1
    data_dict.update({age_labels[selected_age_index]: selected_age_portion})
    colors.append('#29b6f6')


    # ABOVE
    if (selected_age != '65+'):
        # Filter the DataFrame to keep only rows corresponding to ages above the selected age
        df_ages_above_selected = df[df['age'] > selected_age]
        
        # Calculate the number of people in the upper age ranges who consume each drug
        ages_above_count = df_ages_above_selected[drugs].applymap(is_consumer).sum()
        
        # Calculate the total number of people in the group
        total_above_ages = len(df_ages_above_selected)
        
        # Calculate the portion of people in the upper age ranges who consume each drug
        above_portion = ages_above_count / total_above_ages
        data_dict.update({age_labels[len(age_labels) - 1]: above_portion})
        colors.append('darkgray')
    
    result_df = pd.DataFrame(data_dict)
    result_df['drug'] = result_df['drug'].map(lambda x: constants.DRUG_INFO[x]['french'])
    return result_df, colors

def create_education_level_dataframe(df, education_dict):
    # Selected education level
    selected_education_level = education_dict.value['value']

    # Filter the DataFrame to keep only rows corresponding to the selected education level
    df_selected_education_level = df[df['education'] == selected_education_level]
    selected_columns_dataframe = df.iloc[:, 11:27]
    drugs = selected_columns_dataframe.columns
    
    # Data to construct the dataframe
    data_dict = {'drug': drugs}

    # Define colors for each bar in a cluster
    colors = []
    if selected_education_level != -2.43591:
        # Calculate the number of people with lower education levels who consume each drug
        df_below_education = df[df['education'] < selected_education_level]
        below_education_count = df_below_education[drugs].applymap(is_consumer).sum()
        
        # Calculate the total number of people in the group
        total_below_education = len(df_below_education)
        
        # Calculate the portion of people with lower education levels who consume each drug
        below_portion = below_education_count / total_below_education
        data_dict.update({'Niveau d\'études inférieures': below_portion})
        colors.append('lightgray')

    # Calculate the number of people with the selected education level who consume each drug
    selected_education_level_count = df_selected_education_level[drugs].applymap(is_consumer).sum()
    
    # Calculate the total number of people in the group
    total_selected_age = len(df_selected_education_level)
    
    # Calculate the portion of people with the selected education level who consume each drug
    selected_age_portion = selected_education_level_count / total_selected_age
    data_dict.update({education_dict.value['text']: selected_age_portion})
    colors.append('#29b6f6')
    
    if selected_education_level != 1.98437:
        # Calculate the number of people with higher education levels who consume each drug
        df_above_education = df[df['education'] > selected_education_level]
        above_education_count = df_above_education[drugs].applymap(is_consumer).sum()
        
        # Calculate the total number of people in the group
        total_above_education = len(df_above_education)
        
        # Calculate the portion of people with higher education levels who consume each drug
        above_portion = above_education_count / total_above_education
        data_dict.update({'Niveau d\'études supérieures': above_portion})
        colors.append('darkgrey')

    result_df = pd.DataFrame(data_dict)
    result_df['drug'] = result_df['drug'].map(lambda x: constants.DRUG_INFO[x]['french'])
    return result_df, colors

def get_most_common_profiles_by_demographic(df):
    """
    Computes the most common demographic profiles and their prevalence ratios for drug consumers.

    Parameters:
    df (DataFrame): Input data with demographic details and drug consumption status.

    Returns:
    DataFrame: Contains the most prevalent demographic category and its ratio for each drug.
    """
    # Drop unnecessary columns
    df = df.drop(columns=['nscore', 'escore', 'ascore', 'oscore', 'cscore', 'impulsive', 'ss'])

    # Apply mappings
    df['age'] = df['age'].map(constants.AGE_CLASSES)
    df['gender'] = df['gender'].map(constants.GENDER_CLASSES)
    df['education'] = df['education'].map(constants.EDUCATION_CLASSES)

    # Drug columns start from the 5th column onwards 
    drug_columns = df.columns[4:]
    results = []

    for drug in drug_columns:
        # Total count per gender
        total_counts = {
            'gender': df['gender'].value_counts(),
            'education': df['education'].value_counts(),
            'age': df['age'].value_counts()
        }
        
        # Filter to consumers only
        consumer_df = df[df[drug].apply(is_consumer)]
        
        consumer_counts = {
            'gender': consumer_df['gender'].value_counts(),
            'education': consumer_df['education'].value_counts(),
            'age': consumer_df['age'].value_counts()
        }
        drug_results = {'drug': drug}

        for category in ['gender', 'education', 'age']:
            if not consumer_counts[category].empty:
                ratios = consumer_counts[category] / total_counts[category]
                most_common_category = ratios.idxmax()
                most_common_ratio = ratios.max()
            else:
                most_common_category = 'Not Available'
                most_common_ratio = 0
            
            drug_results[f'most_common_{category}'] = most_common_category
            drug_results[f'{category}_ratio'] = most_common_ratio
        results.append(drug_results)
    return pd.DataFrame(results)