import math


def grade_courses(course_list):
    # only contains the items that will be graded
    gradeable_items = []

    for item in course_list:
        if item["sampleSize"] >= 21:
            gradeable_items.append(item)

    gradeable_count = len(gradeable_items)

    letter_weights = [
        math.ceil(gradeable_count*0.05),
        math.ceil(gradeable_count*0.15),
        math.ceil(gradeable_count*0.20),
        math.floor(gradeable_count * 0.24),
        math.floor(gradeable_count * 0.20),
        math.floor(gradeable_count * 0.11)
    ]

    sum_of_letter_weights = sum(letter_weights)

    # assign improbaturs
    letter_weights.append(gradeable_count - sum_of_letter_weights)

    letters = ["L", "E", "M", "C", "B", "A", "I"]

    # tells which letter you are on
    letterCounter = 0

    # count courses that have received a "too good" grade due to rounding
    done = [0, 0]

    # tells how many courses of this letter have been graded
    total_counter = 1

    print(letter_weights)

    gradeable_items[0]["letter"] = letters[0]

    for i in range(1, len(gradeable_items)):
        if total_counter >= letter_weights[letterCounter] and gradeable_items[i]["grade"] == gradeable_items[i - 1]["grade"]:
            gradeable_items[i]["letter"] = gradeable_items[i - 1]["letter"]
            done[1] += 1
            total_counter += 1

        elif total_counter >= letter_weights[letterCounter]:
            try:
                gradeable_items[i]["letter"] = letters[letterCounter+1]
                letter_weights[letterCounter+1] -= sum(done)
                letterCounter += 1
            except IndexError:
                gradeable_items[i]["letter"] = letters[letterCounter]
            done[0] = done[1]
            done[1] = 0
            total_counter = 0
        else:
            gradeable_items[i]["letter"] = gradeable_items[i - 1]["letter"]
            total_counter += 1

    print("List length", len(gradeable_items), len(course_list))

    return course_list
