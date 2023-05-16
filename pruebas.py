from src.strava_api.tokens_management.access_token import GetAccessToken
# from src.strava_api.tokens_management.oauth_code_management.get_oauth_code import GetOauthCode


def main():
    at = GetAccessToken().get_access_token()
    print(at)
    # code = GetOauthCode().get_oauth_code()
    # print(code)


if __name__ == "__main__":
    main()
