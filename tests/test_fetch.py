import datetime as dt
import unittest
from src.services.scadaFetcher import fetchScadaPntHistData
from src.config.appConfig import loadAppConfig


class TestFetch(unittest.TestCase):
    def setUp(self):
        # this method is called before executing each test method
        # common initialization activities like fetching database connections, api tokens etc. before starting each test method can be done here
        print("\\nsetup called...")
        self.start = dt.datetime.now()
        self.appConf = loadAppConfig()

    def testFetch(self) -> None:
        """This is a test method that tests addition
        """
        data = fetchScadaPntHistData(self.appConf.testPnt,
                                     dt.datetime.now()-dt.timedelta(minutes=30),
                                     dt.datetime.now()-dt.timedelta(minutes=10),
                                     'snap', 60)
        print(data)
        self.assertTrue(len(data) > 0)
        self.assertTrue(len(data[0]) == 2)

    def tearDown(self):
        # this method is called after each test method is executed
        # any common disposal activities like disposing connections, tokens etc. can be done in this method
        print("\\ntear down called...")
        print(f"executed in {dt.datetime.now()-self.start}")
