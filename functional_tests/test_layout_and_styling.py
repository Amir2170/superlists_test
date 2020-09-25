from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from unittest import skip

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
	
	def test_layout_and_styling(self):
		#edith goes to the homepage
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 568)
		
		#she notices the inputbox is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
		#she starts a new list and sees input is nicely centered 
		#there too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10,
		)
