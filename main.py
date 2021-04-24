from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
)


class ReservationBot:
    def __init__(self, fobId, lastName):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(
            "https://reserve.anytimefitness.com/clubs/2946"  # replace this link with your desired club location
        )
        self.fobId = fobId
        self.lastName = lastName
        self.navigateAndLogin()

    def navigateAndLogin(self):
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_class_name("res-loginbutton").click()
            self.driver.implicitly_wait(10)
            wait = WebDriverWait(self.driver, 10)
            fobId = wait.until(EC.presence_of_element_located((By.NAME, "keyfob")))
            lastName = wait.until(EC.presence_of_element_located((By.NAME, "lastName")))
            fobId.send_keys(self.fobId)
            lastName.send_keys(self.lastName)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(
                '//button[contains(text(), "look me up!")]'
            ).click()
            self.driver.implicitly_wait(10)
        except:
            self.driver.quit()

    def pickTime(self, time):
        try:
            daySections = self.driver.find_elements_by_class_name("res-day")
            latestTime = 0

            for section in daySections:
                try:
                    section.find_element_by_class_name(
                        "res-day-reserved"
                    ).get_attribute("innerHTML")
                except:
                    times = section.find_elements_by_class_name("res-timeslot-select")
                    for timeElement in times:
                        if timeElement.text == time:
                            currTime = int(timeElement.get_attribute("data-start_int"))
                            if currTime > latestTime:
                                latestTime = currTime
                                timeElement.click()
            self.driver.implicitly_wait(10)
            confirmButtons = self.driver.find_elements_by_class_name(
                "res-timeslot-confirm"
            )
            for button in confirmButtons:
                try:
                    button.click()
                    self.driver.implicitly_wait(10)
                except ElementNotInteractableException:
                    pass
                except:
                    pass
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_class_name("res-final-selectnew").click()
        except:
            self.driver.quit()

    def cleanup(self):
        self.driver.quit()


if __name__ == "__main__":
    reservationBot = ReservationBot(
        # replace "fId" with your fobId, replace "lN" with your lastName
        fobId="fId",
        lastName="lN",
    )
    reservationBot.pickTime(
        time="7:30 AM"  # replace set time with desired time (must be formatted in "X:XX XX", ie "12:00 AM" or "6:00 PM")
    )
    reservationBot.cleanup()