from time import sleep
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from singleton import singleton

@singleton
class Test:
    def __init__(self, url):
        sleep(5)
        # driver = webdriver.Remote("http://192.168.101.54:4444/wd/hub", desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver = webdriver.Firefox(executable_path=r"geckodriver.exe")
        self.driver.implicitly_wait(30)
        self.driver.get(url)

    def navigate(self, url):
        self.driver.get(url)
        
    def get_current_url(self):
        return str(self.driver.current_url)

    def wait_for_html_element_by_css_class(self, css_class, wait_time = 30):
        WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, css_class)))

    def wait_for_html_element_by_id(self, id, wait_time = 30):
        WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.ID, id)))

    def get_element_by_id(self, id, validate_if_shows=True):
        if validate_if_shows:
            self.wait_for_html_element_by_id(id)
        return self.driver.find_element(By.ID, id)

    def get_attribute_of_html_element_by_id(self, id, attribute, validate_if_shows=True):
        if validate_if_shows:
            self.wait_for_html_element_by_id(id)
        return self.driver.find_element(By.ID, id).get_attribute(attribute)
        
    def click_button_by_id(self, id, validate_if_shows=True):
        if validate_if_shows:
            self.wait_for_html_element_by_id(id)
        self.driver.find_element(By.ID, id).click()

    def fill_textbox_by_id(self, id, text, validate_if_shows=True, submit=False):
        if validate_if_shows:
            self.wait_for_html_element_by_id(id)
        self.driver.find_element(By.ID, id).clear()
        self.driver.find_element(By.ID, id).send_keys(text)
        if submit:
            self.driver.find_element(By.ID, id).submit()
    
    def get_elements_by_css_class(self, css_class, validate_if_shows=True):
        if validate_if_shows:
            self.wait_for_html_element_by_css_class(css_class)
        return self.driver.find_elements(By.CLASS_NAME, css_class)
    
    def get_elements_by_xpath(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    def select_option_dropdown(self, id, text, validate_if_shows=True):
        if validate_if_shows:
            self.wait_for_html_element_by_id(id)
        select = Select(self.driver.find_element(By.ID, id))
        select.select_by_visible_text(text)

    def capture(self, path):
        self.driver.save_screenshot(path)