import frappe
from frappe.exceptions import ValidationError
from club360.exceptions import NoValidMembershipError, NoServingsAvailableError
from datetime import datetime
import calendar

@frappe.whitelist()
def add_new_club_member(club_member):
    new_club_member = frappe.new_doc('Club Member')

    if club_member['source'] == 'Referral':
        referral_id = club_member['referral_of']['value']
        club_member_to_update_referrals_number = frappe.get_doc('Club Member', referral_id)
        club_member_to_update_referrals_number.referrals += 1
        club_member_to_update_referrals_number.save(ignore_permissions=True)
       
    new_club_member.first_name = club_member['first_name']
    new_club_member.last_name = club_member['last_name']
    new_club_member.coach = club_member['coach']['value']
    new_club_member.full_name = club_member['first_name'] + " " + club_member['last_name']
    new_club_member.source = club_member['source']
    new_club_member.status = 'Active'
    new_club_member.type = 'Club Member'
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
    club_member.type = new_club_member['type']

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

    club_member_to_update = frappe.get_doc('Club Member', club_member)
    club_member_to_update.status = 'Active'
    club_member_to_update.save(ignore_permissions=True)
    
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
    try:
        memberships = memberships_and_club_member['memberships']
        club_member_name = memberships_and_club_member['club_member']['name']  # Get the name from the club member object
        
        doc = frappe.get_doc('Club Member', club_member_name)
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
    except Exception as e:
        frappe.throw(str(e))


@frappe.whitelist()
def add_new_coach(coach):
    new_coach = frappe.new_doc('Coach')
    new_coach.first_name = coach['first_name']
    new_coach.last_name = coach['last_name']
    new_coach.full_name = coach['first_name'] + " " + coach['last_name']
    new_coach.id_herbalife = coach['id_herbalife']
    new_coach.email = coach['email']
    new_coach.phone_number = coach['phone_number']
    new_coach.role = coach['role']
    new_coach.level = coach['level']  # Add this line to set the level

    if isinstance(coach['sponsor'], dict):
        new_coach.sponsor = coach['sponsor']['value']
    else:
        new_coach.sponsor = coach['sponsor']

    new_coach.insert(ignore_permissions=True)
    return new_coach


@frappe.whitelist()
def edit_coach(coach):
    try:
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

@frappe.whitelist()
def delete_coach(coach):
    try:
        doc = frappe.get_doc('Coach', {'id_herbalife': coach.get('id_herbalife')})
        doc_name = doc.full_name
        doc.delete(ignore_permissions=True)
        frappe.db.commit()
        return {"message": f"Coach {doc_name} deleted successfully"}
    except frappe.DoesNotExistError:
        frappe.throw('Coach not found')
    except Exception as e:
        frappe.throw(f'Error deleting coach: {str(e)}')

@frappe.whitelist()
def add_visit(visit_data):
    try:
        new_visit = frappe.new_doc('Visit')
        new_visit.club_member = visit_data['club_member']['value']
        new_visit.date = visit_data['date']
        new_visit.type_event = visit_data['type_event']

        try:
            new_visit.insert(ignore_permissions=True)
            return new_visit
        except NoValidMembershipError as e:
            return f"Error adding visit: {str(e)}"
        except NoServingsAvailableError as e:
            return f"Error adding visit: {str(e)}"
            
    except Exception as e:
        frappe.throw(str(e))

@frappe.whitelist()
def delete_visit(visit):
    try:
        doc = frappe.get_doc('Visit', visit.get('name'))
        doc_name = doc.name
        
        # restore the visit count
        club_member = frappe.get_doc('Club Member', doc.club_member)
        if club_member.memberships:
            active_membership = club_member.memberships[-1]
            active_membership.remaining_visits += 1
            if active_membership.remaining_visits == 1:
                club_member.status = "Active"
            club_member.save(ignore_permissions=True)
        
        # Delete the visit
        doc.delete(ignore_permissions=True)
        frappe.db.commit()
        
        return {"message": f"Visit {doc_name} deleted successfully"}
    except frappe.DoesNotExistError:
        frappe.throw('Visit not found')
    except Exception as e:
        frappe.throw(f'Error deleting visit: {str(e)}')

