'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import src.utils.constants as constants
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
                # df["sober"][personality] += dataframe[personality][i]
                df.at[personality, "sober"] += dataframe.at[i, personality]
        else:
            for drug in constants.DRUGS:
                if is_consumer(dataframe[drug][i]):
                    df_size[drug] += 1
                    for personality in constants.PERSONNALITY:
                        # df[drug][personality] += dataframe[personality][i]
                        df.at[personality, drug] += dataframe.at[i, personality]

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

def create_age_label(age: str):
    if age == "18-24":
        return '18-24', 'Plus de 24 ans'
    elif age == "65+":
        return '18-64', 'Plus de 64 ans'
    else:
        lower_bound, upper_bound = age.split('-')
        return f'18-{int(lower_bound) - 1}', age, f'Plus de {upper_bound} ans'

def create_age_dataframe(dataframe, selected_age):
    age_labels = create_age_label(selected_age)
    df = convert_scores(dataframe)

    selected_columns_dataframe = df.iloc[:, 11:27]
    drugs = selected_columns_dataframe.columns
    # Data pour construire le dataframe
    data_dict = {'drug': drugs}
    # Définir les couleurs pour chaque barre dans un cluster
    colors = []

    # BELOW
    if (selected_age != '18-24'):
        # Filtrer le DataFrame pour ne garder que les lignes correspondant aux âges inférieurs à l'âge sélectionné
        df_ages_below_selected = df[df['age'] < selected_age]
        # Calculer le nombre de personnes dans les tranches d'âge inférieures qui consomment chaque drogue
        ages_below_count = df_ages_below_selected[drugs].applymap(is_consumer).sum()
        # Calculer le nombre total de personne dans le groupe
        total_below_ages = len(df_ages_below_selected)
        # Calculer la portion de personnes dans les tranches inférieures d'âge qui consomment chaque drogue
        below_portion = ages_below_count / total_below_ages
        data_dict.update({age_labels[0]: below_portion})
        colors.append('lightgray')

    # SELECTED
    # Filtrer le DataFrame pour ne garder que les lignes correspondant à l'âge sélectionné
    df_selected_age = df[df['age'] == selected_age]
    # Calculer le nombre de personnes dans la tranche d'âge sélectionnée qui consomment chaque drogue
    selected_age_count = df_selected_age[drugs].applymap(is_consumer).sum()
    # Calculer le nombre total de personne dans le groupe
    total_selected_age = len(df_selected_age)
    # Calculer la portion de personnes dans la tranche d'âge sélectionnée qui consomment chaque drogue
    selected_age_portion = selected_age_count / total_selected_age
    selected_age_index = 0 if (selected_age == '18-24') else 1
    data_dict.update({age_labels[selected_age_index]: selected_age_portion})
    colors.append('#29b6f6')


    # ABOVE
    if (selected_age != '65+'):
        # Filtrer le DataFrame pour ne garder que les lignes correspondant aux âges supérieurs à l'âge sélectionné
        df_ages_above_selected = df[df['age'] > selected_age]
        # Calculer le nombre de personnes dans les tranches d'âge supérieures qui consomment chaque drogue
        ages_above_count = df_ages_above_selected[drugs].applymap(is_consumer).sum()
        # Calculer le nombre total de personne dans le groupe
        total_above_ages = len(df_ages_above_selected)
        # Calculer la portion de personnes dans les tranches supérieures d'âge qui consomment chaque drogue
        above_portion = ages_above_count / total_above_ages
        data_dict.update({age_labels[len(age_labels) - 1]: above_portion})
        colors.append('darkgray')
    
    result_df = pd.DataFrame(data_dict)

    french_drugs = []
    for key, value in constants.DRUG_INFO.items():
        french_drugs.append(value['french'])
        # print('key : ', key)

    result_df['drug'] = french_drugs

    return result_df, colors

