# import os
# from src.strava_API.tokens_management.generate_credentials import GenerateAccessToken
from src.strava_API.tokens_management.get_oauth_code import GetOAuthCode
from src.strava_API.tokens_management.oauth_code_management.extract_code_selenium import GetCode
from config import url_to_get_OAuth_code
 
# print(os.getenv('ACTIVITY_ID'))
# from config import (
#     CLIENT_ID,
#     authorization_url,
#     header_code_OAuth,
#     redirect_url,
#     scopes,
#     seconds
# )

# url = f"{authorization_url}?client_id={CLIENT_ID}&response_type=code&redirect_uri={redirect_url}&approval_prompt=force&scope={scopes}"


# def get_url():
#     return f"{authorization_url}?client_id={CLIENT_ID}\
# &&response_type=code&redirect_uri={redirect_url}\
# approval_prompt=force&scope={scopes}"


# url = get_url()
# print(url)
# print(type(url))


def main():
    # a = GetOAuthCode()
    # url = get_oauth_code()
    # print(url)
    # GenerateAccessToken().generate_access_token()
    # print(ac)
    # code = GetOAuthCode().get_oauth_code()
    # print(code)
    # print(url_to_get_OAuth_code)
    code = GetCode().code_to_get_access_token()
    print(code)
    print(type(code))


if __name__ == "__main__":
    main()
