from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait # Gerekli bekleme kodlarını import eder
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date

class Test_OdevClass:
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_deneme(self):
        print("1")

    @pytest.mark.parametrize("username,pw",[("","")])
    def test_null_login(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        self.waitForElementVisible((By.ID,"password"))
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{pw}.png")
        assert errorMessage.text == "Epic sadface: Username is required"


    @pytest.mark.parametrize("username,pw",[("standard_user","")])
    def test_null_password(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput= self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)

        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        errorMessage = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{pw}.png")
        assert errorMessage.text == "Epic sadface: Password is required"

    @pytest.mark.parametrize("username,pw",[("locked_out_user","secret_sauce")])
    def test_username_password(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)

        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        errorMessage = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{pw}.png")
        assert errorMessage.text == "Epic sadface: Sorry, this user has been locked out."


    @pytest.mark.parametrize("username,pw",[("", "")])
    def test_icon(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        self.waitForElementVisible((By.ID,"password"))
        
        
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{pw}.png") 

        errorIcon = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3/button")
        errorIcon.click()

        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{pw}.png")


    @pytest.mark.parametrize("username,pw",[("standard_user","secret_sauce")])
    def test_login_standard_user(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)

        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{pw}.png")

        self.driver.get("https://www.saucedemo.com/inventory.html")

        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login2-{username}-{pw}.png")

        sleep(2)


    @pytest.mark.parametrize("username,pw",[("standard_user","secret_sauce")])
    def test_show_product_count(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)

        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        itemNumber = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        self.driver.save_screenshot(f"{self.folderPath}/test-item-number-{username}-{pw}.png")
        assert len(itemNumber) == 6

    #ürün ekleme
    @pytest.mark.parametrize("username,pw",[("standard_user","secret_sauce")])
    def test_add(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        self.waitForElementVisible((By.ID,"add-to-cart-sauce-labs-backpack"))
        addInput = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        addInput.click()
        self.waitForElementVisible((By.ID,"add-to-cart-sauce-labs-bike-light"))
        addInput = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-bike-light")
        addInput.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add-{username}-{pw}.png")

        

    # ürün detayına ulaşma
    @pytest.mark.parametrize("username,pw",[("standard_user","secret_sauce")])
    def test_product_detail(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        self.waitForElementVisible((By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/a/div"))
        detailInput = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/a/div")
        detailInput.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-product-detail-{username}-{pw}.png")

    # ürün detayına gidip, ürünü ekleme ve sepete gitme
    @pytest.mark.parametrize("username,pw",[("standard_user","secret_sauce")])
    def test_product_detail_and_add(self,username,pw):
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        self.waitForElementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(pw)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

        self.waitForElementVisible((By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/a/div"))
        detailInput = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/a/div")
        detailInput.click()

        self.waitForElementVisible((By.ID,"add-to-cart-sauce-labs-backpack"))
        addInput = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        addInput.click()

        self.waitForElementVisible((By.XPATH,"/html/body/div[1]/div/div/div[1]/div[1]/div[3]/a"))
        cartInput = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div[1]/div[3]/a")
        cartInput.click()

        self.driver.save_screenshot(f"{self.folderPath}/test-product-detail-and-add-{username}-{pw}.png")




    def waitForElementVisible(self,locator):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located(locator))
