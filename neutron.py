from selenium import webdriver

#set chromodriver.exe path
driver = webdriver.Chrome(executable_path="/usr/bin/chromium-browser")
driver.get('https://www.google.com')

driver.execute_script("window.open('');")
driver.implicitly_wait(5)

driver.switch_to.window(driver.window_handles[1])
driver.get("https://facebook.com")
driver.implicitly_wait(5)

driver.close()
driver.implicitly_wait(5)

driver.switch_to.window(driver.window_handles[0])
driver.get("https://www.yahoo.com")
driver.implicitly_wait(5)

#driver.close()