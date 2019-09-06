import re
import sys
import requests
import cssutils
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

# Constants
NO_CHANGE_TAGS = set(["html", "body", "head"])

def traverse(elements, driver):
    # don't pass in elements!  editing innerHTML basically destroys and recreates
    #  all elements below it in the DOM structure, which means any reference to those
    #  elements are destroyed.  
    # also use innerHTML.append!!! With restructuring the DOM because of references
    numElements = len(elements)
    for i in range(0, numElements):
        properties = driver.execute_script(
            'return window.getComputedStyle(arguments[0], null)', elements[i]
        )
        properties = str(properties)

        if elements[i].tag_name not in NO_CHANGE_TAGS:
            # print("element was not <html> or <body> or <head>.")
            if "font-size" in properties:
                checkTextSize(elements[i], driver)
            elif i > 0:
                # probably needs a different text size checker for a size with parent
                checkTextSize(elements[i - 1], driver)
            else:
                print("No text size found.  WCAG's recommends that a font size of 12pt or higher be used for visibility.")

def checkTextSize(element, driver):
    incorrectSizeText = 'The text size in this element is less than 12pt, which does not meet WCAG\'s recommendations for text size (12pt or higher).'
    val = element.value_of_css_property("font-size")
    if val is not None and int(val[:2]) < 20: # should be changed back to 12!!!
        print("")
        driver.execute_script("arguments[0].innerHTML = arguments[1]", element, incorrectSizeText)

def getBackgroundColor():
    print(0)

def main():
    """Gets the url intended for judging from the user, and calls xxx
        function to begin the process."""

    link: str = sys.argv[1]
    request = requests.get(link)
    soup = BeautifulSoup(request.content, 'html.parser')
    # print(soup)

    # Create a selenium instance
    ops = ChromeOptions()
    ops.add_experimental_option("detach", True)
    driver = Chrome(options=ops)
    driver.get(link)
    
    elements = driver.find_elements_by_xpath("//*")
    # elements = driver.find_elements_by_css_selector("*")

    traverse(elements, driver)


main()
