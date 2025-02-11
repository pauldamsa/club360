# Copyright (c) 2025, pauldamsa and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Coach(WebsiteGenerator):	
	def before_naming(self):
		self.full_name = f"{self.first_name} {self.last_name}"