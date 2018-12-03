import math
import random
import re

from sources import *

class Phonemes:
    """
    Basic sound units in a language.

    The sound units are grouped into categories.  Each category's name should
    be a single alphabetic character, so that these categories can be
    used in a Phonology's structure and restrictions.

    Sound units can be provided in two ways:
      - As a string or list, where each charater represents a single sound unit.
      - As a dictionary, where each key represents a sound unit and each value
        its relative frequency.

    When a dictionary is provided, `choose()` will sample a sound unit based
    on the probability distribution that the dictionary describes.  Otherwise,
    `choose()` will assume a uniform probability distribution.
    """
    def __init__(self, **kwargs):
        if not kwargs:
            kwargs['C'] = CONSONANT_SETS['Minimal']
            kwargs['V'] = VOWEL_SETS['Standard 5-vowel']
            kwargs['S'] = SIBILANT_SETS['Just s']
            kwargs['F'] = FINAL_SETS['m n']
            kwargs['L'] = LIQUID_SETS['r l']

        self._phonemes = {}
        for key in kwargs:
                self[key] = kwargs[key]

    def get_all_phonemes(self):
        """
        A sorted list of all phonemes across all categories.

        Copies and empty strings are removed.
        """
        inventory = []
        for category in self.get_categories():
            inventory += list(self[category])
        return sorted(filter(None, set(inventory)))

    def get_categories(self):
        """
        A list of all categories in this collection of phonemes.
        """
        return list(self._phonemes.keys())

    def choose(self, category):
        """
        Samples a single sound unit from a category.

        When a dictionary is provided, `choose()` will sample a sound unit
        based on the probability distribution that the dictionary describes.
        Otherwise, `choose()` will assume a uniform probability distribution.
        """
        phonemes = self[category]
        if type(phonemes) == dict:
            # If phonemes is a dict, each key represents a phoneme and each
            # value represents its relative frequency with respect to the
            # total.
            frequency_mass = sum(phonemes.values())
            sample = random.uniform(0, frequency_mass)
            cumulative_frequency = 0
            for phoneme, frequency in phonemes.items():
                cumulative_frequency += frequency
                if sample <= cumulative_frequency:
                    return phoneme
        else:
            # We use random.sample instead of random.choice, because it works
            # on non-indexable collections as well, such as sets.
            return random.sample(phonemes, 1)[0]

    def __getitem__(self, key):
        return self._phonemes[key]

    def __setitem__(self, key, value):
        if len(key) != 1 or len(value) == 0 or key == '?':
            raise KeyError('Not allowed')
        self._phonemes[key] = value
        self.__dict__[key] = value


class Phonology:
    """
    Generate syllables from phonemes following a structure and restrictions.

    A structure is a sequence of the Phonemes' categories which each may be
    followed by a question mark.  When generating a syllable, each category
    character will be replaced by a phoneme from that category.  If the
    category character is followed by a question mark, there is a 50% chance
    that this category will result in no phoneme.

    Restrictions is a list of regular expressions.  When a syllable matches
    such expressions, it is invalid, and cannot be generated.  In these
    regular expressions, a complete list of a category's phonemes can be
    included as \C where C is the category character.  For category C with
    phonemes 'abc', '\C' will be expanded to '[abc]'.

    There are no inter-syllabic checks.  If that is desired, this should be
    implemented on Language-level during word generation.
    """
    def __init__(self, phonemes, structure, restrictions=[]):
        self.phonemes = phonemes
        self.structure = structure
        self.restrictions = restrictions[:]

    def make_syllable(self):
        """
        Generate a new syllable.

        During syllable generation, a sound unit is sampled from Phonemes for
        each category symbol in the structure.  The question mark indicates
        that the preceeding category symbol has a 50% chance of being ignored.
        When the completed syllable matches one of the restrictions, the
        process is started again.
        """
        restrictions = [self._process_restriction(r)
                for r in self.restrictions]
        print(restrictions)

        categories = ''.join(self.phonemes.get_categories())
        structure_pattern = re.compile(r'([{}])(\??)'.format(categories))
        structure = structure_pattern.findall(self.structure)

        while True:
            # First, build up a complete syllable.
            # Afterwards we will check if it matches a restriction.
            # If it matches a restriction, we throw it away and start again.
            syllable = ''
            for phoneme_type, is_optional in structure:
                # If the phoneme type is followed by '?', there is a 50%
                # chance we won't use it.
                if is_optional and random.random() <  0.5:
                    continue
                syllable += self.phonemes.choose(phoneme_type)
            # If at least one restriction matched, we start again.
            if any(r.search(syllable) for r in restrictions):
                continue
            return syllable

    def _process_restriction(self, regex):
        """
        Rewrites the slash-category combinations in restrictions.

        Internal use only.  For each arbitrary category C with phonemes 'abc',
        '\C' will be expanded to '[abc]'.
        """
        pattern = re.compile(r"(?:\\\\)*(?:\\)([{}])"
                .format(''.join(self.phonemes.get_categories())))
        return re.compile(pattern.sub(self._regex_sub_repl, regex))

    def _regex_sub_repl(self, matchgroup):
        """
        Internal use only.  Helper function to `_process_restriction()`.
        """
        group = matchgroup.group(1)
        if group in self.phonemes.get_categories():
            return '[' + ''.join(self.phonemes[group]) + ']'

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, structure):
        """
        Verifies that structure is conform promised layout.
        """
        categories = ''.join(self.phonemes.get_categories())
        valid_structure = re.compile(r'([{}]\??)+'.format(categories))
        if valid_structure.fullmatch(structure) is None:
            raise ValueError('Invalid phoneme structure: ' + structure)
        self._structure = structure


