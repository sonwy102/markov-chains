"""Generate Markov text from text files."""

from random import choice
from sys import argv


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # strip newline at the end of each line and replace with a space to make textfile into one single string
    text = open(file_path).read().replace('\n', ' ').rstrip(' ')

    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    words = text_string.split(' ')

    # Iterate over list of words until 3rd-to-last word
    for i in range(len(words) - 2):

        # If (word1, word2) already exists as a key in chains
        if (words[i], words[i+1]) in chains:
            # Append the next word (words[i + 2]) to the value list
            chains[(words[i], words[i + 1])].append(words[i + 2])
        else:
            # Else, initialize key and add next word as first item of value list
            chains[(words[i], words[i + 1])] = [words[i + 2]]

    return chains


def make_text(chains):
    """Return text from chains."""

    # Choose a random key (tuple)
    current_key = choice(list(chains))

    # Initialize words (list) with the 2 words in current_key
    words = list(current_key)

    # Repeat until current_key is non-existant in chains
    while current_key in chains:

        # Choose a random word from current_key's value (list)    
        next_word = choice(chains[current_key])

        # Append the random word to words (list)
        words.append(next_word)

        # Update current_key
        current_key = (current_key[1], next_word)

    return ' '.join(words)



# Open the file and turn it into one long string
input_text = open_and_read_file(argv[1])

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print(random_text)
