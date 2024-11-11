from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    possible_deciphers = []
    ascii_codes = [ord(char) for char in ciphered]
    dictionary_set = set(dictionary)

    for shift in range(1, 27):
        shifted_ascii_codes = [(ascii - 97 - shift) % 26 + 97 if ascii != 32 else ascii for ascii in ascii_codes]
        deciphered_text = ''.join(chr(code) for code in shifted_ascii_codes)
        words = deciphered_text.split(" ")
        non_dictionary_word_count = sum(1 for word in words if word.lower() not in dictionary_set)
        possible_deciphers.append((deciphered_text, shift, non_dictionary_word_count))

    best_decipher = min(possible_deciphers, key=lambda x: x[2])
    return best_decipher
