from base64 import b64encode

# ----------------------
#       Challenge 1
# ----------------------
input_a = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
result = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"


def bytes_to_b64_string(a: bytes) -> str:
    return b64encode(a).decode()


input_as_bytes = bytes.fromhex(input_a)
base_64 = bytes_to_b64_string(input_as_bytes)
print("challenge 1:", base_64 == result)


# ----------------------
#       Challenge 2
# ----------------------
def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    if len(bytes1) != len(bytes2):
        raise Exception(f"trying to xor bytes of different lengths {len(bytes1)} and {len(bytes2)}")
    return bytes(x ^ y for x, y in zip(bytes1, bytes2))


input_a = bytes.fromhex("1c0111001f010100061a024b53535009181c")
input_b = bytes.fromhex("686974207468652062756c6c277320657965")

result = xor_bytes(input_a, input_b)
print("challenge 2:", result)


# ----------------------
#       Challenge 3
# ----------------------

def single_byte_xor(text: bytes, key: int) -> bytes:
    if key > 256:
        raise ValueError(f"key must be less then 256, it is currently {key}")
    return bytes([b ^ key for b in text])


def all_single_byte_xor(text: bytes) -> list[bytes]:
    """returns a list of all possible single byte xors"""
    return [single_byte_xor(text, i) for i in range(256)]


def letter_ratio(input_bytes):
    "find the ratio on [0, 1] of letters in a given input"
    ascii_text_chars = list(range(97, 122)) + [32]  # includes space
    nb_letters = sum([x in ascii_text_chars for x in input_bytes])
    return nb_letters / len(input_bytes)


def find_most_likely_single_byte_xor(input_a: bytes):
    all_options = all_single_byte_xor(input_a)
    all_scores = [letter_ratio(a) for a in all_options]

    # look for the option with the highest letter ratio
    max_letter_ratio_i = all_scores.index(max(all_scores))
    return all_options[max_letter_ratio_i]


input_a = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
print("challenge 3:", find_most_likely_single_byte_xor(input_a))

# ----------------------
#       Challenge 4
# ----------------------

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

candidates = []
scores = []

for line in lines:
    line = bytes.fromhex(line)
    find_most_likely_single_byte_xor(line)
    for result in all_single_byte_xor(line):
        score = letter_ratio(result)

        if score > 0.7:  # under 0.7, it is too unlikely to be text
            scores.append(score)
            candidates.append(result)

index_best = scores.index(max(scores))
print("challenge 4:", candidates[index_best])


# ----------------------
#       Challenge 5
# ----------------------

def repeating_key_xor(text: bytes, key: bytes):
    l = len(key)
    return bytes([text[i] ^ key[i % l] for i in range(0, len(text))])


input_a = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
input_a = input_a.encode('utf-8')
result = repeating_key_xor(input_a, b'ICE')
print(f"challenge 5: {result == bytes.fromhex(expected)}")
