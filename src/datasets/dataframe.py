from ucimlrepo import fetch_ucirepo

from utils import preprocess

# fetch dataset
dataframe = fetch_ucirepo(id=373).data.original
dataframe = preprocess.drop_columns(dataframe)
dataframe = preprocess.fix_errors(dataframe)

personality_per_drug_df = preprocess.personality_per_drug(dataframe)
