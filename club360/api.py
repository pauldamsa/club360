import frappe

@frappe.whitelist()
def add_new_club_member(club_member):
    new_club_member = frappe.new_doc('Club Member')


    new_club_member.first_name = club_member['first_name']
    new_club_member.last_name = club_member['last_name']
    new_club_member.coach = club_member['coach']['value']
    new_club_member.full_name = club_member['first_name'] + " " + club_member['last_name']
    new_club_member.source = club_member['source']
    new_club_member.status = 'Active'
    new_club_member.refferal = 0
    new_club_member.referral_of = club_member['referral_of']['value']
    
    new_club_member.set('memberships', [{
        'type': '10 visits',
        'start_date': frappe.utils.getdate(frappe.utils.today()).strftime('%Y-%m-%d'),
        'end_date': (frappe.utils.getdate(frappe.utils.today()) + frappe.utils.datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
        'remaining_visits': 10
    }])

    # print("New Club Member:", frappe.as_json(new_club_member.as_dict()))
    new_club_member.insert(ignore_permissions=True)
    return new_club_member