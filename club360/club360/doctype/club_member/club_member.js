// Copyright (c) 2025, pauldamsa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Club Member", {
    // ...existing code...
});

frappe.ui.form.on("Membership", {
    type: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.type) return;
        
        if (row.type === "10 visits") {
            frappe.model.set_value(cdt, cdn, 'remaining_visits', 10);
            let end_date = frappe.datetime.add_months(frappe.datetime.get_today(), 1);
            frappe.model.set_value(cdt, cdn, 'end_date', end_date);
        } 
        else if (row.type === "30 visits") {
            frappe.model.set_value(cdt, cdn, 'remaining_visits', 30);
            let end_date = frappe.datetime.add_months(frappe.datetime.get_today(), 3);
            frappe.model.set_value(cdt, cdn, 'end_date', end_date);
        }
    }
});
