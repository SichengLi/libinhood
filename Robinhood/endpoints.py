api_url = "https://api.robinhood.com"

def login():
    return api_url + "/oauth2/token/"

def stock_info(url = None):
    return url

def request_get(url, dataType='regular', payload=None, jsonify_data=True):
    """For a given url and payload, makes a get request and returns the data.
    :param url: The url to send a get request to.
    :type url: str
    :param dataType: Determines how to filter the data. 'regular' returns the unfiltered data. \
    'results' will return data['results']. 'pagination' will return data['results'] and append it with any \
    data that is in data['next']. 'indexzero' will return data['results'][0].
    :type dataType: Optional[str]
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as url/?key1=value1&key2=value2.
    :type payload: Optional[dict]
    :param jsonify_data: If this is true, will return requests.post().json(), otherwise will return response from requests.post().
    :type jsonify_data: bool
    :returns: Returns the data from the get request. If jsonify_data=True and requests returns an http code other than <200> \
    then either '[None]' or 'None' will be returned based on what the dataType parameter was set as.
    """
    if (dataType == 'results' or dataType == 'pagination'):
        data = [None]
    else:
        data = None
    res = None
    if jsonify_data:
        try:
            res = SESSION.get(url, params=payload)
            res.raise_for_status()
            data = res.json()
        except (requests.exceptions.HTTPError, AttributeError) as message:
            print(message, file=get_output())
            return(data)
    else:
        res = SESSION.get(url, params=payload)
        return(res)
    # Only continue to filter data if jsonify_data=True, and Session.get returned status code <200>.
    if (dataType == 'results'):
        try:
            data = data['results']
        except KeyError as message:
            print("{0} is not a key in the dictionary".format(message), file=get_output())
            return([None])
    elif (dataType == 'pagination'):
        counter = 2
        nextData = data
        try:
            data = data['results']
        except KeyError as message:
            print("{0} is not a key in the dictionary".format(message), file=get_output())
            return([None])

        if nextData['next']:
            print('Found Additional pages.', file=get_output())
        while nextData['next']:
            try:
                res = SESSION.get(nextData['next'])
                res.raise_for_status()
                nextData = res.json()
            except:
                print('Additional pages exist but could not be loaded.', file=get_output())
                return(data)
            print('Loading page '+str(counter)+' ...', file=get_output())
            counter += 1
            for item in nextData['results']:
                data.append(item)
    elif (dataType == 'indexzero'):
        try:
            data = data['results'][0]
        except KeyError as message:
            print("{0} is not a key in the dictionary".format(message), file=get_output())
            return(None)
        except IndexError as message:
            return(None)

    return(data)

def logout():
    return api_url + "/oauth2/revoke_token/"

def investment_profile():
    return api_url + "/user/investment_profile/"

def accounts():
    return api_url + "/accounts/"

def ach(option):
    '''
    Combination of 3 ACH endpoints. Options include:
        * iav
        * relationships
        * transfers
    '''
    return api_url + "/ach/iav/auth/" if option == "iav" else api_url + "/ach/{_option}/".format(_option=option)

def applications():
    return api_url + "/applications/"

def dividends():
    return api_url + "/dividends/"

def edocuments():
    return api_url + "/documents/"

def instruments(instrumentId=None, option=None):
    '''
    Return information about a specific instrument by providing its instrument id.
    Add extra options for additional information such as "popularity"
    '''
    return api_url + "/instruments/" + ("{id}/".format(id=instrumentId) if instrumentId else "") + ("{_option}/".format(_option=option) if option else "")

def margin_upgrades():
    return api_url + "/margin/upgrades/"

def markets():
    return api_url + "/markets/"

def notifications():
    return api_url + "/notifications/"

def orders(orderId=None):
    return api_url + "/orders/" + ("{id}/".format(id=orderId) if orderId else "")

def password_reset():
    return api_url + "/password_reset/request/"

def portfolios():
    return api_url + "/portfolios/"

def positions():
    return api_url + "/positions/"

def quotes():
    return api_url + "/quotes/"

def historicals():
    return api_url + "/quotes/historicals/"

def document_requests():
    return api_url + "/upload/document_requests/"

def user():
    return api_url + "/user/"

def watchlists():
    return api_url + "/watchlists/"

def news(stock):
    return api_url + "/midlands/news/{_stock}/".format(_stock=stock)

def fundamentals(stock):
    return api_url + "/fundamentals/{_stock}/".format(_stock=stock)

def tags(tag=None):
    '''
    Returns endpoint with tag concatenated.
    '''
    return api_url + "/midlands/tags/tag/{_tag}/".format(_tag=tag)

def chain(instrumentid):
    return api_url + "/options/chains/?equity_instrument_ids={_instrumentid}".format(_instrumentid=instrumentid)

def options(chainid, dates, option_type):
    return api_url + "/options/instruments/?chain_id={_chainid}&expiration_dates={_dates}&state=active&tradability=tradable&type={_type}".format(_chainid=chainid, _dates=dates, _type=option_type)

def market_data(optionid):
    return api_url + "/marketdata/options/{_optionid}/".format(_optionid=optionid)

def convert_token():
    return api_url + "/oauth2/migrate_token/"
