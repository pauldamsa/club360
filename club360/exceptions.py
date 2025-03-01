from frappe.exceptions import ValidationError

class NoValidMembershipError(ValidationError):
    """Raised when a member has no valid membership"""
    pass

class NoServingsAvailableError(ValidationError):
    """Raised when a coach has no servings available for an event type"""
    pass
