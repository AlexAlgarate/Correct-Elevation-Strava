class ReplaceWhiteSpace:
    @staticmethod
    def replace(string):
        return string.replace(" ", ".")


def extract_number(element):
    numbers = element.split()[0]
    return numbers


string = "Tengo el corazón contento "
d = ReplaceWhiteSpace()
print(d.replace(string))

# sequence = ["123225563 m", "1233"]
# elevation = sequence[0]
# elevation_clean = extract_number(elevation)
# print(type(elevation_clean))

# extract_elevation = lambda x: x[0].split()[0]
# elevation = extract_elevation(sequence)
# logger.info("CORRECT")
# # print(elevation)

