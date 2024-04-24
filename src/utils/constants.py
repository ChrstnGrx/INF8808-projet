from enum import Enum

DRUGS = [
    "alcohol",
    "amphet",
    "amyl",
    "benzos",
    "cannabis",
    "coke",
    "crack",
    "ecstasy",
    "heroin",
    "ketamine",
    "legalh",
    "lsd",
    "meth",
    "mushrooms",
    "nicotine",
    "vsa"
]

PERSONNALITY = [
    "escore",
    "nscore",
    "oscore",
    "ascore",
    "cscore",
    "impulsive",
    "ss"
]

PERSONNALITY_INFO = {
    'escore': {
        'french': 'Extraversion'
    },
    'nscore': {
        'french': 'Neuroticisme'
    },
    'oscore': {
        'french': 'Ouverture'
    },
    'ascore': {
        'french': 'Agréabilité'
    },
    'cscore': {
        'french': 'Conscienciosité'
    },
    'impulsive': {
        'french': 'Impulsivité'
    },
    'ss': {
        'french': 'Recherche de sensations'
    }
}

DRUG_INFO = {
    'alcohol': {
        'group': 'group0',
        'french': 'alcool'
    },
    "amphet": {
        'group': 'group3',
        'french': 'amphétamines'
    },
    "amyl": {
        'group': 'group0',
        'french': 'nitrite d\'amyle'
    },
    "benzos": {
        'group': 'group0',
        'french': 'benzodiazépine'
    },
    "cannabis": {
        'group': 'group2',
        'french': 'cannabis'
    },
    "coke": {
        'group': 'group2',
        'french': 'cocaïne'
    },
    "crack": {
        'group': 'group1',
        'french': 'crack'
    },
    "ecstasy": {
        'group': 'group2',
        'french': 'ecstasy'
    },
    "heroin": {
        'group': 'group1',
        'french': 'héroïne'
    },
    "ketamine": {
        'group': 'group2',
        'french': 'kétamine'
    },
    "legalh": {
        'group': 'group2',
        'french': 'euphorisants légaux'
    },
    "lsd": {
        'group': 'group2',
        'french': 'LSD'
    },
    "meth": {
        'group': 'group3',
        'french': 'méthadone'
    },
    "mushrooms": {
        'group': 'group2',
        'french': 'champignons magiques'
    },
    "nicotine": {
        'group': 'group0',
        'french': 'nicotine'
    },
    "vsa": {
        'group': 'group0',
        'french': 'solvants volatils'
    }
}


class EducationLevel(Enum):
    BEFORE_16 = {'code': 'BEFORE_16',
                 'text': 'Quitté l\'école avant 16 ans', 'value': -2.43591}
    AT_16 = {'code': 'AT_16',
             'text': 'Quitté l\'école à 16 ans', 'value': -1.73790}
    AT_17 = {'code': 'AT_17',
             'text': 'Quitté l\'école à 17 ans', 'value': -1.43719}
    AT_18 = {'code': 'AT_18',
             'text': 'Quitté l\'école à 18 ans', 'value': -1.22751}
    SOME_COLLEGE_NO_DEGREE = {'code': 'SOME_COLLEGE_NO_DEGREE',
                              'text': 'Fréquenté une université, mais sans diplôme', 'value': -0.61113}
    PROF_DIPLOMA_CERTIFICATE = {'code': 'PROF_DIPLOMA_CERTIFICATE',
                                'text': 'Diplôme ou certificat professionnel', 'value': -0.05921}
    UNIVERSITY_DEGREE = {'code': 'UNIVERSITY_DEGREE',
                         'text': 'Baccaulauréat', 'value': 0.45468}
    MASTER_DEGREE = {'code': 'MASTER_DEGREE',
                     'text': 'Maîtrise', 'value': 1.16365}
    DOCTORATE_DEGREE = {'code': 'DOCTORATE_DEGREE',
                        'text': 'Doctorat', 'value': 1.98437}


GATEWAY_DRUGS = [
    'alcohol',
    'nicotine',
    'cannabis',
]

CONSUMPTION_CLASSES = {
    'CL0': 'Jamais consommée',
    'CL1': 'Consommée il y a plus d\'une décennie',
    'CL2': 'Consommée dans la dernière décennie',
    'CL3': 'Consommée dans la dernière année',
    'CL4': 'Consommée dans le dernier mois',
    'CL5': 'Consommée dans la dernière semaine',
    'CL6': 'Consommée dans le dernier jour'
}


AGE_CLASSES = {
    -0.95197: '18-24',
    -0.07854: '25-34',
     0.49788: '35-44',
     1.09449: '45-54',
     1.82213: '55-64',
     2.59171: '65+'
}

GENDER_CLASSES = {
     0.48246: 'Femme',
    -0.48246: 'Homme'
}

EDUCATION_CLASSES = {
    -2.43591: 'Quitté l\'école avant 16 ans',
    -1.73790: 'Quitté l\'école à 16 ans',
    -1.43719: 'Quitté l\'école à 17 ans',
    -1.22751: 'Quitté l\'école à 18 ans',
    -0.61113: 'Fréquenté une université, mais sans diplôme',
    -0.05921: 'Diplôme ou certificat professionnel',
     0.45468: 'Baccaulauréat',
     1.16365: 'Maîtrise',
     1.98437: 'Doctorat'
}


AGE_IMAGE_PATHS = {
    '18-24': '/assets/icons/ages/18-24.svg',
    '25-34': '/assets/icons/ages/25-34.svg',
    '35-44': '/assets/icons/ages/35-44.svg',
    '45-54': '/assets/icons/ages/45-54.png',
    '55-64': '/assets/icons/ages/55-64.svg',
    '65+': '/assets/icons/ages/65+.svg'
}

GENDER_IMAGE_PATHS = {
    'Femme': '/assets/icons/gender/woman.svg',
    'Homme': '/assets/icons/gender/man.svg'
}

EDUCATION_IMAGE_PATHS = {
    'Quitté l\'école avant 16 ans': '/assets/icons/education/Left_school_before_16.svg',
    'Quitté l\'école à 16 ans': '/assets/icons/education/Left_school_at_16.svg',
    'Quitté l\'école à 17 ans': '/assets/icons/education/Left_school_at_17.svg',
    'Quitté l\'école à 18 ans': '/assets/icons/education/Left_school_at_18.svg',
    'Fréquenté une université, mais sans diplôme': '/assets/icons/education/some_college_no_degree.svg',
    'Diplôme ou certificat professionnel': '/assets/icons/education/Professional_certificat_diploma.svg',
    'Baccaulauréat': '/assets/icons/education/baccalaureat.svg',
    'Maîtrise': '/assets/icons/education/maitrise.svg',
    'Doctorat': '/assets/icons/education/doctorat.svg'
}