@frappe.whitelist()
def edit_visit(visit_data):
    try:
        doc = frappe.get_doc('Visit', visit_data['name'])
        # print(frappe.as_json(doc))
        doc.club_member = visit_data['club_member']
        # doc.data = visit_data['date']
        doc.date = visit_data['date'] 
        doc.type_event = visit_data['type_event']
        # print(frappe.as_json(doc))
        doc.save(ignore_permissions=True)
        return doc
    except frappe.DoesNotExistError:
        frappe.throw('Visit not found')
    except Exception as e:
        frappe.throw(f'Error updating visit: {str(e)}')

@frappe.whitelist()
def add_stock(stock_data):
    try:
        stock_entry = frappe.new_doc('Stock Entry')
        stock_entry.coach = stock_data['coach']
        stock_entry.data = frappe.utils.today()
        stock_entry.type_event = 'Breakfast'
        
        # Add stock quantities
        stock_entry.shake = stock_data['shake']
        stock_entry.tea = stock_data['tea']
        stock_entry.aloe = stock_data['aloe']
        stock_entry.pdm = stock_data['pdm']
        
        stock_entry.insert(ignore_permissions=True)
        
        return {
            "message": "Stock added successfully",
            "stock_entry": stock_entry.name,
        }
        
    except Exception as e:
        frappe.throw(f"Error adding stock: {str(e)}")

@frappe.whitelist()
def get_club_settings():
    club_settings = frappe.get_single('Settings')

    return club_settings

@frappe.whitelist()
def update_club_settings(new_settings):
    club_settings = frappe.get_single('Settings')
    club_settings.shake = new_settings['shake']
    club_settings.tea = new_settings['tea']
    club_settings.aloe = new_settings['aloe']
    club_settings.pdm = new_settings['pdm']
    club_settings.save(ignore_permissions=True)
    return club_settings

@frappe.whitelist()
def get_club_user():
    current_user = frappe.session.user
    user_doctype = frappe.get_doc('User', current_user)
    return user_doctype

@frappe.whitelist()
def change_club_password(new_password):
    current_user = frappe.session.user
    user_doctype = frappe.get_doc('User', current_user)
    user_doctype.new_password = new_password
    user_doctype.save(ignore_permissions=True)
    return user_doctype

@frappe.whitelist()
def get_visits_trend(month=None):
    try:
        current_user = frappe.session.user
        
        # Parse the month or use current month
        if month:
            # Ensure the month string is properly formatted
            selected_date = datetime.strptime(month + '-01', '%Y-%m-%d')
        else:
            selected_date = datetime.now()

        # Get first and last day of month
        first_day = selected_date.replace(day=1)
        last_day = selected_date.replace(day=calendar.monthrange(selected_date.year, selected_date.month)[1])
        
        # Format dates for query
        start_date = first_day.strftime('%Y-%m-%d')
        end_date = last_day.strftime('%Y-%m-%d')

        # Get all visits for the month
        visits = frappe.get_all('Visit',
            filters={
                'owner': current_user,
                'date': ['between', [start_date, end_date]]
            },
            fields=['date', 'name'],
            order_by='date'
        )

        # Create daily count
        days_in_month = calendar.monthrange(selected_date.year, selected_date.month)[1]
        daily_counts = [0] * days_in_month
        
        for visit in visits:
            visit_day = visit.date.day
            daily_counts[visit_day - 1] += 1
            
        return {
            'labels': list(range(1, days_in_month + 1)),  # [1, 2, 3, ..., 30/31]
            'values': daily_counts
        }
        
    except Exception as e:
        frappe.throw(f"Error getting visits trend: {str(e)}")

