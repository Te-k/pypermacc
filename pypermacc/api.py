import requests
from datetime import datetime, timedelta
from urllib.parse import urljoin


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
        if key == '':
            self.private = False
        else:
            self.private = True
            self.key = key

    def _should_have_private_key(self):
        if not self.private:
            raise PermaccPrivateKeyRequired()

    def _request(self, path, params, private=False):
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
        return self._request('public/archives/' + guid + '/download', {}).content

    def public_archives(self, limit=10, offset=0):
        """
        Download list of public archives

        Input:
        -offset :
        -limit
        """
        return self._request('public/archives/', {'limit': limit, 'offset':offset}).json()

    def archive_create(self, url, title="", folder=0):
        """
        Create an archive, requires private key

        Input:
        -url
        -title
        """
        self._should_have_private_key()
        data = {'url': url, 'title': title}
        if folder != 0:
            data['folder'] = folder
        r = requests.post(self.base_url + 'archives/', data=data, params={'api_key': self.key})
        if r.status_code != 201:
            raise PermaccError('Bad HTTP Status Code %i' % r.status_code)
        return r.json()
