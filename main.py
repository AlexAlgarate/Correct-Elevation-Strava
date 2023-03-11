from src.utils.summary import Summary
from strava_elevation_correction_OOP import CorrectElevation


def main():
    # df = Summary().fetch_ids_data()
    id = [8040982449]
    correct_elevation = CorrectElevation(id)
    correct_elevation.run()


if __name__ == '__main__':
    main()
