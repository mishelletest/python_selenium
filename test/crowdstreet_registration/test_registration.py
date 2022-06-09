import unittest

from basefunc.browser import Browser
from basefunc.testUtilities import get_random_string
from basefunc.ui_constant import UI_WEBINAR_MESSAGE

browser = None
first_name = get_random_string(10).upper()
last_name = get_random_string(10).upper()
email_add = get_random_string(10).upper() +'@gmail.com'
password = 'abcdefG#1'

def setUpModule():
    global browser
    browser = Browser()


def tearDownModule():
    browser.stop()


class test_registration(unittest.TestCase):

    def setUp(self):
        pass

    def test_registration(self):
        browser.click_create_an_account_button()
        browser.fill_up_form(first_name=first_name, last_name=last_name, email=email_add, password=password, yes_investor=True)
        assert browser.is_text_appeared_on_page(text='AHHHH')
        assert browser.is_text_appeared_on_page(text=UI_WEBINAR_MESSAGE)

    def tearDown(self):
        browser.get_screenshot(screenshot_name='registration.png')

if __name__ == '__main__':
    unittest.main()