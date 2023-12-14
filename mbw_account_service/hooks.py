from . import __version__ as app_version

app_name = "mbw_account_service"
app_title = "MBW Account"
app_publisher = "MBW"
app_description = "api mbw account"
app_email = "dev@mbw.vn"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mbw_account_service/css/mbw_account_service.css"
# app_include_js = "/assets/mbw_account_service/js/mbw_account_service.js"

# include js, css files in header of web template
# web_include_css = "/assets/mbw_account_service/css/mbw_account_service.css"
# web_include_js = "/assets/mbw_account_service/js/mbw_account_service.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mbw_account_service/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "mbw_account_service.utils.jinja_methods",
#	"filters": "mbw_account_service.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mbw_account_service.install.before_install"
# after_install = "mbw_account_service.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mbw_account_service.uninstall.before_uninstall"
# after_uninstall = "mbw_account_service.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mbw_account_service.utils.before_app_install"
# after_app_install = "mbw_account_service.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mbw_account_service.utils.before_app_uninstall"
# after_app_uninstall = "mbw_account_service.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mbw_account_service.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"mbw_account_service.tasks.all"
#	],
#	"daily": [
#		"mbw_account_service.tasks.daily"
#	],
#	"hourly": [
#		"mbw_account_service.tasks.hourly"
#	],
#	"weekly": [
#		"mbw_account_service.tasks.weekly"
#	],
#	"monthly": [
#		"mbw_account_service.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "mbw_account_service.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "mbw_account_service.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "mbw_account_service.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mbw_account_service.utils.before_request"]
# after_request = ["mbw_account_service.utils.after_request"]

# Job Events
# ----------
# before_job = ["mbw_account_service.utils.before_job"]
# after_job = ["mbw_account_service.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"mbw_account_service.auth.validate"
# ]
