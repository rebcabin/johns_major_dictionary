import eng_to_ipa
import pickle
from collections import defaultdict
import pprint
import timeit
from typing import *
from maps import num_to_phones, phone_to_num


def ipa_to_numseq(word: str):
    """Convert IPA to number sequence."""
    result = []
    for char in word:
        num = phone_to_num.get(char)
        if num is not None:
            result.append(num)
    return result


def numseq_to_str(numseq: Iterable[int]):
    """Convert number sequence to string."""
    return ''.join(str(x) for x in numseq)


def word_to_numseq(word: str):
    fixed_word = word.lower().strip()
    ipa = eng_to_ipa.convert(
        fixed_word,
        retrieve_all=True,
        keep_punct=False,
        stress_marks=False)
    the_ipa = ipa[0]
    # if the_ipa == (fixed_word + '*'):
    #     print({'error': 'MISS', 'word': fixed_word, 'ipa': ipa, 'the_ipa': the_ipa})

    result = numseq_to_str(ipa_to_numseq(the_ipa))
    return result


# All this stuff is global so that 'timeit' can get at it easily.
# begin ridiculous globals


lines = []
num_to_words = defaultdict(set)
count = 0
furst_rule = True  # using Bruno Furst's convention that
#                    only the first three numerals are significant


def build_dict_in_memory():
    global lines
    global num_to_phones
    global count
    global furst_rule
    for line in lines:
        if "'" in line:
            continue  # skip over possessives
        word = line.strip().lower()
        numstr = word_to_numseq(line)
        if (count % 1000) == 0:
            print({'word': word, 'numstr': numstr, 'furst numstr': numstr[:3]})
        count += 1
        num_to_words[numstr].add(word)
        if furst_rule:
            num_to_words[numstr[:3]].add(word)


# end ridiculous globals


def main():
    try:
        with open("num_to_words.pkl", "rb") as infile:
            new_dict = pickle.load(infile)
            pprint.pprint({'142': new_dict['142'],
                           'thing': word_to_numseq('thing'),
                           'think': word_to_numseq('think')})

    except FileNotFoundError as ed:
        try:
            with open('/usr/share/dict/american-english', 'r') as file:
                global lines
                lines = file.readlines()
                the_time = timeit.timeit(
                    stmt='build_dict_in_memory()',
                    setup='pass',
                    timer=timeit.default_timer,
                    globals=globals(),
                    number=1)
                pprint.pprint({'time to build the dictionary': the_time})
            with open('num_to_words.pkl', 'wb') as outfile:
                global num_to_words
                pickle.dump(num_to_words, outfile)

        except FileNotFoundError as ef:
            raise FileNotFoundError('try "sudo apt install wamerican" to get the dictionary')


if __name__ == '__main__':
    main()
