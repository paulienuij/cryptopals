from base64 import b64decode
from itertools import combinations
from math import floor
from typing import List

from matplotlib import pyplot as plt

from set_1.set1 import xor_bytes, find_most_likely_single_byte_xor, repeating_key_xor


# ---------------------------------
#     compute Hamming distance
# ---------------------------------

def hamming_distance(a: bytes, b: bytes):
    # xor to get 1 for each differing bet
    r = xor_bytes(a, b)
    # convert to int to count number of ones
    return int.from_bytes(r, "big").bit_count()


a = "this is a test"
b = "wokka wokka!!!"

print("challenge 6:")
print(f"    Hamming distance check: {hamming_distance(a.encode('utf-8'), b.encode('utf-8'))}")


# ---------------------------------
#   Find most likely key length
# ---------------------------------

def _normalised_hamming_dist(chunks: List[bytes]) -> float:
    """
    find the average Hamming distance between any 2 combinations of the chunks
       example:
          if there are 4 chunks: A, B, C, and D
          compute the Hamming distances of: A-B, A-C, A-D, B-C, B-D and C-D
          return the average
    """
    dists = []
    chunk_length = len(chunks[0])

    for a, b in combinations(chunks, 2):
        dists.append(hamming_distance(a, b) / chunk_length)

    return sum(dists) / len(dists)


def _chunk(a, l: int, n: int):
    """
    generate n chunks of length l
    example: a = b"HUIfTQsPAh9PE048GmllH0kcDk4TAQsHThsBFkU2AB4BSWQgVB0dQzNTTmVS"
             n = 4, l = 3
             returns: HUI, fTQ, sPA, h9P
    """
    if n * l > len(a):
        raise ValueError(f"you can't take {n} chuncks of length {l} out of input of length {len(a)}")
    return [a[i:i + l] for i in range(0, n * l, l)]


def find_all_hem_dists(encoded_text, max_k, nb_of_chunks, plot=False):
    key_lengths = list(range(2, max_k + 1))
    hem_dists = []
    for k in key_lengths:
        hem_dists.append(
            _normalised_hamming_dist(_chunk(encoded_text, k, nb_of_chunks))
        )

    if plot:
        fig, ax = plt.subplots()
        ax.plot(key_lengths, hem_dists)
        ax.set_xlabel("key length")
        ax.set_ylabel("normalised Hamming distance")
        ax.set_xlim(2, max_k)
        plt.title(f"normalized Hamming distance based on {nb_of_chunks} chunks for each key length")
        plt.show()

    return key_lengths, hem_dists


# find keysize

with open("input_6.txt", "rb") as f:
    text = b64decode(f.read())

_, h_dists = find_all_hem_dists(text, 40, 10, plot=False)
keysize = h_dists.index(min(h_dists)) + 2
print(f"    most likely keysize:    {keysize}")

# ---------------------------------
#         Find the key
# ---------------------------------

# now we know the key length, we can break it into chunks
number_of_chunks = floor(len(text) / keysize)
chunks = _chunk(text, keysize, number_of_chunks)

key = ""

# Now transpose the blocks: make a block that is the first byte of every chunk,
#                           and a block that is the second byte of every chunk, and so on

for k in range(keysize):
    blocks_k = bytes(chunk[k] for chunk in chunks)
    _, letter = find_most_likely_single_byte_xor(blocks_k)
    key = key + chr(letter)

print(f"    most likely key:        {key}")

# ---------------------------------
#           Break it!
# ---------------------------------

with open("output_6.txt", "wb") as f:
    f.write(repeating_key_xor(text, key.encode("ascii")))
