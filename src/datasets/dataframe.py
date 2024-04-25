from ucimlrepo import fetch_ucirepo

from src.utils import preprocess
from src.utils.constants import EducationLevel

def fetch_and_prepare_data(dataset_id):
    """
    Retrieves and preprocesses a dataset from the UC Irvine Machine Learning Repository.
    This specific dataset, identified by ID 373, concerns drug consumption.
    It is publicly available at https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified

    Args:
    dataset_id (int): The identifier of the dataset to retrieve.

    Returns:
    DataFrame: The preprocessed dataset.
    """
    # Fetching data from the UCI repository using a specified ID
    dataframe = fetch_ucirepo(id=dataset_id).data.original
    # Removing unnecessary columns and control drugs ('country', 'ethnicity', 'semer', 'caff', 'choc')
    dataframe = preprocess.drop_columns(dataframe)
    # Correcting typos in column names
    dataframe = preprocess.fix_errors(dataframe)
    return dataframe

dataframe = fetch_and_prepare_data(373)

# -------------------
# First Page: Drug Analysis
# -------------------
# Preprocessing for drug-related visualizations
profiles_df = preprocess.get_most_common_profiles_by_demographic(dataframe.copy())
personality_per_drug_df = preprocess.personality_per_drug(dataframe.copy())
consumption_per_drug_df = preprocess.consumption_per_drug(dataframe.copy())
drug_corr_df = preprocess.drug_correlation(dataframe.copy())

# -------------------
# Second Page: Demographic Analysis
# -------------------
# Transforming data for demographic-related visualizations
transformed_df = preprocess.convert_scores(dataframe.copy())
b2bbarchart_df = preprocess.b2b_barchart(transformed_df.copy())

# Grouping data by age and education level
cluster_by_age_df, age_df_colors = preprocess.create_age_dataframe(transformed_df.copy(), '18-24')
cluster_by_education_df, education_df_colors = preprocess.create_education_level_dataframe(transformed_df.copy(), EducationLevel.UNIVERSITY_DEGREE)
