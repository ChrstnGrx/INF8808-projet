NEUTRAL_0 = '#f5f5f5'
NEUTRAL_1 = '#e0e0e0'
NEUTRAL_2 = '#bdbdbd'
NEUTRAL_3 = '#9e9e9e'
NEUTRAL_4 = '#757575'
NEUTRAL_5 = '#616161'
NEUTRAL_6 = '#424242'

GROUP1_0 = '#fbe9e7'
GROUP1_1 = '#ffccbc'
GROUP1_2 = '#ffab91'
GROUP1_3 = '#ff7043'
GROUP1_4 = '#f4511e'
GROUP1_5 = '#d84315'
GROUP1_6 = '#bf360c'

GROUP2_0 = '#f3e5f5'
GROUP2_1 = '#e1bee7'
GROUP2_2 = '#ce93d8'
GROUP2_3 = '#ab47bc'
GROUP2_4 = '#8e24aa'
GROUP2_5 = '#6a1b9a'
GROUP2_6 = '#4a148c'

GROUP3_0 = '#f1f8e9'
GROUP3_1 = '#dcedc8'
GROUP3_2 = '#c5e1a5'
GROUP3_3 = '#9ccc65'
GROUP3_4 = '#7cb342'
GROUP3_5 = '#558b2f'
GROUP3_6 = '#33691e'

GROUP4_0 = '#e1f5fe'
GROUP4_1 = '#b3e5fc'
GROUP4_2 = '#81d4fa'
GROUP4_3 = '#29b6f6'
GROUP4_4 = '#039be5'
GROUP4_5 = '#0277bd'
GROUP4_6 = '#01579b'

GROUPS = ['neutral', 'group1', 'group2', 'group3', 'group4']

MAIN_COLORS = {
    'neutral' : NEUTRAL_3,
    'group1' : GROUP1_3,
    'group2' : GROUP2_3,
    'group3' : GROUP3_3,
    'group4' : GROUP4_3
}

TRIADS = {
    'neutral' : [NEUTRAL_1, NEUTRAL_3, NEUTRAL_5],
    'group1' : [GROUP1_1, GROUP1_3, GROUP1_5],
    'group2' : [GROUP2_1, GROUP2_3, GROUP2_5],
    'group3' : [GROUP3_1, GROUP3_3, GROUP3_5],
    'group4' : [GROUP4_1, GROUP4_3, GROUP4_5]
}

SHADES = {
    'neutral' : [NEUTRAL_0, NEUTRAL_1, NEUTRAL_2, NEUTRAL_3, NEUTRAL_4, NEUTRAL_5, NEUTRAL_6],
    'group1' : [GROUP1_0, GROUP1_1, GROUP1_2, GROUP1_3, GROUP1_4, GROUP1_5, GROUP1_6],
    'group2' : [GROUP2_0, GROUP2_1, GROUP2_2, GROUP2_3, GROUP2_4, GROUP2_5, GROUP2_6],
    'group3' : [GROUP3_0, GROUP3_1, GROUP3_2, GROUP3_3, GROUP3_4, GROUP3_5, GROUP3_6],
    'group4' : [GROUP4_0, GROUP4_1, GROUP4_2, GROUP4_3, GROUP4_4, GROUP4_5, GROUP4_6]
}

STACKED_COLORS = {
    'CL0': {
        'selected' : SHADES['group4'][0],
        'unselected' : SHADES['neutral'][0],
    },
    'CL1': {
        'selected' : SHADES['group4'][1],
        'unselected' : SHADES['neutral'][1],
    },
    'CL2': {
        'selected' : SHADES['group4'][2],
        'unselected' : SHADES['neutral'][2],
    },
    'CL3': {
        'selected' : SHADES['group4'][3],
        'unselected' : SHADES['neutral'][3],
    },
    'CL4': {
        'selected' : SHADES['group4'][4],
        'unselected' : SHADES['neutral'][4],
    },
    'CL5': {
        'selected' : SHADES['group4'][5],
        'unselected' : SHADES['neutral'][5],
    },
    'CL6': {
        'selected' : SHADES['group4'][6],
        'unselected' : SHADES['neutral'][6],
    },
}