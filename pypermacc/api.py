import requests


class PermaccError(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)


class PermaccPrivateKeyRequired(PermaccError):
    def __init__(self):
        self.message = "Private Key required"


class Permacc(object):
    def __init__(self, key=''):
        self.base_url = 'https://api.perma.cc/v1/'
        self.user_agent = 'pypermacc'
        if key == '':
            self.private = False
        else:
            self.private = True
            self.key = key

    def requires_private_key(func):
        def decorated(*args, **kwargs):
            if not args[0].private:
                raise PermaccPrivateKeyRequired()
            return func(*args, **kwargs)
        return decorated

    def _request(self, path, params, private=False):
        if private:
            params['api_key'] = self.key
        r = requests.get(self.base_url + path, params=params)
        if r.status_code != 200:
            raise PermaccError('Bad HTTP Status Code %i' % r.status_code)
        return r

    def archive_detail(self, guid):
        """
        Get information about an archive entry

        Input:
        @guid : archive id (like Y6JJ-TDUJ)

        Returns:
            Dictionary with information
        """
        return self._request('public/archives/' + guid + '/', {}).json()

    def archive_download(self, guid):
        """
        Download WARC archive file

        Input:
        @guid: archive id (like Y6JJ-TDUJ)

        Returns:
            Binary file
        """
        return self._request(
            'public/archives/' + guid + '/download',
            {}
        ).content

    def public_archives(self, limit=10, offset=0):
        """
        Download list of public archives

        Input:
        -offset :
        -limit
        """
        return self._request(
            'public/archives/',
            {'limit': limit, 'offset': offset}
        ).json()

    @requires_private_key
    def archive_create(self, url, title="", folder=0):
        """
        Create an archive, requires private key

        Input:
        -url
        -title
        """
        data = {'url': url, 'title': title}
        if folder != 0:
            data['folder'] = folder
        r = requests.post(
            self.base_url + 'archives/',
            data=data,
            params={'api_key': self.key}
        )
        if r.status_code != 201:
            raise PermaccError('Bad HTTP Status Code %i' % r.status_code)
        return r.json()

    @requires_private_key
    def archive_delete(self, guid):
        """
        Deletes an archive
        """
        r = requests.delete(
            self.base_url + 'archives/' + guid + '/',
            params={'api_key': self.key}
        )
        return r
        if r.status_code != 204:
            raise PermaccError('Invalid return code: %i' % r.status_code)
        return True

    @requires_private_key
    def user_account(self):
        """
        Get information about the user account
        Requires a private key
        """
        return self._request('user/', {}, private=True).json()

    @requires_private_key
    def user_archives(self, limit=10, offset=0):
        """
        List user's archived pages

        Parameters
        ----------

        limit: int
            Number of results maximum
        offset: int
            Offset

        Returns
        -------
        dict
            dictionary of pages
        """
        return self._request(
                'user/archives/',
                {'limit': limit, 'offset': offset},
                private=True
        ).json()

    @requires_private_key
    def user_foders(self, limit=10, offset=0):
        """
        Returns user's folders
        """
        return self._request(
            'user/folders/',
            {'limit': limit, 'offset': offset},
            private=True
        ).json()

    @requires_private_key
    def user_organization(self, limit=1, offset=0):
        """
        Returns information on the organizations
        """
        return self._request(
            'user/organizations/',
            {'limit': limit, 'offset': offset},
            private=True
        ).json()
