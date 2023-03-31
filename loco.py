import logging
from functools import reduce


logger = logging.getLogger()


def extract_number(element):
    numbers = element.split()[0]
    return numbers


# sequence = ["123225563 m", "1233"]
# elevation = sequence[0]
# elevation_clean = extract_number(elevation)
# print(type(elevation_clean))

# extract_elevation = lambda x: x[0].split()[0]
# elevation = extract_elevation(sequence)
# logger.info("CORRECT")
# # print(elevation)

