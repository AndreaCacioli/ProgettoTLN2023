def parse(csvPath):
    entries = []

    with open(csvPath, "r") as file:
        for j, line in enumerate(file):
            if j > 0:
                words = line.split(",")
                entry = []
                for i, word in enumerate(words):
                    if i != 2:
                        entry.append(word)
                    else:
                        entry.append(float(word))

                entries.append(entry)
    return entries
