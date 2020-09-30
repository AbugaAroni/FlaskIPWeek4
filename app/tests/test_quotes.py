import unittest
from app.models import Quotes
Quotes = quotes.Quotes

class QuoteTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Quote class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_quote = Quotes(1234,'Jon','A thrilling nfwfwwSeries')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote,Quotes))
