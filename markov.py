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


def make_chains(text_string, n):
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

    # Iterate over list of words
    for i in range(len(words) - n):

        # Create n-gram
        n_gram = tuple([words[j] for j in range(i, i + n)])
        
        # If n-gram already exists as a key in chains
        if n_gram in chains:
            # Append the next word (words[i + 2]) to the value list
            chains[n_gram].append(words[i + n])
        else:
            # Else, initialize key and add next word as first item of value list
            chains[n_gram] = [words[i + n]]

    return chains


def make_text(chains):
    """Return text from chains."""

    # Choose a initial random key (tuple)
    current_key = choice(list(chains))

    # Repeat searching for initial key until its first word is capitalized
    while not current_key[0][0].isupper():
        current_key = choice(list(chains))
    
    # Initialize words (list) with the words in current_key
    words = list(current_key)

    # Repeat until current_key is non-existant in chains
    while current_key in chains:

        # Choose a random word from current_key's value (list)    
        next_word = choice(chains[current_key])

        # Append the random word to words (list)
        words.append(next_word)

        # Update current_key
        current_key = tuple(list(current_key[j] for j in range(1, len(current_key))) + [next_word])

    return ' '.join(words)


# Open the file provided as command-line argument and turn it into one long string
input_text = open_and_read_file(argv[1])

# Get a Markov chain
chains = make_chains(input_text, 2)

# Produce random text
random_text = make_text(chains)

print(random_text)
