# Some systems decode 'ŋ' to 2, some to 7, and some to 27.
# Some avoid the ambiguity by simply not using 'ŋ'.

# I don't think we want to support the possibility of 27;
# That would require replacing 'ŋ' with "ng" since one phoneme maps to one digit.

ng_decodes_to = 7 # Possible values: 2, 7. Anything else won't use 'ŋ'.

# Mapping from number to sounds
num_to_phones = {0: ['s', 'z'],
                 1: ['t', 'd', 'ð', 'θ'],
                 2: ['n'],
                 3: ['m'],
                 4: ['r'],
                 5: ['l'],
                 6: ['ʤ', 'ʧ', 'ʃ', 'ʒ'],
                 7: ['k', 'g'],
                 8: ['f', 'v'],
                 9: ['p', 'b']}

if ng_decodes_to in [2, 7]:
    num_to_phones[ng_decodes_to].append('ŋ')

# Reverse mapping from sound to number
phone_to_num = {x: k
                for k, v in num_to_phones.items()
                for x in v}

