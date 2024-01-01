
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import random
import csv
import sys

opr_id = sys.argv[1]

csv_file = open('output.csv','a', newline='',encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Operator ID', 'Route', 'Start Time', 'End Time', 'Time Taken'])

options = Options()
options.add_argument('--disable-notifications')
try:
    driver = webdriver.Chrome(ChromeDriverManager(version='116.0.5845.96').install(),options=chrome_options1)
except:
    driver=webdriver.Chrome(options=options)
wait=WebDriverWait(driver,500)

driver.maximize_window()
    
driver.get("https://xyz.com")

driver.find_element("id","inputEmail").send_keys("aziya@xyz.com")
driver.find_element("id","inputPassword").send_keys("abcd")
driver.find_element("id","btn_submit").click()
print("Login Successful")
driver.implicitly_wait(50)

wait = WebDriverWait(driver,500)

operators =[opr_id]
for i in range(len(operators)) :
	# Operator selection
	operator = Select(driver.find_element(By.ID,"nav_t"))
	operator.select_by_value(operators[i])

	for i in range(3) :
		try :
			sleep(3)
			master=driver.find_element(By.CSS_SELECTOR, "#ul > li.master_dash.nav-items > a").click()
			driver.refresh()
			break
		except :
		    print("Exception: Stale Element")	
	
	for i in range(2):
		try:
			wait.until(EC.element_to_be_clickable((By.ID, "btnselected"))).click()
			wait.until(EC.presence_of_element_located((By.XPATH,"//input[@type='search']")))
			break
		except:
			print()

	modal_buttons = driver.find_elements(By.XPATH,value="//tbody/tr[@class='odd'][10]//button[@id='popup']")

	
	for i in range(7):

		modal_buttons = driver.find_elements(By.XPATH,value="//tbody/tr[@class='odd'][10]//button[@id='popup']")

		
		sleep(1)
		
		picked = random.choice(modal_buttons)
		picked.click()
	   
		
		sleep(2)

		schedule_details = wait.until(EC.presence_of_element_located((By.ID, "mod-label"))).get_attribute("innerHTML")

		print(schedule_details)

		opt_option = ["0"] # "1","2"

		for i in range(len(opt_option)):
		   	option = Select(wait.until(EC.presence_of_element_located((By.ID, "pr_val"))))
		   	option.select_by_value(opt_option[i])
		   	button = driver.find_element(By.ID, "btn_opt")
		   	button.click()

		   	start_time = time.time()
		   	start_datetime = datetime.now()
		   	wait.until(EC.alert_is_present())
		   	driver.switch_to.alert.accept()
		   	end_time = time.time()
		   	end_datetime = datetime.now()
		   	time_taken = end_time - start_time

		   	print(opt_option[i],"Routes optimization time taken: ",time_taken)

		wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='myModal_pc']/div/div/div[10]/button"))).click()
		sleep(3)
		
		csv_writer.writerow([operators[0],schedule_details,start_datetime,end_datetime,time_taken])

	start_time = None
	end_time = None
	time_taken = None
	start_datetime = None
	end_datetime = None



csv_file.close()
driver.close()
