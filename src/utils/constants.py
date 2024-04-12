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
        'french': 'substances volatiles'
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
    'CL0': 'Jamais utilisé',
    'CL1': 'Utilisé il y a plus de une décennie',
    'CL2': 'Utilisé dans la dernière décennie',
    'CL3': 'Utilisé dans la dernière année',
    'CL4': 'Utilisé dans le dernier mois',
    'CL5': 'Utilisé dans la dernière semaine',
    'CL6': 'Utilisé dans le dernier jour'
}