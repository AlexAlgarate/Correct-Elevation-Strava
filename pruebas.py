# import os
from src.strava_API.tokens_management.get_access_token import GetAccessToken
from src.strava_API.tokens_management.generate_credentials import GenerateAccessToken
from src.strava_API.tokens_management.get_oauth_code import GetOAuthCode
from src.strava_API.tokens_management.oauth_code_management.GetCode import GetCode
from config import url_to_get_OAuth_code
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
