import unittest
from basefunc.config import TEST_CONFIG
from basefunc.driver import Driver


def setUpModule():
    pass


def tearDownModule():
    pass


class DriverCheck(unittest.TestCase):
    def setUp(self):
        pass

    def test_driver_check(self):
        drvClass = Driver.getDriverClass()
        (loaded, try_to_download) = drvClass.try_load_web_driver()
        if loaded:
            print("driver was successfully loaded")
        else:
            if try_to_download:
                print("Downloading latest driver ...")
            else:
                self.assertTrue(try_to_download, "Unknown error while loading web driver")
            drvClass.download_latest()
            (loaded, try_to_download) = drvClass.try_load_web_driver()
            self.assertTrue(loaded, "Error downloading latest web driver")
        print('Done')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()