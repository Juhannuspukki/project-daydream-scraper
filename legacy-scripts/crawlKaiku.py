import json

# I honestly have no idea what this script does. Some kind of duplicate removal is my best guess
# I don't understand why there would be duplicates, though

with open(('kaiku-19-20-new.json'), 'rb') as file:
    courses = json.load(file)

seen = set()
new_l = []
for d in courses:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_l.append(d)

with open('kaiku-19-20-new.json', 'w', encoding="utf-8") as outfile:
    json.dump(new_l, outfile, indent=2, ensure_ascii=False)

