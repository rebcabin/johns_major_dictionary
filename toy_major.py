import eng_to_ipa
from maps import num_to_phones, phone_to_num

def major_decode_from_ipa(ipa):
    """Convert IPA to number sequence."""

    
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
