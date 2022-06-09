
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from basefunc.driver import Driver
from basefunc.config import TEST_CONFIG
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from basefunc.global_dict_variables import *
from basefunc.ui_constant import *



class Browser(object):

    def __init__(self):
        self.driver = Driver.getDriverClass().get_web_driver_instance()
        self.driver.maximize_window()
        self.implicit_wait_time = 5
        self.driver.implicitly_wait(self.implicit_wait_time)
        self.driver.get(TEST_CONFIG['server'])

    def stop(self):
        self.driver.close()
        self.driver.quit()

    def getDriver(self):
        return self.driver

    def click_when_element_is_present(self, xpath):
        delay = 20
        self.check_elem_state(xpath)
        try:
            element = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            return True

        except TimeoutException:
            return False

    def check_elem_state(self,xpath):
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #print('Element present')
        except:
            print(xpath + ' Sorry - not present')

        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            #print('Element visible')
        except:
            print(xpath + ' Sorry - not visible')

        try:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            #print('Element clickable')
        except:
            print(xpath + ' Sorry - not clickable')

    def sendKeysActiveElement(self, *keys):
        ActionChains(self.driver).send_keys(*keys).perform()

    def get_screenshot(self, screenshot_name='screenshot.png'):
        self.driver.save_screenshot(TEST_CONFIG['screenshotsfolder']+"/"+screenshot_name)

    def element_present(self, xpath):
        self.check_elem_state(xpath)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    def find_element_by_xpath(self, xpath):
        self.driver.find_element_by_xpath(xpath)

    def is_text_appeared_on_page(self, text='test'):
        text = self.element_present("//*[text()='"+text+"']")
        return text

    def keyboard_action(self, key=Keys.PAGE_DOWN, times=2):
        for _ in range(times):
            time.sleep(.5)
            self.sendKeysActiveElement(key)
        return True

    def click_create_an_account_button(self):
        self.click_when_element_is_present(dict_vars['CREATE AN ACCOUNT button'])

    def checked_not_robot_frame(self):
        '''save the main window handle'''
        main_window = self.driver.current_window_handle

        time.sleep(10)
        ''' get the recapthca iframe then navigate to it '''
        frame = self.driver.find_element_by_xpath('//iframe[@title="reCAPTCHA"]')
        self.driver.switch_to.frame(frame)

        '''now you can access the checkbox element'''
        self.click_when_element_is_present(dict_vars['Im not a robot'])

        ''' navigate back to main window '''
        self.driver.switch_to.window(main_window)

    def fill_up_form(self, first_name='name', last_name='last name', email='test@gmail.com', password='pw', yes_investor=True):
        assert self.is_text_appeared_on_page(text=UI_PAGE_TITLE)
        self.driver.find_element_by_id(dict_vars['First name field']).send_keys(first_name)
        self.driver.find_element_by_id(dict_vars['Last name field']).send_keys(last_name)
        self.driver.find_element_by_id(dict_vars['Email address field']).send_keys(email)
        self.driver.find_element_by_id(dict_vars['Password field']).send_keys(password)
        self.driver.find_element_by_id(dict_vars['Confirm Password field']).send_keys(password)
        if yes_investor is True:
            self.click_when_element_is_present(dict_vars['Yes radio button'])
        else:
            self.click_when_element_is_present(dict_vars['No radio button'])
        self.keyboard_action(key=Keys.PAGE_DOWN, times=1)
        time.sleep(1)
        self.driver.find_element_by_id(dict_vars['I have read and accept checkbox']).click()
        self.checked_not_robot_frame()
        self.click_when_element_is_present(dict_vars['Create an Account button'])
