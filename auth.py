#!/usr/bin/env python
"""
Copyright (c) 2011 Chris Skalenda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import urllib
import httplib
import oauth2 as oauth
import urlparse
import json
import os.path
import time


class Auth():
    """
    Auth manages cli2phone's authentication with Google for access to
    chrometophone.
    """

    def __init__(self, url=None):
        if url is not None:
            self.url = url
        else:
            self.url = "https://chrometophone.appspot.com"

        self.authfile = "auth.json"

        if not os.path.exists(self.authfile):
            req_url = self.get_request_url()

            print "In order to use cli2phone, you must authorize cli2phone "\
                  "to access the google account your android phone uses.\n\n" \
                  "Grant access for cli2phone with the following URL:"
            print req_url

            print ""
            prompt = "After authorizing, enter the PIN provided by Google: "
            oauth_verifier = raw_input(prompt)

            self.get_access_keys(oauth_verifier)

        else:
            with open('auth.json', 'r') as f:
                self.access_token = json.load(f)

    def get_request_url(self):
        """
        Generates a request URL the user can use to authorize Google account
        access for cli2phone. This must be called before get_access_keys.
        """
        self.auth = {'request_url': '%s/_ah/OAuthGetRequestToken' % (self.url),
                    'auth_url': '%s/_ah/OAuthAuthorizeToken' % (self.url),
                    'access_url': '%s/_ah/OAuthGetAccessToken' % (self.url)}

        self.consumer = oauth.Consumer(key="anonymous", secret="anonymous")
        client = oauth.Client(self.consumer)
        resp, content = client.request("%s?%s&%s" %
                                          (self.auth['request_url'],
                                          "xoauth_displayname=cli2phone",
                                          "oauth_callback=oob"),
                                      'GET')

        if resp['status'] == '200':
            self.request_token = dict(urlparse.parse_qsl(content))

            url = '%s?oauth_token=%s&hd=default' % \
                  (self.auth['auth_url'], self.request_token['oauth_token'])

            return url

        else:
            raise IOError("Failed to retrieve request tokens from %s" %
                              self.auth["request_url"])

    def get_access_keys(self, oauth_verifier):
        """
        Takes an oauth_verifier PIN and the previously retrieved
        request_tokens, and retrieves authorization tokens from Google.
        """

        token = oauth.Token(self.request_token['oauth_token'],
                            self.request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, token)

        resp, content = client.request(self.auth['access_url'], "POST")

        if resp['status'] == '200':
            self.access_token = dict(urlparse.parse_qsl(content))

            with open('auth.json', mode='w') as f:
                json.dump(self.access_token, f)

            return self.access_token

        else:
            raise IOError("Failed to retrieve access tokens: PIN %s URL %s" %
                          (oauth_verifier, self.auth["request_url"]))

    def request(self, url, params):
        """
        Performs an oAuth authenticated request with previously retrieved
        access tokens.
        """

        params['oauth_version'] = '1.0'
        params['oauth_nonce'] = oauth.generate_nonce()
        params['oauth_timestamp'] = int(time.time())

        headers = {"Content-type": "application/x-www-form-urlencoded",
                  "X-Same-Domain": "true"}

        token = oauth.Token(key=self.access_token['oauth_token'],
                            secret=self.access_token['oauth_token_secret'])
        consumer = oauth.Consumer(key='anonymous', secret='anonymous')

        client = oauth.Client(consumer, token)
        client.set_signature_method(oauth.SignatureMethod_HMAC_SHA1())
        resp, content = client.request(url,
                                       method="POST",
                                       body=urllib.urlencode(params),
                                       headers=headers)

        if resp['status'] != '200':
            raise IOError("Failed to do request: %s" % content)