class Orthography:
    """
    Renders words in a desired spelling format.

    Orthographies should provide a `spell(word)` method that transforms a
    string of phonemes to a more appropriate writing system, and a
    `get_alphabet(phonemes)` method that returns all possible characters for
    the corresponding phonemes.

    This base Orthography works on the character-level.  Implementing a
    syllabary could be done by providing a different spell function.
    """
    def __init__(self, consonants, vowels):
        self._consonants = consonants
        self._vowels = vowels

    def spell(self, word):
        spelled = ''
        for char in word:
            spelled += self._consonants.get(char,
                    self._vowels.get(char,
                        DEFAULT_ORTHOGRAPHY.get(char,
                            char)))
        return spelled

    def get_alphabet(self, phonemes):
        return self.spell(phonemes.get_all_phonemes())


class IPAOrthography(Orthography):
    """
    This Orthography saves the phonetic description.

    The "identity orthography", if you will.
    """
    def __init__(self, *args, **kwargs):
        pass

    def spell(self, syllable):
        return syllable.replace('.', '')


class Language:
    """
    Generates words and names, based on a phonology and orthography.
    """
    def __init__(self, phonology, orthography, 
            min_syllables=1, max_syllables=1,
            min_namelen=5, max_namelen=12,
            joiner=' ', genitive=[], definitive=[]):
        self.phonology = phonology
        self.orthography = orthography

        # For words
        self.min_syllables = min_syllables
        self.max_syllables = max_syllables
        self.morphemes = {}
        self.words = {}

        # For names
        self.min_namelen = min_namelen
        self.max_namelen = max_namelen
        self.joiner = joiner
        self.genitive = genitive[:]
        self.definitive = definitive[:]
        self.names = {}


    def spell(self, word):
        """
        Delegate to the orthography.
        """
        return self.orthography.spell(word)

    def get_alphabet(self):
        """
        Delegate to the orthography.
        """
        return orthography.get_alphabet(self.phonemes)

    def get_morpheme(self, category=None):
        new_factor = 1
        if category is None:
            new_factor = 10

        count = len(self.morphemes.get(category, []))
        if random.randint(0, count + new_factor) < count:
            return random.choice(self.morphemes[category])

        while True:
            morpheme = self.phonology.make_syllable()
            if any(morpheme in m for m in self.morphemes.values()):
                continue
            morphemes = self.morphemes.get(category, [])
            morphemes.append(morpheme)
            self.morphemes[category] = morphemes
            return morpheme

    def make_word(self, category):
        syllable_count = random.randint(self.min_syllables,
                self.max_syllables)
        syllables = []
        for i in range(syllable_count-1):
            syllables.append(self.get_morpheme())
        syllables.append(self.get_morpheme(category))
        word = '.'.join(syllables)
        return word

    def get_word(self, category=None):
        new_factor = 2
        if category is None:
            new_factor = 3

        count = len(self.words.get(category, []))
        if random.randint(0, count + new_factor) < count:
            return random.choice(self.words[category])

        while True:
            word = self.make_word(category)
            if any(word in w for w in self.words.values()):
                continue
            words = self.words.get(category, [])
            words.append(word)
            self.words[category] = words
            return word

    def make_name(self, category):
        genitive = self.genitive or self.get_morpheme('of')
        definitive = self.definitive or self.get_morpheme('the')

        while True:
            name = ''
            if random.random() < 0.5:
                name = self.get_word(category).capitalize()
            else:
                c1 = category if random.random() < 0.6 else None
                c2 = category if random.random() < 0.6 else None
                w1 = self.get_word(c1).capitalize()
                w2 = self.get_word(c2).capitalize()
                if w1 == w2:
                    continue
                if category == 'region' or random.random() < 0.5:
                    words = [w1, w2]
                else:
                    words = [w1, genitive, w2]
                name = self.joiner.join(words)
            if random.random() < 0.1:
                name = self.joiner.join([definitive, name]).capitalize()
            name = name.strip()

            if self.min_namelen > len(name) or len(name) > self.max_namelen:
                continue

            if any(name in n for n in self.names.values()):
                continue
            names = self.names.get(category, [])
            names.append(name)
            self.names[category] = names
            return name


def make_random_language():
    """
    Generate a language with randomly selected sounds, structures and a
    sensible set of restrictions on the phonology.
    """
    C = random.choice(list(CONSONANT_SETS.values()))
    V = random.choice(list(VOWEL_SETS.values()))
    S = random.choice(list(SIBILANT_SETS.values()))
    F = random.choice(list(FINAL_SETS.values()))
    L = random.choice(list(LIQUID_SETS.values()))
    random.shuffle(C)
    random.shuffle(V)
    random.shuffle(S)
    random.shuffle(F)
    random.shuffle(C)
    phonemes = Phonemes(C=C, V=V, S=S, F=F, L=L)

    phonology = Phonology(phonemes=phonemes,
            structure=random.choice(SYLLABLE_STRUCTURES),
            restrictions=RESTRICTION_SETS['Double and hard clusters'])

    orthography = Orthography(
            consonants=random.choice(list(CONSONANT_ORTHOGRAPHIES.values()), 2),
            vowels=random.choice(list(VOWEL_ORTHOGRAPHIES.values()), 2))

    min_syllables = random.randint(1, 3)
    if len(structure) < 3:
        min_syllables += 1
    max_syllables = min_syllables + random.randint(1, 7)
    joiner = random.choice(JOIN_SETS)

    lang = Language(phonology=phonology,
            orthography=orthography,
            min_syllables=min_syllables,
            max_syllables=max_syllables,
            joiner=joiner)

    return lang
