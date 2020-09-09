import eng_to_ipa
import pickle
from collections import defaultdict
import pprint
import timeit
from typing import *
from maps import num_to_phones, phone_to_num


# Mapping from number to sounds
num_to_phones = {0: ['s', 'z'],
                 1: ['t', 'd', 'ð', 'θ'],
                 2: ['n'],
                 3: ['m'],
                 4: ['r'],
                 5: ['l'],
                 6: ['ʤ', 'ʧ', 'ʃ', 'ʒ'],
                 7: ['k', 'g', 'ŋ'],
                 8: ['f', 'v'],
                 9: ['p', 'b']}

# Reverse mapping from sound to number
phone_to_num = {x: k
                for k, v in num_to_phones.items()
                for x in v}


def ipa_to_numseq(ipa_word: str):
    """Convert IPA to number sequence."""
    result = []
    for ipa_char in ipa_word:
        num = phone_to_num.get(ipa_char)
        if num is not None:
            result.append(num)
    return result


def numseq_to_str(numseq: Iterable[int]):
    """Convert number sequence to string."""
    return ''.join(str(x) for x in numseq)

hit_count = 0
miss_count = 0

def eng_word_to_numseq(eng_word: str):
    fixed_eng_word = eng_word.lower().strip()
    ipa = eng_to_ipa.convert(
        fixed_eng_word,
        retrieve_all=True,
        keep_punct=False,
        stress_marks=False)
    the_ipa = ipa[0]  # arbitrary choice amongst pronunciation variants
    global hit_count
    global miss_count
    if the_ipa == (fixed_eng_word + '*'):
        miss_count += 1
        result = None
        if __debug__:
            print({'error': 'MISS',
                   'word': fixed_eng_word,
                   'ipa': ipa,
                   'the_ipa': the_ipa,
                   'hit count': hit_count,
                   'miss count': miss_count,
                   'total': hit_count + miss_count,
                   })
    else:
        hit_count += 1
        result = numseq_to_str(ipa_to_numseq(the_ipa))
        if __debug__:
            print({'error': 'HIT ',
                   'word': fixed_eng_word,
                   'ipa': ipa,
                   'the_ipa': the_ipa,
                   'hit count': hit_count,
                   'miss count': miss_count,
                   'total': hit_count + miss_count,
                   })

    return result


# All this stuff is global so that 'timeit' can get at it easily.
# begin ridiculous globals


lines = []
num_to_words = defaultdict(set)
valid_count = 0
furst_rule = True  # using Bruno Furst's convention that
#################### only the first three numerals are significant


def build_dict_in_memory():
    global lines
    global num_to_phones
    global valid_count
    global furst_rule
    for line in lines:
        if "'" in line:
            continue  # skip over possessives
        word = line.strip().lower()
        numstr = eng_word_to_numseq(line)
        if numstr:
            if (valid_count % 1000) == 0:
                print({'word': word,
                       'numstr': numstr,
                       'furst numstr': numstr[:3],
                       'valid_count': valid_count})
                valid_count += 1
                num_to_words[numstr].add(word)
            if furst_rule:
                num_to_words[numstr[:3]].add(word)


# end ridiculous globals


def main():
    try:
        with open("num_to_words.pkl", "rb") as infile:
            new_dict = pickle.load(infile)
            pprint.pprint({'142': new_dict['142'],
                           'thing': eng_word_to_numseq('thing'),
                           'think': eng_word_to_numseq('think')})

    except FileNotFoundError as ed:
        try:
            with open('/usr/share/dict/american-english', 'r') as file:
                global hit_count
                global miss_count
                global lines
                hit_count = 0
                miss_count = 0
                lines = file.readlines()
                the_time = timeit.timeit(
                    stmt='build_dict_in_memory()',
                    setup='pass',
                    timer=timeit.default_timer,
                    globals=globals(),
                    number=1)
                pprint.pprint({'time to build the dictionary': the_time,
                               'hit count': hit_count,
                               'miss count': miss_count,
                               'total': hit_count + miss_count})
            with open('num_to_words.pkl', 'wb') as outfile:
                global num_to_words
                pickle.dump(num_to_words, outfile)

        except FileNotFoundError as ef:
            raise FileNotFoundError('try "sudo apt install wamerican" to get the dictionary')


if __name__ == '__main__':
    main()
