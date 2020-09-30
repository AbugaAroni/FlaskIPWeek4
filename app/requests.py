import urllib.request,json#
from .models import Quotes

def get_quotes():
    '''
    Function that gets the json response to our url request
    '''
    get_quotes='http://quotes.stormconsultancy.co.uk/random.json'

    with urllib.request.urlopen(get_quotes) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quotes_results = None

        if get_quotes_response:
            #quotes_results_list = get_quotes_response
            #quotes_results = process_results(quotes_results_list)

            id = get_quotes_response.get('id')
            author = get_quotes_response.get('author')
            quote = get_quotes_response.get('quote')

            quote_object = Quotes(id, author, quote)
            quote_results= quote_object

    return quote_results

def process_results(quotes_list):
    '''
    Function  that processes the quotes result and transform them to a list of Objects

    Args:
        quotes_list: A list of dictionaries that contain movie details

    Returns :
        quote_results: A list of quote objects
    '''
    id = quotes_list.get('id')
    author =quotes_list.get('author')
    quote = quotes_list.get('quote')

    quote_object = Quotes(id , author ,quote)
    quote_results= quote_object

    return quote_results
