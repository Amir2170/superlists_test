from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from unittest import skip

from .base import FunctionalTest
				

class NewVisitorTest(FunctionalTest):
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
		#page title and header mention 'To-Do'
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('to-do', header_text)
		#user is invited to enter a to-do list straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 
		'Enter a to-do item')
		#user types smt into text box
		inputbox.send_keys('Buy peacock feathers')
		#when user press Enter page will refresh and 
		#put to-do list in specified text into the list
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
		#The page updates and there is a place holder still
		#inviting the user to enter a message user enter another 
		#message and press 'ENTER' the page updates and shows both items
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

	def test_multiple_users_can_start_lists_at_different_url(self):
		#user starts a new to do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
		#(edith)user notices her to do list has a unique url
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#a new user(francis) comes along...
        
		##we use a new browser session to make sure no 
		##information of edith is comming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()
        
		#user(francis) visits the homepage there is no sign of edith
		#information
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
        
		#francis starts a new list by entering a new item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
        
		#francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
        
		#agian there is no trace of edith list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
