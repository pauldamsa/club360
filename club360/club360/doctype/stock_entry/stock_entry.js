// Copyright (c) 2025, pauldamsa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Entry", {
    refresh(frm) {
        if (!frm.doc.data) {
            frm.set_value('data', frappe.datetime.get_today());
        }
    },
    
    before_load(frm) {
        if (!frm.doc.data) {
            frm.set_value('data', frappe.datetime.get_today());
        }
    }
});
