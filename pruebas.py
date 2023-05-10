# import os
from src.strava_api.tokens_management.get_access_token import GetAccessToken

# print(os.getenv('ACTIVITY_ID'))


def main():
    # a = GetOAuthCode()
    # url = get_oauth_code()
    # print(url)
    # GenerateAccessToken().generate_access_token()
    # code = GetOAuthCode().get_oauth_code()
    # print(code)

    # code = GetCode().code_to_get_access_token()
    # print(code)
    access_token = GetAccessToken().get_access_token()
    print(access_token)


if __name__ == "__main__":
    main()
