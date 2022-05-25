import eng_to_ipa
import pickle

# Mapping from number to sounds
num_to_phones = {0: ['s', 'z'], 1: ['t', 'd', 'ð', 'θ'], 2: ['n'], 3: ['m'], 4: ['r'],
                 5: ['l'], 6: ['ʤ', 'ʧ', 'ʃ', 'ʒ'], 7: ['k', 'g'], 8: ['f', 'v'],
                 9: ['p', 'b']}

# Reverse mapping from sound to number
phone_to_num = {x: k for k, v in num_to_phones.items() for x in v}

def decode_from_ipa(ipa):
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

def decode_word(word):
    ipa = eng_to_ipa.convert(word.lower(), retrieve_all=True, keep_punct=False, stress_marks=False)
    return numseq_to_str(decode_from_ipa(word))

def encode_number(number_string):
    # Clearly you'd want a long list of words.
    # And you wouldn't want to decode them on every call.
    words = ["table", "chair", "tuple"]
    
    encodings = []
    for w in words:
        if decode_word(w) == number_string:
            encodings.append(w)
    return encodings

if __name__ == "__main__":

    #print(decode_word("table"))
    #print(encode_number("109"))

    # Use a pickled dictionary to encode words
    infile = open("num_to_words.pkl", "rb")
    mydict = pickle.load(infile)
    infile.close()    
    print(mydict["009"])
