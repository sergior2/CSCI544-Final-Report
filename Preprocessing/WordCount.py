import sys
haikus = {}

for o in range(2, 6):
    for p in range(2, 8):
        for q in range(2, 6):
            haikus[f"{o}{p}{q}"] = []
with open(sys.argv[1], "r") as file:
    for line in file:
        trimmed = line.replace("$", "").strip()
        if '"' in trimmed:
            continue
        array = trimmed.split("/")
        if len(array) == 1:
            array = trimmed.split(",")
            syllable = "".join([str(x) for x in array[-3:]])
            if syllable != "575":
                continue

        key = ""
        output = []
        for words in array[:3]:
            words = list(filter(None, words.strip().split(" ")))
            key += str(len(words))
            output.append(" ".join(words))
        if key in haikus:
            haikus[key].append(" / ".join(output))

largestSubsets = []
for key in haikus.keys():
    largestSubsets.append(key)
    largestSubsets.sort(key=lambda x: len(haikus[x]), reverse=True)

# States right here how top 50 subset
largestSubsets = largestSubsets[:150]
for key in largestSubsets:
    print(key, len(haikus[key]))

with open("output.txt", "w") as file:
    for key in largestSubsets:
        for words in haikus[key]:
            keystr = ",".join(list(key))
            file.write(f"{keystr} | {words}\n")
