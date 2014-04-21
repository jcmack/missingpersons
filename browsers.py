from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Earnhardt(webdriver.Remote):
    def __init__(self):
        super(Earnhardt, self).__init__()
        self.implicitly_wait(10)

    def select_option(self, elem, option):
        for option_elem in elem.find_elements_by_tag_name("option"):
            if option_elem.text.lower() == option.lower():
                option_elem.click()
                return

    def wait_until_clickable(self, loc_val, by=By.ID, timeout=10):
        return WebDriverWait(self, timeout).until(
            EC.element_to_be_clickable((by, loc_val)))

    def wait_until_txt_is_present(self, txt, loc_val, by=By.ID, timeout=10):
        return WebDriverWait(self, timeout).until(
            EC.text_to_be_present_in_element((by, loc_val), txt))

    def wait_until_visible(self, loc_val, by=By.ID, timeout=10):
        return WebDriverWait(self, timeout).until(
            EC.visibility_of_element_located((by, loc_val)))

class Firefox(Earnhardt, webdriver.Firefox):
    def __init__(self):
        super(Firefox, self).__init__()