import frappe

@frappe.whitelist()
def add_new_club_member(club_member):
    new_club_member = frappe.new_doc('Club Member')

    if club_member['source'] == 'Referral':
        referral_name = club_member['referral_of']['value']
        club_member_to_update_referrals_number = frappe.get_doc('Club Member', referral_name)
        club_member_to_update_referrals_number.referrals += 1
        club_member_to_update_referrals_number.save(ignore_permissions=True)
        
    new_club_member.first_name = club_member['first_name']
    new_club_member.last_name = club_member['last_name']
    new_club_member.coach = club_member['coach']['value']
    new_club_member.full_name = club_member['first_name'] + " " + club_member['last_name']
    new_club_member.source = club_member['source']
    new_club_member.status = 'Active'
    new_club_member.refferals = 0
    new_club_member.referral_of = club_member['referral_of']['value'] if club_member['source'] == 'Referral' else ''

    new_club_member.set('memberships', [{
        'type': '10 visits',
        'start_date': frappe.utils.getdate(frappe.utils.today()).strftime('%Y-%m-%d'),
        'end_date': (frappe.utils.getdate(frappe.utils.today()) + frappe.utils.datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
        'remaining_visits': 10
    }])
    new_club_member.insert(ignore_permissions=True)
    return new_club_member

@frappe.whitelist()
def edit_club_member(new_club_member):

    club_member = frappe.get_doc('Club Member', new_club_member['name'])
    club_member.first_name = new_club_member['first_name']
    club_member.last_name = new_club_member['last_name']

    if isinstance(new_club_member['coach'], dict):
        club_member.set('coach',new_club_member['coach']['value'])
    else:
        club_member.set('coach',new_club_member['coach'])

    club_member.full_name = new_club_member['first_name'] + " " + new_club_member['last_name']
    club_member.source = new_club_member['source']
    club_member.status = new_club_member['status']
    club_member.referrals = new_club_member['referrals']

    if isinstance(new_club_member['referral_of'], dict):
        club_member.referral_of = new_club_member['referral_of']['value'] if new_club_member['source'] == 'Referral' else ''
    else:
        club_member.referral_of = new_club_member['referral_of'] if new_club_member['source'] == 'Referral' else ''
    
    club_member.save(ignore_permissions=True)
    return club_member


@frappe.whitelist()
def add_new_membership(memberships_and_club_member):
    memberships = memberships_and_club_member['memberships']
    club_member = memberships_and_club_member['club_member']
    new_membership = memberships[-1]
    doc = frappe.get_doc('Club Member', club_member)
    doc.append('memberships', {
        'type': new_membership['type'],
        'start_date': new_membership['start_date'],
        'end_date': new_membership['end_date'],
        'remaining_visits': new_membership['remaining_visits']
    })
    doc.save(ignore_permissions=True)


@frappe.whitelist()
def edit_membership(request_membership):
    memberships = request_membership['memberships']
    club_member = request_membership['club_member']
    
    doc = frappe.get_doc('Club Member', club_member)
    doc.memberships = []  # Clear existing memberships
    
    for membership in memberships:
        doc.append('memberships', {
            'type': membership['type'],
            'start_date': membership['start_date'],
            'end_date': membership['end_date'],
            'remaining_visits': membership['remaining_visits']
        })
    
    doc.save(ignore_permissions=True)
    return doc

@frappe.whitelist()
def delete_club_member(club_member):
    try:
        doc = frappe.get_doc('Club Member', club_member.get('name'))  # Fix: use get() for safe access
        doc_name = doc.name  # store name before deletion
        doc.delete(ignore_permissions=True)
        frappe.db.commit()
        return {"message": f"Club member {doc_name} deleted successfully"}
    except frappe.DoesNotExistError:
        frappe.throw('Club Member not found')
    except Exception as e:
        frappe.throw(f'Error deleting club member: {str(e)}')

@frappe.whitelist()
def delete_club_member_membership(memberships_and_club_member):
    memberships = memberships_and_club_member['memberships']
    club_member = memberships_and_club_member['club_member']
    doc = frappe.get_doc('Club Member', club_member['full_name'])
    doc.memberships = []
    for membership in memberships:
        doc.append('memberships', {
            'type': membership['type'],
            'start_date': membership['start_date'],
            'end_date': membership['end_date'],
            'remaining_visits': membership['remaining_visits']
        })
    doc.save(ignore_permissions=True)
    return doc


@frappe.whitelist()
def add_new_coach(coach):
    new_coach = frappe.new_doc('Coach')
    new_coach.first_name = coach['first_name']
    new_coach.last_name = coach['last_name']
    new_coach.full_name = coach['first_name'] + " " + coach['last_name']
    new_coach.id_herbalife = coach['id_herbalife']
    new_coach.email = coach['email']
    new_coach.phone = coach['phone_number']
    new_coach.role = coach['role']

    if isinstance(coach['sponsor'], dict):
        new_coach.sponsor = coach['sponsor']['value']
    else:
        new_coach.sponsor = coach['sponsor']

    new_coach.insert(ignore_permissions=True)
    return new_coach


@frappe.whitelist()
def edit_coach(coach):
    try:
        print(frappe.as_json(coach))
        doc = frappe.get_doc('Coach', {'id_herbalife': coach['id_herbalife']})
        doc.first_name = coach['first_name']
        doc.last_name = coach['last_name']
        doc.full_name = coach['first_name'] + " " + coach['last_name']
        doc.id_herbalife = coach['id_herbalife']
        doc.email = coach['email']
        doc.phone = coach['phone_number']
        doc.role = coach['role']
        doc.level = coach['level']

        if isinstance(coach['sponsor'], dict):
            doc.sponsor = coach['sponsor']['value']
        else:
            doc.sponsor = coach['sponsor']

        doc.save(ignore_permissions=True)
        return doc
    except frappe.DoesNotExistError:
        frappe.throw('Coach not found')
    except Exception as e:
        frappe.throw(f'Error updating coach: {str(e)}')
