import frappe

@frappe.whitelist()
def create_club_member():
    print("Create Club Member API")
    # """
    # Create a new Club Member
    # """
    # try:
    #     # Create a new Club Member document
    #     club_member = frappe.get_doc({
    #         "doctype": "Club Member",
    #         **kwargs
    #     })
        
    #     club_member.insert(ignore_permissions=False)
    #     frappe.db.commit()
        
    #     return {
    #         "status": "success",
    #         "message": _("Club Member created successfully"),
    #         "data": club_member.as_dict()
    #     }
        
    # except Exception as e:
    #     frappe.log_error(frappe.get_traceback(), _("Club Member Creation Failed"))
    #     return {
    #         "status": "error",
    #         "message": _("Failed to create Club Member"),
    #         "error": str(e)
    #     }