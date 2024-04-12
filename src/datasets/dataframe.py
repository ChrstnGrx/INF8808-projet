from ucimlrepo import fetch_ucirepo

from src.utils import preprocess
from src.utils.constants import EducationLevel

# fetch dataset
dataframe = fetch_ucirepo(id=373).data.original
dataframe = preprocess.drop_columns(dataframe)
dataframe = preprocess.fix_errors(dataframe)

personality_per_drug_df = preprocess.personality_per_drug(dataframe)

consumption_per_drug_df = preprocess.consumption_per_drug(dataframe)
b2bbarchart_df = preprocess.b2b_barchart(dataframe)

dataframe = preprocess.convert_scores(dataframe)
cluster_by_age_df, age_df_colors = preprocess.create_age_dataframe(dataframe, '18-24')
cluster_by_education_df, education_df_colors = preprocess.create_education_level_dataframe(dataframe, EducationLevel.UNIVERSITY_DEGREE)

