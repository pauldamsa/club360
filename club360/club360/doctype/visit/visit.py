# Copyright (c) 2025, pauldamsa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator
from club360.exceptions import NoValidMembershipError, NoServingsAvailableError

class Visit(WebsiteGenerator):
		
	def before_save(self):
		self.update_stock_coach()
		self.update_number_of_visits()

	def update_number_of_visits(self):
		club_member = frappe.get_doc("Club Member", self.club_member)
		today = frappe.utils.getdate(frappe.utils.today())
		valid_membership_found = False
		
		for membership in club_member.memberships:

			if membership.remaining_visits > 0 and frappe.utils.getdate(membership.end_date) >= today:
				membership.remaining_visits -= 1
				if membership.remaining_visits == 0:
					club_member.status = "Inactive"
				valid_membership_found = True
				break

		if not valid_membership_found:
			raise NoValidMembershipError("There is no valid membership for this club member")
			
		club_member.save()
	
	def update_stock_coach(self):
		club_member = frappe.get_doc("Club Member", self.club_member)
		coach = frappe.get_doc("Coach", club_member.coach)
		for stock_item in coach.stock:
			if self.type_event == stock_item.type_event:
				if stock_item.servings > 0:
					stock_item.servings -= 1
				else:
					raise NoServingsAvailableError(f"Coach products are out of stock! Check coach's stock")
					break
		coach.save()
