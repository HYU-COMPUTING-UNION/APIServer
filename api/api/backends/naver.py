from social_core.backends.naver import NaverOAuth2


class MyNaverOAuth2(NaverOAuth2):
    def get_user_details(self, response):
        """Return user details from Naver account"""
        return {
            'username': response.get('username'),
            'email': response.get('email'),
            'fullname': response.get('name'),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
                'https://openapi.naver.com/v1/nid/me',
                headers={
                    'Authorization': 'Bearer {0}'.format(access_token),
                }
        )['response']
