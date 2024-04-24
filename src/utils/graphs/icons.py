import plotly.graph_objects as go
import src.colors as c
from src.utils.constants import PERSONNALITY_INFO, DRUG_INFO
from dash import html

from src.utils.constants import AGE_CLASSES, GENDER_CLASSES, EDUCATION_CLASSES
import plotly.express as px
import src.utils.constants as constants

import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))
