import hashlib


def parse_input(filename: str = "input.txt") -> bytes:
    rv: str = ""
    with open(filename, mode="rt") as inputfile:
        rv = inputfile.read().strip()

    return bytes(rv, "utf-8")


input = parse_input()


def churn(prefix: bytes, suffix: int) -> tuple[bool, str, bytes]:
    test = prefix + bytes(str(suffix), "utf-8")
    hash = hashlib.md5(test).hexdigest()
    return hash.startswith("00000"), hash, test


suffix: int = 0
while True:
    is_match, hash, test = churn(input, suffix)
    if is_match:
        print("hash found!", hash, suffix, test.decode("utf-8"))
        break

    suffix += 1


with open("result.txt", mode="wt") as result:
    result.write(f"{suffix}\n")

with open("output.txt", mode="wt") as outfile:
    suffix = 0
    while True:
        is_match, hash, test = churn(input, suffix)
        outfile.write(f"{int(is_match)} {suffix: >12d} {hash} {test.decode('utf-8')}\n")
        if is_match:
            break

        suffix += 1
