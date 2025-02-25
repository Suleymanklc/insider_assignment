import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InsiderTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def test_1_home_page(self):
        self.driver.get("https://useinsider.com/")
        self.assertIn("Insider", self.driver.title, "Home page did not load correctly.")

    def test_2_careers_page(self):
        self.driver.get("https://useinsider.com/")
        company_menu = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Company")))
        company_menu.click()
        careers_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Careers")))
        careers_link.click()

        self.assertIn("Careers", self.driver.title, "Career page did not load correctly.")

        locations_block = self.wait.until(EC.presence_of_element_located((By.ID, "locations")))
        teams_block = self.wait.until(EC.presence_of_element_located((By.ID, "teams")))
        life_at_insider_block = self.wait.until(EC.presence_of_element_located((By.ID, "life-at-insider")))
        self.assertTrue(locations_block.is_displayed(), "Locations block is not displayed.")
        self.assertTrue(teams_block.is_displayed(), "Teams block is not displayed.")
        self.assertTrue(life_at_insider_block.is_displayed(), "Life at Insider block is not displayed.")

    def test_3_qa_jobs_filter(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        see_all_qa_jobs_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "See all QA jobs")))
        see_all_qa_jobs_button.click()

        location_filter = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Istanbul, Turkey')]")))
        location_filter.click()

        department_filter = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Quality Assurance')]")))
        department_filter.click()

        jobs_list = self.wait.until(EC.presence_of_element_located((By.ID, "jobs-list")))
        self.assertTrue(jobs_list.is_displayed(), "Jobs list is not displayed.")

    def test_4_verify_job_details(self):
        self.test_3_qa_jobs_filter()

        jobs = self.driver.find_elements(By.CLASS_NAME, "job-item")
        for job in jobs:
            position = job.find_element(By.CLASS_NAME, "position").text
            department = job.find_element(By.CLASS_NAME, "department").text
            location = job.find_element(By.CLASS_NAME, "location").text

            self.assertIn("Quality Assurance", position, "Position does not contain 'Quality Assurance'.")
            self.assertIn("Quality Assurance", department, "Department does not contain 'Quality Assurance'.")
            self.assertIn("Istanbul, Turkey", location, "Location does not contain 'Istanbul, Turkey'.")

    def test_5_view_role_redirect(self):
        self.test_3_qa_jobs_filter()

        view_role_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "view-role")))
        view_role_button.click()

        self.driver.switch_to.window(self.driver.window_handles[1])
        self.assertIn("Lever", self.driver.title, "Did not redirect to Lever Application form.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
