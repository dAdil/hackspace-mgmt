from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import request
from hackspace_mgmt.models import db, Member, Card

member_columns = (
    "first_name",
    "last_name",
    "preferred_name",
    "email",
    "alt_email",
    "join_date",
    "discourse",
    "mailchimp",
    "payment_ref",
    "payment_active",
    "address1",
    "address2",
    "town_city",
    "county",
    "postcode",
    "end_date",
    "end_reason",
    "notes",
)

class MemberView(ModelView):
    can_view_details = True
    can_export = True
    column_list = member_columns
    form_columns = member_columns
    column_filters = member_columns
    column_searchable_list = (
        'first_name',
        'last_name',
        'preferred_name',
        'email',
        'alt_email'
    )
    inline_models = (Card,)

    column_labels = {
        'preferred_name': "Preferred full name (including surname)",
        'discourse': "Discourse invite status"
    }

    column_descriptions = {
        'preferred_name': (
            "This must include the surname unless the member uses a mononym." +
            " Leave blank if not needed."
        )
    }

    form_widget_args = {
        "preferred_name": {
            "placeholder": "(optional)"
        }
    }

    def search_placeholder(self):
        return "Member name or email"

    def is_accessible(self):
        return request.headers.get("X-Remote-User") == "admin"

def create_views(admin: Admin):
    admin.add_view(MemberView(Member, db.session, category="Access Control"))