@frappe.whitelist()
def get_new_members_trend(month=None):
    try:
        current_user = frappe.session.user
        
        if month:
            selected_date = datetime.strptime(month + '-01', '%Y-%m-%d')
        else:
            selected_date = datetime.now()
            
        first_day = selected_date.replace(day=1)
        last_day = selected_date.replace(day=calendar.monthrange(selected_date.year, selected_date.month)[1])
        
        start_date = first_day.strftime('%Y-%m-%d')
        end_date = last_day.strftime('%Y-%m-%d')
        
        # Get all members created in this month
        members = frappe.get_all('Club Member',
            filters={
                'owner': current_user,
                'creation': ['between', [start_date, end_date]]
            },
            fields=['creation', 'name'],
            order_by='creation'
        )
        
        # Calculate weeks in month (always 5 to cover all cases)
        weeks = [0] * 5
        
        for member in members:
            creation_date = member.creation
            # Calculate which week of the month (0-based)
            week_number = (creation_date.day - 1) // 7
            if week_number < 5:  # Safety check
                weeks[week_number] += 1
            
        return {
            'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'values': weeks
        }
        
    except Exception as e:
        frappe.throw(f"Error getting new members trend: {str(e)}")

@frappe.whitelist()
def get_dashboard_statistics():
    try:
        current_user = frappe.session.user
        current_date = datetime.now()
        first_day = current_date.replace(day=1)
        
        # Get all members with status
        all_members = frappe.get_all('Club Member',
            filters={'owner': current_user},
            fields=['source', 'creation', 'status']
        )
        
        # Get active members count
        active_members = len([m for m in all_members if m.status == 'Active'])
        
        # Get total coaches
        total_coaches = frappe.db.count('Coach', {'owner': current_user})
        
        # Get all visits
        all_visits = frappe.get_all('Visit',
            filters={'owner': current_user},
            fields=['date']
        )
        
        # Get visits this month
        visits_this_month = frappe.get_all('Visit',
            filters={
                'owner': current_user,
                'date': ['>=', first_day.strftime('%Y-%m-%d')]
            }
        )
        
        # Initialize source counts
        sources = {
            'Facebook': {'total': 0, 'thisMonth': 0},
            'Instagram': {'total': 0, 'thisMonth': 0},
            'Referral': {'total': 0, 'thisMonth': 0},
            'Active Contact': {'total': 0, 'thisMonth': 0},
            'Roadshow': {'total': 0, 'thisMonth': 0}
        }
        
        # Count members by source
        for member in all_members:
            source = member.source
            if source in sources:
                sources[source]['total'] += 1
                if member.creation.date() >= first_day.date():
                    sources[source]['thisMonth'] += 1
        
        return {
            'totalMembers': len(all_members),
            'activeMembers': active_members,
            'totalCoaches': total_coaches,
            'totalVisits': len(all_visits),
            'visitsThisMonth': len(visits_this_month),
            'memberSources': sources
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting dashboard statistics: {str(e)}")
        return {}

@frappe.whitelist()
def promote_to_coach(member_data):
    try:
        member = frappe.get_doc('Club Member', member_data.get('name'))
        
        def get_all_related_members(member_id, processed=None):
            if processed is None:
                processed = set()
            
            if member_id in processed:
                return []
                
            processed.add(member_id)
            members = [member_id]
            
            # Get direct referrals
            referrals = frappe.get_all('Club Member',
                filters={'referral_of': member_id},
                fields=['name']
            )
            
            # Recursively get all referrals' referrals
            for referral in referrals:
                members.extend(get_all_related_members(referral.name, processed))
                
            return members

        # Get all related members including nested referrals
        all_related_members = get_all_related_members(member.name)
        
        # Store referral relationships and their hierarchy
        referral_hierarchy = {}
        for member_id in all_related_members:
            member_doc = frappe.get_doc('Club Member', member_id)
            referral_hierarchy[member_id] = {
                'member': member_id,
                'referral_of': member_doc.referral_of,
                'coach': member_doc.coach,
                'original_referrer': member_doc.referral_of
            }

        # Store all visits
        all_visits = []
        for member_id in all_related_members:
            member_visits = frappe.get_all('Visit',
                filters={'club_member': member_id},
                fields=['club_member', 'date', 'type_event']
            )
            all_visits.extend(member_visits)

        # Delete all visits
        frappe.db.sql("""
            DELETE FROM `tabVisit`
            WHERE club_member IN %(members)s
        """, {'members': all_related_members})
        frappe.db.commit()

        # Temporarily remove referral connections
        frappe.db.sql("""
            UPDATE `tabClub Member` 
            SET referral_of = NULL 
            WHERE referral_of IN %(members)s
        """, {'members': all_related_members})
        frappe.db.commit()

        # Create new coach
        new_coach = frappe.new_doc('Coach')
        new_coach.first_name = member.first_name
        new_coach.last_name = member.last_name
        new_coach.full_name = member.full_name
        new_coach.id_herbalife = member_data['id_herbalife']
        new_coach.email = member_data['email']
        new_coach.phone_number = member_data['phone_number']
        new_coach.sponsor = member_data['coach']
        new_coach.level = 'SV'
        new_coach.role = 'Junior Partner'
        new_coach.insert(ignore_permissions=True)

        # Delete the original member
        member.delete(ignore_permissions=True)
        frappe.db.commit()

        # Restore referral relationships maintaining the hierarchy
        for member_id, rel_data in referral_hierarchy.items():
            if member_id != member.name:  # Skip the promoted member
                member_doc = frappe.get_doc('Club Member', member_id)
                member_doc.coach = new_coach.id_herbalife
                
                # If this member was referring to the promoted member,
                # remove the referral connection
                if rel_data['referral_of'] == member.name:
                    member_doc.referral_of = None
                else:
                    # Otherwise keep the original referral relationship
                    member_doc.referral_of = rel_data['original_referrer']
                
                member_doc.save(ignore_permissions=True)

        # Restore all visits
        for visit in all_visits:
            new_visit = frappe.new_doc('Visit')
            new_visit.club_member = visit.club_member
            new_visit.date = visit.date
            new_visit.type_event = visit.type_event
            new_visit.insert(ignore_permissions=True)

        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Successfully promoted to coach",
            "coach": new_coach.id_herbalife,
            "visits_restored": len(all_visits),
            "relationships_maintained": len(referral_hierarchy) - 1
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error promoting member to coach: {str(e)}")
        frappe.throw(f"Error promoting member to coach: {str(e)}")

@frappe.whitelist()
def get_network_hierarchy():
    try:
        current_user = frappe.session.user
        
        def get_member_tree(member_id, processed_members=None):
            if processed_members is None:
                processed_members = set()
                
            if member_id in processed_members:
                return None
                
            processed_members.add(member_id)
            
            member = frappe.get_doc('Club Member', member_id)
            referrals = frappe.get_all('Club Member',
                filters={
                    'owner': current_user,
                    'referral_of': member_id
                },
                fields=['name', 'full_name', 'creation', 'status', 'referrals']
            )
            
            children = []
            for referral in referrals:
                child = get_member_tree(referral.name, processed_members)
                if child:
                    children.append(child)
            
            return {
                'id': member.name,
                'name': member.full_name,
                'type': 'member',
                'date': member.creation,
                'status': member.status,
                'direct_count': len(referrals),
                'total_count': len(referrals) + sum(c['total_count'] for c in children),
                'children': children
            }

        # Get coaches with their direct members
        coaches = frappe.get_all('Coach',
            filters={'owner': current_user},
            fields=['id_herbalife', 'full_name', 'level', 'role']
        )

        network = []
        processed_members = set()
        
        for coach in coaches:
            # Get direct members for this coach
            members = frappe.get_all('Club Member',
                filters={
                    'owner': current_user,
                    'coach': coach.id_herbalife,
                    'referral_of': ''  # Only get direct members
                },
                fields=['name', 'full_name', 'creation', 'status']
            )

            children = []
            total_network = 0
            
            for member in members:
                member_tree = get_member_tree(member.name, processed_members)
                if member_tree:
                    children.append(member_tree)
                    total_network += 1 + member_tree['total_count']

            coach_data = {
                'id': coach.id_herbalife,
                'name': coach.full_name,
                'type': 'coach',
                'level': coach.level,
                'role': coach.role,
                'direct_count': len(members),
                'total_count': total_network,
                'children': children
            }
            network.append(coach_data)

        return network

    except Exception as e:
        frappe.log_error(f"Error getting network hierarchy: {str(e)}")
        return []

