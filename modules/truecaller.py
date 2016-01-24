
#!/bin/python
# coding: utf-8

'''
Dependencies are the selenium module and Firefox

'''
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# chromedriver = "../chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# driver = webdriver.Chrome(chromedriver, chrome_options=options, )


def get_truecaller_result(phone):
    driver = webdriver.Firefox()
    #These are gmail credentials
    username = 'httrafficking123'
    password = 'stopthetrafficking'
    
    #Selenium searches truecaller and automatically
    #completes authentication process with google
    driver.get('http://www.truecaller.com/us/' + phone)
    time.sleep(2)

    google_button = driver.find_element_by_id('signInGoogle')
    google_button.click()
    time.sleep(2)

    main_window_handle = driver.current_window_handle

    google_button = driver.find_element_by_id('signInGoogle')
    google_button.click()
    time.sleep(2) 

    for handle in driver.window_handles:
        if handle != main_window_handle:
            signin_window_handle = handle
            break

    driver.switch_to.window(signin_window_handle)

    username_element = driver.find_element_by_id('Email')
    username_element.send_keys(username)
    time.sleep(2)

    next_button = driver.find_element_by_name('signIn')
    next_button.click()
    time.sleep(2)

    password_element = driver.find_element_by_id('Passwd')
    password_element.send_keys(password)
    time.sleep(2)

    next_button = driver.find_element_by_id('signIn')
    next_button.click()
    time.sleep(2)

    approve_button = driver.find_element_by_id('submit_approve_access')
    approve_button.click()
    time.sleep(2)

    driver.switch_to.window(main_window_handle)
    time.sleep(2)

    result_class = driver.find_element_by_class_name('detailView__nameText')
    result = result_class.text
    # try:
    #     driver.quit()
    # except AttributeError:
    #     pass
    driver.close()
    
    #Closes all emulated Chrome windows
    if len(driver.window_handles) > 0:
        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)
            driver.close()
        
    return result
    
# print get_truecaller_result('617-916-9754')











