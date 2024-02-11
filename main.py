import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
import time
import logging
from logging import INFO, info, error
from selenium.webdriver.chrome.options import Options
import pyautogui
import random
import telebot
from datetime import datetime
from bot_secrets import Secrets
# exit(0)

logging.basicConfig(level=INFO)


class VisaBot:
    def __init__(self, driver, secrets) -> None:
        self.driver = driver
        self.secrets = secrets

    def run(self, driver):
        return self.main(driver)

    def clear_browsing_data(self, driver):
        driver.get("chrome://settings/clearBrowserData")

        time.sleep(2)  # Adjust the wait time as needed
        pyautogui.moveTo(1015, 764)
        pyautogui.click()
        pyautogui.click()

        # Find and click the 'Advanced' button (assuming Chrome version 87 or higher)
        # advanced_button = driver.find_element(By.CSS_SELECTOR, ".settings-ui [role='button']")
        # advanced_button.click()
        # print('here1')
        # time.sleep(1)  # Adjust the wait time as needed

        # Find and click the checkbox for 'Browsing history'
        # history_checkbox = driver.find_element(By.CSS_SELECTOR, "settings-checkbox[name='browsingHistory']")
        # history_checkbox.click()
        # print('here2')
        # time.sleep(0.5)

        # Find and click the 'Clear data' button
        # clear_data_button = driver.find_element(By.ID, "clearBrowsingDataConfirm")
        # clear_data_button.click()
        # print('here3')



    def random_move_to(self, from_point, to_point):
        start_x, start_y = from_point
        # Get the ending position
        end_x, end_y = to_point
        # Calculate the distance between the points
        distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
        # Number of steps to divide the movement into
        steps = int(distance / 10) + 1
        # Generate random points along the path
        points = [(start_x + (end_x - start_x) * i / steps + random.randint(-5, 5),
                start_y + (end_y - start_y) * i / steps + random.randint(-5, 5))
                for i in range(steps + 1)]
        # Perform the mouse movement
        for point in points:
            pyautogui.moveTo(point[0], point[1], duration=0.002)
            time.sleep(random.uniform(0.001, 0.005))
        pass


    def wait_for_verify(self, driver):
        time.sleep(10)
        return
        success_label = 'success-text'
        try:
            element = driver.find_element(By.ID, success_label)
            inner_html = element.get_attribute('innerHTML')
        except:
            pass

    def human_click(self, ):
        time.sleep(0.532)
        pyautogui.mouseDown()
        time.sleep(0.4524)
        pyautogui.mouseUp()


    def type_with_random_intervals(self, text):
        for char in text:
            pyautogui.typewrite(char)
            pyautogui.sleep(random.uniform(0.05, 0.2))


    def main(self, driver):
        pyautogui.moveTo(10, 10)

        info("sleeping")
        time.sleep(5.234)
        pyautogui.click()
        info('Opening URL')
        driver.get('https://visa.vfsglobal.com/gbr/en/ita/book-an-appointment')
        info("Sleeping")
        time.sleep(7.112)
        button_target = (383, 492)
        self.random_move_to((10, 10), button_target)
        time.sleep(0.4975)
        pyautogui.mouseDown()
        time.sleep(0.2331)
        pyautogui.mouseUp()
        time.sleep(10)

        info("switching to new tab")
        driver.switch_to.window(driver.window_handles[-1])
        email_field = (708, 366)
        # wait_for_verify()
        self.random_move_to(button_target, email_field)
        time.sleep(0.23)
        pyautogui.mouseDown()
        time.sleep(0.4524)
        pyautogui.mouseUp()
        time.sleep(0.245)

        self.type_with_random_intervals(self.secrets.username)
        time.sleep(0.532)
        pyautogui.press('tab')
        time.sleep(0.7876)
        self.type_with_random_intervals(self.secrets.password)
        time.sleep(0.142)
        pyautogui.press('enter')
        time.sleep(9.365)

        new_application_button = (1119, 244)
        self.random_move_to(email_field, new_application_button)
        time.sleep(0.532)
        pyautogui.mouseDown()
        time.sleep(0.4524)
        pyautogui.mouseUp()
        time.sleep(4.245)

        field_1 = (703, 517)
        field_1_1 = (648, 564)
        self.random_move_to(new_application_button, field_1)
        time.sleep(0.532)
        self.human_click()
        self.random_move_to(field_1, field_1_1)
        time.sleep(0.532)
        self.human_click()
        time.sleep(4.532)

        field_2 = (736, 643)
        self.random_move_to(field_1_1, field_2)
        time.sleep(0.532)
        self.human_click()
        self.human_click()
        time.sleep(4.532)

        field_3 = (530, 763)
        self.random_move_to(field_2, field_3)
        time.sleep(0.532)
        self.human_click()
        self.human_click()
        time.sleep(2)

        try:
            response_element = driver.find_element(By.CLASS_NAME, "alert-info")
            response_element_content = response_element.get_attribute('innerHTML')
        except Exception as e:
            error(f"Error: {e}")
            error("Did we trigger the CloudFlare?")
            return "denied"

        if 'We are sorry' in response_element_content:
            return 'empty'
        else:
            info("Found a slot!")
            return 'rich'


class TelegramBot:
    def __init__(self, secrets) -> None:
        self.bot_token = secrets.bot_token
        self.bot = telebot.TeleBot(self.bot_token)
        self.max_chat_id = secrets.max_chat_id

        @self.bot.message_handler(commands=['start', 'hello'])
        def send_welcome(self, message):
            self.bot.reply_to(message, "Howdy, how are you doing?")

        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            self.bot.reply_to(message, "Yes I AM alive...")

    def notify_max(self):
        self.bot.send_message(self.max_chat_id, '!!!!!NOW NOW NOW NOW NOW!!!!!')

    def send_logs(self, results_str:str):
        self.bot.send_message(self.max_chat_id, f'Debug: {results_str}')


class Main:
    def __init__(self) -> None:
        self.telegram = TelegramBot(Secrets())
        self.do_run = True
        self.results = []

    def run_cycle(self):
        info('opening webdriver')
        # options = Options()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--incognito")
        # free proxy server URL
        # proxy_server_url = "173.212.227.160:26854"
        # options.add_argument(f'--proxy-server={proxy_server_url}')
        driver = uc.Chrome(headless=False, use_subprocess=False, options=chrome_options)
        # clear_browsing_data(driver)
        agent = VisaBot(driver, Secrets())
        result = agent.run(driver)
        if result == 'rich':
            self.telegram.notify_max()
        now = datetime.now()
        formatted_date_time = now.strftime("%d %H:%M:%S")
        labelled_result = f"({formatted_date_time}): {result} | "
        self.results.append(f"{labelled_result}")
        info("Cycle done, sleeping for 10 seconds")
        time.sleep(10)
        driver.quit()

    def run_loop(self):
        while self.do_run:
            try:
                self.run_cycle()
            except Exception as e:
                now = datetime.now()
                formatted_date_time = now.strftime("%d %H:%M:%S")
                labelled_result = f"({formatted_date_time}): ERROR: {e} | "
                self.results.append(labelled_result)
            if len(self.results) > (3*60/10):  # if over 6 hours has passed since last results notification
                info("6 Hour cycle complete, sending results")
                results_str = ', '.join(self.results)
                self.telegram.send_logs(results_str)
                self.results = []
            info("Cycle completed, sleeping for 5 minutes")
            time.sleep(7*60)





if __name__ == "__main__":
    runner = Main()
    runner.run_loop()
