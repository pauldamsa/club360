# Copyright (c) 2025, pauldamsa and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class StockEntry(WebsiteGenerator):
    def validate(self):
        if not self.coach:
            return
            
        coach = frappe.get_doc("Coach", self.coach)
        settings = frappe.get_single("Settings")
        
        # Get all fields from Stock Entry doctype
        meta = frappe.get_meta('Stock Entry')
        product_fields = [field.fieldname for field in meta.fields 
                         if field.fieldtype == 'Int' 
                         and field.fieldname not in ['idx']]
        
        # Create products dictionary dynamically with settings multiplier
        products = {
            field: getattr(self, field) * getattr(settings, field, 1)
            for field in product_fields
            if getattr(self, field)
        }
        
        for product_name, quantity in products.items():
            existing_stock = None
            for stock in coach.stock:
                if stock.product.lower() == product_name and stock.type_event == self.type_event:
                    existing_stock = stock
                    break
            
            if existing_stock:
                existing_stock.servings += quantity
            else:
                coach.append("stock", {
                    "product": product_name.capitalize(),
                    "servings": quantity,
                    "type_event": self.type_event
                })
        
        coach.save()
