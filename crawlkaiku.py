import json
with open(('kaiku-18-19-new.json'), 'rb') as file:
    courses = json.load(file)

seen = set()
new_l = []
for d in courses:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_l.append(d)

with open('kaiku-18-19-new.json', 'w', encoding="utf-8") as outfile:
    json.dump(new_l, outfile, indent=2, ensure_ascii=False)

