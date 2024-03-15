import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from db_manager import DBManager

class Scraper:
    def __init__(self) -> None:
        self.driver_setup()
        self.get_db_input()
        self.get_search_input()


    def get_db_input(self) -> None:
        user = input("Please enter the database user: ")
        password = input("Please enter the database password: ")
        database = input("Please enter the database name: ")
        table = input("Please enter the table name: ")
        self.db = DBManager(user, password, database, table)


    def get_search_input(self) -> None:
        job_title = str(input("Please enter the job title (empty for all jobs): "))
        if job_title == "":
            job_title = ""

        location = input("Please enter the job location (empty for all locations): ")
        if location == "":
            location = ""
            radius = ""
            self.get_search_link(job_title, location, radius)
            return

        else:
            while True:
                radius = str(input("Please enter the job radius (10km, 20km, 30km, 60km, 100km): "))

                if radius in ["10km", "20km", "30km", "60km", "100km", "10", "20", "30", "60", "100"]:
                    if "km" in radius:
                        radius = radius.replace("km", "")
                    break

        self.get_search_link(job_title, location, radius)

    
    def get_search_link(self, job_title, location, radius) -> None:
        if job_title != "" and location != "" and radius != "":
            self.search_link = f"https://www.profesia.sk/praca/{location}/{job_title}/?radius=radius{radius}"
        elif job_title == "" and location == "":
            self.search_link = "https://www.profesia.sk/praca/"
        elif job_title != "" and location == "":
            self.search_link = f"https://www.profesia.sk/praca/?search_anywhere={job_title}"
        elif job_title == "" and location != "":
            self.search_link = f"https://www.profesia.sk/praca/{location}/?radius=radius{radius}"
        print("Going to: ", self.search_link)

        self.get_total_pages()

    def driver_setup(self) -> None:
        service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)


    def get_total_pages(self) -> None:
        self.driver.get(self.search_link)
        time.sleep(1)
        try:
            self.driver.find_element(By.ID, "c-p-bn").click()
        except NoSuchElementException:
            pass
        time.sleep(0.5)
        self.total_pages = int(self.driver.find_element(By.XPATH, "//*[@id='content']/div/div/main/nav/ul/li[6]/a").get_attribute("text"))
        print("Total pages: ", self.total_pages)

        self.scrape_website()

    
    def convert_pay_to_int(self, string: str) -> int:

        divider = None
        string = string.lower()

        if "od" in string:
            string = string.replace("od", "")
        if "-" in string:
            string = string.split("-")[0]
        if "kč" in string:
            string = string.split("kč")[0]
            divider = 25
        if "eur" in string:
            string = string.split("eur")[0]
        if "ft" in string:
            string = string.split("ft")[0]
            divider = 400
        if "," in string:
            string = string.replace(",", ".")

        string = string.replace(" ", "")

        string = float(string)

        if string <= 100:
            string = string * 160
        
        if divider != None:
            string /= divider

        return int(string)

    
    def scrape_website(self):
        for page in range(self.total_pages):
            listings = self.driver.find_element(By.XPATH, "//*[@id='content']/div/div/main/div[1]/ul")
            listings = listings.find_elements(By.CLASS_NAME, "list-row")
            for index, listing in enumerate(listings):
                print("Scraping listing:", index + 1, "from page:", page + 1)
                try:
                    title = listing.find_element(By.CLASS_NAME, "title").text
                    employer = listing.find_element(By.CLASS_NAME, "employer").text
                    job_location = listing.find_element(By.CLASS_NAME, "job-location").text
                    pay_text = listing.find_element(By.CLASS_NAME, "label.label-bordered.green.half-margin-on-top").text
                    pay = self.convert_pay_to_int(pay_text)
                    print(title, employer, job_location, pay)
                    self.db.insert_into_db(title, employer, job_location, pay)
                except NoSuchElementException:
                    print("Error. Something is missing. Skipping.")

            if page != self.total_pages - 1:
                next_page = self.driver.find_element(By.CLASS_NAME, "next")
                self.driver.execute_script("arguments[0].scrollIntoView();", next_page)
                self.driver.execute_script("arguments[0].click();", next_page)

Scraper()
    