from src.strava_api.tokens_management.access_token import GetAccessToken


def main():
    at = GetAccessToken().get_access_token()
    print(at)


if __name__ == "__main__":
    main()
