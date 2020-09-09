import eng_to_ipa

# Mapping from number to sounds
num_to_phones = {0: ['s', 'z'], 1: ['t', 'd', 'ð', 'θ'], 2: ['n', 'ŋ'], 3: ['m'], 4: ['r'],
                 5: ['l'], 6: ['ʤ', 'ʧ', 'ʃ', 'ʒ'], 7: ['k', 'g'], 8: ['f', 'v'],
                 9: ['p', 'b']}

# Reverse mapping from sound to number
phone_to_num = {x: k for k, v in num_to_phones.items() for x in v}


def major_decode_from_ipa(ipa):
    """Convert IPA to number sequence."""
    result = []
    for char in ipa:
        num = phone_to_num.get(char)
        if num is not None:
            result.append(num)
    return result


def numseq_to_str(numseq):
    """Convert number sequence to string."""
    return ''.join(str(x) for x in numseq)


def major_decode_word(word):
    ipa = eng_to_ipa.convert(word.lower(), retrieve_all=True, keep_punct=False, stress_marks=False)
    return numseq_to_str(major_decode_from_ipa(word))


def major_encode_number(number_string):
    # Clearly you'd want a long list of words.
    # And you wouldn't want to decode them on every call.
    words = ["table", "chair", "tuple"]

    encodings = []
    for w in words:
        if major_decode_word(w) == number_string:
            encodings.append(w)
    return encodings


if __name__ == "__main__":
    print(major_decode_word("table"))
    print(major_encode_number("195"))
