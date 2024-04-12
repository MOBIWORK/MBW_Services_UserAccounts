import json
import frappe
from frappe import _
from frappe.auth import LoginManager

from datetime import datetime
from mbw_account_service.api.common import (
    gen_response,
    generate_key,
    get_employee_by_user,
    get_language,
    exception_handel
)
from mbw_account_service.config_translate import i18n

def add_device_notification(user_id, device_name=None, device_id=None):
    try:
        if user_id and device_name and device_id:
            name_doc = frappe.db.get_value(
                'User Device', {"device_id": device_id}, ['name'])
            if not name_doc:
                name_doc = frappe.db.get_value(
                    'User Device', {"user": user_id, "device_name": device_name}, ['name'])

            if name_doc:
                update_doc = frappe.get_doc('User Device', name_doc)
                update_doc.user = user_id
                update_doc.device_name = device_name
                update_doc.device_id = device_id
                update_doc.save(ignore_permissions=True)
            else:
                new_doc = frappe.new_doc('User Device')
                new_doc.user = user_id
                new_doc.device_name = device_name
                new_doc.device_id = device_id
                new_doc.insert(ignore_permissions=True)
        return False
    except Exception as e:
        print('===login', e)
        return False
    
def remove_device_notification(user_id, device_id):
    try:
        if user_id and device_id:
            frappe.db.delete("User Device", {
                "user": user_id,
                "device_id": device_id
            })
            frappe.db.commit()
        return True
    except Exception as e:
        return False


def validate_employee(user):
    if not frappe.db.exists("Employee", dict(user_id=user)):
        frappe.response["message"] = "Please link Employee with this user"
        raise frappe.AuthenticationError(frappe.response["message"])

@frappe.whitelist(allow_guest=True, methods='POST')
def login(**kwargs):
    try:
        usr = kwargs.get('usr')
        pwd = kwargs.get('pwd')
        device_name = kwargs.get('device_name')
        device_id = kwargs.get('device_id')

        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        # validate_employee(login_manager.user)
        login_manager.post_login()

        if frappe.response["message"] == "Logged In":
            emp_data = get_employee_by_user(login_manager.user, fields=[
                                            "name", "employee_name"])
            # print("emp_data", emp_data)
            frappe.response['message'] = ""
            del frappe.local.response["full_name"]
            del frappe.local.response["home_page"]

        # them thiet bi nhan thong bao
        add_device = add_device_notification(
            login_manager.user, device_name, device_id)

        gen_response(200, "Thành công", {
            "key_details": generate_key(login_manager.user),
        })

    except frappe.AuthenticationError as fa:
        # gen_response(404, "Thất bại", [])
        exception_handel(fa)
        return None
    except Exception as e:
        exception_handel(e)

def validate_employee(user):
    if not frappe.db.exists("Employee", dict(user_id=user)):
        frappe.response["message"] = "Please link Employee with this user"
        raise frappe.AuthenticationError(frappe.response["message"])
    
#Logout
@frappe.whitelist(allow_guest=True)
def logout(device_id=None):
    try:
        auth_manager = LoginManager()
        remove_device_notification(auth_manager.user, device_id)
        auth_manager.logout()
        frappe.response["message"] = "Logged Out"
        gen_response(200, "Đẵng xuất thành công")
    except frappe.AuthenticationError:
        # gen_response(204, i18n.t('translate.logout_error', locale=get_language()), [])
        exception_handel(e)
        return None
    except Exception as e:
        exception_handel(e)
        # gen_response(500, e, [])

#reset password
@frappe.whitelist(allow_guest=True)
def reset_password(user):
    if user == "Administrator":
        gen_response(500, "Không có sẵn", [])

    try:
        user = frappe.get_doc("User", user)
        if not user.enabled:
            gen_response(500, "Gửi email thất bại", [])

        user.validate_reset_password()
        user.reset_password(send_email=True)

        gen_response(200, "Gửi email thành công")
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        del frappe.response["exc_type"]
        gen_response(404, "Người dùng không có", [])
        return