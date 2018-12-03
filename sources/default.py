from collections import OrderedDict

"""
Contains default parameter sets for Phonemes, Phonology, Orthography and
Language that should give you decent-looking naming languages.

Searching (ctrl-f'ing) for the following lines will bring you to parameters
that would work with the corresponding classes.
### Phonemes
### Phonology
### Orthography
### Language
"""


### Phonemes
CONSONANT_SETS = {
    'Minimal': 'ptkmnls',
    'English-ish': 'ptkbdgmnlrsʃzʒʧ',
    'Pirahã (very simple)': 'ptkmnh',
    'Hawaiian-ish': 'hklmnpwʔ',
    'Greenlandic-ish': 'ptkqvsgrmnŋlj',
    'Arabic-ish': 'tksʃdbqɣxmnlrwj',
    'Arabic-lite': 'tkdgmnsʃ',
    'English-lite': 'ptkbdgmnszʒʧhjw',
    'Japanese-ish': 'ksztdnhbpmyrw',
}

SIBILANT_SETS = {
    'Just s': 's',
    's ʃ': 'sʃ',
    's ʃ f': 'sʃf',
}

LIQUID_SETS = {
    'r l': 'rl',
    'Just r': 'r',
    'Just l': 'l',
    'w j': 'wj',
    'r l w j': 'rlwj',
}

FINAL_SETS = {
    'm n': 'mn',
    's k': 'sk',
    'm n ŋ': 'mnŋ',
    's ʃ z ʒ': 'sʃzʒ',
    'Just n': 'n',
}

VOWEL_SETS = {
    'Standard 5-vowel': 'aeiou',
    '3-vowel a i u': 'aiu',
    'Extra A E I': 'aeiouAEI',
    'Extra U': 'aeiouU',
    '5-vowel a i u A I': 'aiuAI',
    '3-vowel e o u': 'eou',
    'Extra A O U': 'aeiouAOU',
}


### Phonology
SYLLABLE_STRUCTURES = [
	'CVC',
	'CVV?C',
	'CVVC?', 'CVC?', 'CV', 'VC', 'CVF', 'C?VC', 'CVF?',
	'CL?VC', 'CL?VF', 'S?CVC', 'S?CVF', 'S?CVC?',
	'C?VF', 'C?VC?', 'C?VF?', 'C?L?VC', 'VC',
	'CVL?C?', 'C?VL?C', 'C?VLC?',
]

"""
Restriction patterns are regular expressions that are preprocessed.
The following super-special sequences match with any character in the
Language's corresponding Phoneme group:
    - \C     Phonemes.C
    - \V     Phonemes.V
    - \S     Phonemes.S
    - \F     Phonemes.F
    - \L     Phonemes.L
The expansion of a super-special sequence happens when the replacement is
checked by the Language.

These super-special sequences are NOT ESCAPABLE!
"""
RESTRICTION_SETS = {
    'None': [],
    'Double sounds': [r'(.)\1'],
    'Doubles and hard clusters': [r'[sʃf][sʃ]', r'(ʃq)', r'(.)\1',
        r'(rl|lr|rw|wr|ww)'],
}


### Orthography
DEFAULT_ORTHOGRAPHY = {
	'ʃ': 'sh',
	'ʒ': 'zh',
	'ʧ': 'ch',
	'ʤ': 'j',
	'ŋ': 'ng',
	'j': 'y',
	'x': 'kh',
	'ɣ': 'gh',
	'ʔ': '‘',
	'A': 'á',
	'E': 'é',
	'I': 'í',
	'O': 'ó',
	'U': 'ú',
};

CONSONANT_ORTHOGRAPHIES = OrderedDict([
    ('Default', {}),
    ('Slavic', {
        'ʃ': 'š',
        'ʒ': 'ž',
        'ʧ': 'č',
        'ʤ': 'ǧ',
        'j': 'j',
    }),
    ('German', {
        'ʃ': 'sch',
        'ʒ': 'zh',
        'ʧ': 'tsch',
        'ʤ': 'dz',
        'j': 'j',
        'x': 'ch',
    }),
    ('French', {
        'ʃ': 'ch',
        'ʒ': 'j',
        'ʧ': 'tch',
        'ʤ': 'dj',
        'x': 'kh',
    }),
    ('Chinese (pinyin)', {
        'ʃ': 'x',
        'ʧ': 'q',
        'ʤ': 'j',
    }),
    ('Japanese (romanji)', {
        'ʃ': 'sh',
    }),
])

VOWEL_ORTHOGRAPHIES = OrderedDict([
    ('Ácutes', {}),
    ('Ümlauts', {
        'A': 'ä',
        'E': 'ë',
        'I': 'ï',
        'O': 'ö',
        'U': 'ü',
    }),
    ('Welsh', {
        'A': 'â',
        'E': 'ê',
        'I': 'y',
        'O': 'ô',
        'U': 'w',
    }),
    ('Diphthongs', {
        'A': 'au',
        'E': 'ei',
        'I': 'ie',
        'O': 'ou',
        'U': 'oo',
    }),
    ('Doubles', {
        'A': 'aa',
        'E': 'ee',
        'I': 'ii',
        'O': 'oo',
        'U': 'uu',
    }),
])


### Language
JOIN_SETS = '   -'
