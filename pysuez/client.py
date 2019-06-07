import requests
import re
import datetime



BASE_URI = 'https://www.toutsurmoneau.fr'
API_ENDPOINT_LOGIN = '/mon-compte-en-ligne/je-me-connecte'
API_ENDPOINT_DATA = '/mon-compte-en-ligne/statJData/'
API_ENDPOINT_HISTORY = '/mon-compte-en-ligne/statMData/'

class PySuezError(Exception):
    pass

class SuezClient():
    """Global variables."""

    def __init__(self, username, password, counter_id, session=None, timeout=None):
        """Initialize the client object."""
        self._username = username
        self._password = password
        self._counter_id = counter_id
        self._token = ''
        self._headers = {}
        self.data = {}
        self.attributes = {}
        self.success = False
        self._session = session
        self._timeout = timeout
        self.state = 0

    def _get_token(self):
        """Get the token"""
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'fr,fr-FR;q=0.8,en;q=0.6',
            'User-Agent': 'curl/7.54.0',
            'Connection': 'keep-alive',
            'Cookie': ''
        }

        url = BASE_URI+API_ENDPOINT_LOGIN

        response = requests.get(url, headers=headers)

        headers['Cookie'] = ""
        for key in response.cookies.get_dict():
            if headers['Cookie']:
                headers['Cookie'] += "; "
            headers['Cookie'] += key + "=" + response.cookies[key]

        phrase = re.compile('_csrf_token" value="(.*)" />')
        result = phrase.search(response.content.decode('utf-8'))
        self._token = result.group(1)
        self._headers = headers

    def _get_cookie(self):
        """Connect and get the cookie"""
        if self._session is None:
            self._session = requests.Session()
            
        self._get_token()
        data = {
            '_username': self._username,
            '_password': self._password,
            '_csrf_token': self._token,
            'signin[username]': self._username,
            'signin[password]': None,
            'tsme_user_login[_username]': self._username,
            'tsme_user_login[_password]': self._password
                }
        url = BASE_URI+API_ENDPOINT_LOGIN
        try:
            self._session.post(url,
                               headers=self._headers, 
                               data=data,
                               allow_redirects=False,
                               timeout=self._timeout)
        except OSError:
            raise PySuezError("Can not submit login form.")

        if not 'eZSESSID' in self._session.cookies.get_dict():
            raise PySuezError("Login error: Please check your username/password.")
        
        self._headers['Cookie'] = ''
        self._headers['Cookie'] = 'eZSESSID='+self._session.cookies.get("eZSESSID")
        return True
        

    def _fetch_data(self):
        """Fetch latest data from Suez."""
        now = datetime.datetime.now()
        today_year = now.strftime("%Y")
        today_month = now.strftime("%m")
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        yesterday_year = yesterday.strftime('%Y')
        yesterday_month = yesterday.strftime('%m')
        yesterday_day = yesterday.strftime('%d')
        url = BASE_URI+API_ENDPOINT_DATA
        url += '{}/{}/{}'.format(
            yesterday_year,
            yesterday_month, self._counter_id
            )
        
        self._get_cookie()

        data = requests.get(url, headers=self._headers)

        try:
            self.state = int(float(data.json()[int(
                yesterday_day)-1][1])*1000)
            self.success = True

        except ValueError:
            raise PySuezError("Issue with yesterday data")
            pass

        try:
            if yesterday_month != today_month:
                url = BASE_URI+API_ENDPOINT_DATA
                url += '{}/{}/{}'.format(
                    today_year,
                    today_month, self._counter_id
                    )
                data = requests.get(url, headers=self._headers)

            self.attributes['thisMonthConsumption'] = {}
            for item in data.json():
                self.attributes['thisMonthConsumption'][item[0]] = int(
                    float(item[1])*1000)

        except ValueError:
            raise PySuezError("Issue with this month data")
            pass

        try:
            if int(today_month) == 1:
                last_month = 12
                last_month_year = int(today_year) - 1
            else:
                last_month = int(today_month) - 1
                last_month_year = today_year

            url = BASE_URI+API_ENDPOINT_DATA
            url += '{}/{}/{}'.format(
                last_month_year, last_month,
                self._counter_id
                )

            data = requests.get(url, headers=self._headers)

            self.attributes['previousMonthConsumption'] = {}
            for item in data.json():
                self.attributes['previousMonthConsumption'][item[0]] = int(
                    float(item[1])*1000)

        except ValueError:
            raise PySuezError("Issue with previous month data")
            pass

        try:
            url = BASE_URI+API_ENDPOINT_HISTORY
            url += '{}'.format(self._counter_id)

            data = requests.get(url, headers=self._headers)
            fetched_data = data.json()
            self.attributes['highestMonthlyConsumption'] = int(
                float(fetched_data[-1])*1000)
            fetched_data.pop()
            self.attributes['lastYearOverAll'] = int(
                float(fetched_data[-1])*1000)
            fetched_data.pop()
            self.attributes['thisYearOverAll'] = int(
                float(fetched_data[-1])*1000)
            fetched_data.pop()
            self.attributes['history'] = {}
            for item in fetched_data:
                self.attributes['history'][item[3]] = int(
                    float(item[1])*1000)


        except ValueError:
            raise PySuezError("Issue with history data")
            pass

    def check_credentials(self):
        if self._session is None:
            self._session = requests.Session()
            
        self._get_token()
        data = {
            '_username': self._username,
            '_password': self._password,
            '_csrf_token': self._token,
            'signin[username]': self._username,
            'signin[password]': None,
            'tsme_user_login[_username]': self._username,
            'tsme_user_login[_password]': self._password
                }
        url = BASE_URI+API_ENDPOINT_LOGIN
        response = requests.post(url,
                               headers=self._headers, 
                               data=data,
                               allow_redirects=False,
                               timeout=self._timeout
            )
        if (
                ('Connexion en cours') in response.content.decode() or 
                ('se déconnecter') in response.content.decode()
                ):
            return True
        else:
            return False

    def update(self):
        """Return the latest collected data from Linky."""
        self._fetch_data()
        if not self.success:
            return
        return self.attributes
        
    def close_session(self):
        """Close current session."""
        self._session.close()
        self._session = None