def create_education_level_dataframe(df, education_dict):
    # Niveau d'étude sélectionné
    selected_education_level = education_dict.value['value']

    # Filtrer le DataFrame pour ne garder que les lignes correspondant au niveau d'éducation sélectionné
    df_selected_education_level = df[df['education'] == selected_education_level]

    selected_columns_dataframe = df.iloc[:, 11:27]
    drugs = selected_columns_dataframe.columns
    # Data pour construire le dataframe
    data_dict = {'drug': drugs}
    # Définir les couleurs pour chaque barre dans un cluster
    colors = []

    if selected_education_level != -2.43591:
        # Calculer le nombre de personnes avec les niveaux d'études inférieurs qui consomment chaque drogue
        df_below_education = df[df['education'] < selected_education_level]
        below_education_count = df_below_education[drugs].applymap(is_consumer).sum()
        # Calculer le nombre total de personne dans le groupe
        total_below_education = len(df_below_education)
        # Calculer la portion de personnes dans les niveaux d'étude inférieurs qui consomment chaque drogue
        below_portion = below_education_count / total_below_education
        data_dict.update({'Niveau d\'études inférieures': below_portion})
        colors.append('lightgray')

    # Calculer le nombre de personnes avec le niveau d'étude sélectionné qui consomment chaque drogue
    selected_education_level_count = df_selected_education_level[drugs].applymap(is_consumer).sum()
    # Calculer le nombre total de personne dans le groupe
    total_selected_age = len(df_selected_education_level)
    # Calculer la portion de personnes qui ont le niveau d'étude sélectionné qui consomment chaque drogue
    selected_age_portion = selected_education_level_count / total_selected_age
    data_dict.update({education_dict.value['text']: selected_age_portion})
    colors.append('#29b6f6')
    
    if selected_education_level != 1.98437:
        # Calculer le nombre de personnes avec les niveaux d'études supérieurs qui consomment chaque drogue
        df_above_education = df[df['education'] > selected_education_level]
        above_education_count = df_above_education[drugs].applymap(is_consumer).sum()
        # Calculer le nombre total de personne dans le groupe
        total_above_education = len(df_above_education)
        # Calculer la portion de personnes dans les niveaux d'étude supérieurs qui consomment chaque drogue
        above_portion = above_education_count / total_above_education
        data_dict.update({'Niveau d\'études supérieures': above_portion})
        colors.append('darkgrey')

    result_df = pd.DataFrame(data_dict)

    return result_df, colors


def get_most_common_profiles(df):
    """ Generate a DataFrame with the most common profiles of drug consumers. """
    # Drop unnecessary columns
    df = df.drop(columns=['nscore', 'escore', 'ascore', 'oscore', 'cscore', 'impulsive', 'ss'])

    # Apply mappings
    df['age'] = df['age'].map(constants.AGE_CLASSES)
    df['gender'] = df['gender'].map(constants.GENDER_CLASSES)
    df['education'] = df['education'].map(constants.EDUCATION_CLASSES)

    # Drug columns assumed to start from the 5th column onwards
    drug_columns = df.columns[4:]
    results = []

    # Loop through each drug column to filter and calculate modes
    for drug in drug_columns:
        # Apply the is_consumer function using vectorized approach
        filtered_df = df[df[drug].apply(is_consumer)][['age', 'gender', 'education', drug]]

        if not filtered_df.empty:
            # Calculate mode (most common value) for each demographic attribute
            most_common_values = filtered_df[['age', 'gender', 'education']].mode().iloc[0]
            results.append({
                'drug': drug,
                'most_common_age': most_common_values['age'],
                'most_common_gender': most_common_values['gender'],
                'most_common_education': most_common_values['education']
            })

    return pd.DataFrame(results)



def get_most_common_profiles_by_demographic(df):
    # Drop unnecessary columns
    df = df.drop(columns=['nscore', 'escore', 'ascore', 'oscore', 'cscore', 'impulsive', 'ss'])

    # Apply mappings
    df['age'] = df['age'].map(constants.AGE_CLASSES)
    df['gender'] = df['gender'].map(constants.GENDER_CLASSES)
    df['education'] = df['education'].map(constants.EDUCATION_CLASSES)

    # Drug columns assumed to start from the 5th column onwards
    drug_columns = df.columns[4:]
    results = []
    
    # print(df['education'].value_counts())
    # print((df[df["alcohol"].apply(is_consumer)])['education'].value_counts())

    for drug in drug_columns:
        # Total count per gender
        # gender_counts = df['gender'].value_counts()
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

        # # Consumer count per gender
        # consumer_gender_counts = consumer_df['gender'].value_counts()

        # # Calculate ratios
        # ratios = consumer_gender_counts / gender_counts

        # # Find the gender with the highest ratio
        # most_common_gender = ratios.idxmax()
        # most_common_ratio = ratios.max()

        # results.append({
        #     'drug': drug,
        #     'most_common_gender': most_common_gender,
        #     'ratio': most_common_ratio
        # })

    return pd.DataFrame(results)


# Tu prends les hommes si 45 % des hommes consommes et 51% consommes alors c'est les femmes qui l'emporte, 
# meme si c'est les hommes les plus represente.
# for each drug, count all consumers and non consumers 4000 6000 donc 40 % taux de consommation
#                   FEMMES taux de consommation. 
# For cannabis :
    # 18-24 Taux de consommation : combien de 18-24 sont consommateurs ? 18-24 consommateurs / 18-24 total
    # 24-35 Taux de consommation : combien de 24-35 sont consommateurs ? 24-35 consommateurs / 24-35 total
    ...

    # take the highest -> ratio for
# Do again for all drugs 