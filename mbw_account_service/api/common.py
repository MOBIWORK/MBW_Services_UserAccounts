from math import sin, cos, sqrt, atan2
import json
import frappe
from bs4 import BeautifulSoup
from frappe import _
from frappe.utils import cstr
import urllib.parse
import http.cookies
from datetime import datetime, timedelta
import base64
from frappe.core.doctype.file.utils import delete_file
from frappe.utils.file_manager import (
    save_file
)
from frappe.desk.query_report import (
    normalize_result, get_report_result, get_reference_report)
from frappe.core.utils import ljust_list
from pypika import Query, Table, Field, Order
import array
from frappe.client import validate_link

BASE_URL = frappe.utils.get_request_site_address()

ShiftType = frappe.qb.DocType('Shift Type')
ShiftAssignment = frappe.qb.DocType('Shift Assignment')
EmployeeCheckin = frappe.qb.DocType("Employee Checkin")

# return definition 1004 1225
def gen_response(status, message, result=[]):
    frappe.response["http_status_code"] = status
    if status == 500:
        frappe.response["message"] = BeautifulSoup(
            str(message), features="lxml").get_text()
    else:
        frappe.response["message"] = message
    frappe.response["result"] = result

# export employee key
def generate_key(user):
    user_details = frappe.get_doc("User", user)
    dms_settings = frappe.get_doc("DMS Settings").as_dict()
    api_secret = api_key = ""
    if not user_details.api_key and not user_details.api_secret:
        api_secret = frappe.generate_hash(length=15)
        # if api key is not set generate api key
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
        user_details.api_secret = api_secret
        user_details.save(ignore_permissions=True)
    else:
        api_secret = user_details.get_password("api_secret")
        api_key = user_details.get("api_key")
    object_id = ''
    if frappe.db.exists("Employee", {"user_id": user_details.get('name')}):
        employee = frappe.get_doc("Employee", {"user_id": user_details.get('name')}).as_dict()
        object_id = employee.get('object_id')
    return {"api_key": api_key, "api_secret": api_secret, "project_id": dms_settings.ma_du_an, "object_id": object_id}


def get_employee_by_user(user, fields=["name"]):
    if isinstance(fields, str):
        fields = [fields]
    emp_data = frappe.db.get_value(
        "Employee",
        {"user_id": user},
        fields,
        as_dict=1,
    )
    return emp_data


def get_language():
    lang_ = frappe.local.request.headers.get("Language")
    lang = "vi" if not lang_ else lang_

    return lang

def exception_handel(e):
    frappe.log_error(title="DMS Mobile App Error",
                     message=frappe.get_traceback())
    return gen_response(406, cstr(e))
    
    if hasattr(e, "http_status_code"):
        return gen_response(e.http_status_code, cstr(e))
    else:
        return gen_response(406, cstr(e))

def get_user_id():
    headers = frappe.local.request.headers.get("Authorization")
    usrPass = headers.split(" ")[1]
    str_b64Val = base64.b64decode(usrPass).decode('utf-8')
    list_key = str_b64Val.split(':')
    api_key = list_key[0]
    user_id = frappe.db.get_value('User', {"api_key": api_key})
    return user_id

def get_employee_id():
    try:
        user_id = get_user_id()
        return get_employee_by_user(user_id).get("name")
    except:
        return ""
    
def get_info_employee(name, fields=['*']):
    info = frappe.db.get_value("Employee", name, fields, as_dict=1)
    # shift_type_now = get_shift_type_now(info.get('employee'))
    # info['shift'] = shift_type_now
    return info

def post_image(name_image, faceimage, doc_type, doc_name):
    # save file and insert Doctype File
    file_name = name_image + "_" + str(datetime.now()) + "_.png"
    imgdata = base64.b64decode(faceimage)

    doc_file = save_file(file_name, imgdata, doc_type, doc_name,
                         folder=None, decode=False, is_private=0, df=None)

    # delete image copy
    path_file = "/files/" + file_name
    delete_file(path_file)
    file_url = BASE_URL + doc_file.get('file_url')
    return file_url

def validate_image(user_image):
    if user_image and "http" not in user_image:
        user_image = BASE_URL + user_image
    return user_image


def get_shift_type_now(employee_name):
    time_now = datetime.now()

    shift_type_now = today_list_shift(employee_name, time_now)
    shift_status = "Bạn không có ca hôm nay"
    time_query = time_now.replace(hour=0, minute=0, second=0)
    time_query_next_day =  time_now.replace(hour=23, minute=59, second=59)
    if len(shift_type_now) > 0:
        last_checkin_today = (frappe.qb.from_(EmployeeCheckin)
                              .limit(4)
                              .where((EmployeeCheckin.time >= time_query) & (EmployeeCheckin.time <= time_query_next_day))
                              .orderby(EmployeeCheckin.time,order= Order.desc)
                              .select('*')
                              .run(as_dict=True))
        if not last_checkin_today:
            shift_type_now = shift_now(employee_name, time_now)
            shift_status = False
        elif last_checkin_today[0].get("log_type") == "OUT":
            shift_type_now = nextshift(employee_name, time_now)
            shift_status = False
        else:
            shift_type_now = frappe.db.get_value('Shift Type', {"name": last_checkin_today[0].get(
                "shift")}, ["name", "start_time", "end_time","allow_check_out_after_shift_end_time", "begin_check_in_before_shift_start_time"], as_dict=1)
            shift_status = last_checkin_today[0].get("log_type")
            pass

    else:
        shift_type_now = False
    return {
        "shift_type_now": shift_type_now,
        "shift_status": shift_status
    }

def today_list_shift(employee_name, time_now):
    query = (ShiftAssignment.employee == employee_name) & (time_now.date() >= ShiftAssignment.start_date)
    if not ShiftAssignment.end_date.isnull() :
        query = (ShiftAssignment.employee == employee_name) & (time_now.date() >= ShiftAssignment.start_date) & (time_now.date() <= ShiftAssignment.end_date)
    data =  (frappe.qb.from_(ShiftType)
            .inner_join(ShiftAssignment)
            .on(ShiftType.name == ShiftAssignment.shift_type)
            .where(
                (ShiftAssignment.employee == employee_name) & 
                            (ShiftAssignment.status == "Active") & 
                            (ShiftAssignment.docstatus == 1) 
            )
            .select(ShiftAssignment.start_date,ShiftAssignment.end_date,ShiftAssignment.employee, ShiftType.name, ShiftType.start_time, ShiftType.end_time, ShiftType.allow_check_out_after_shift_end_time, ShiftType.begin_check_in_before_shift_start_time)
            .run(as_dict=True)
            )
    data_rs = []
    for shift in data:
            if not shift.get("end_date") and not shift.get('start_date'):
                data_rs.append( shift)
            elif not shift.get("end_date") and  shift.get('start_date') :
                if shift.get("start_date") <= time_now.date() :
                    data_rs.append( shift)
            elif  shift.get("end_date") and not shift.get('start_date') :
                if shift.get("end_date") >= time_now.date() :
                    data_rs.append( shift)
            else :
                if shift.get("end_date") >= time_now.date()  and shift.get("start_date") <= time_now.date() :
                    data_rs.append( shift)
    return data_rs

def shift_now(employee_name, time_now):
    in_shift = inshift(employee_name, time_now)

    if not in_shift:
        next_shift = nextshift(employee_name, time_now)
        if not next_shift:
            return False
        return next_shift
    return in_shift


def inshift(employee_name,time_now) :
    data = (frappe.qb.from_(ShiftType)
                      .inner_join(ShiftAssignment)
                      .on(ShiftType.name == ShiftAssignment.shift_type)
                      .where(
                          (ShiftAssignment.employee == employee_name) & 
                          (ShiftAssignment.status == "Active") & 
                          (ShiftAssignment.docstatus == 1) & 
                          (time_now.time() >= ShiftType.start_time) & 
                          (time_now.time() <= ShiftType.end_time) 
                             )
                      .select(ShiftAssignment.end_date,ShiftAssignment.start_date,ShiftType.name, ShiftType.start_time, ShiftType.end_time, ShiftType.allow_check_out_after_shift_end_time, ShiftType.begin_check_in_before_shift_start_time)
                      .run(as_dict=True)
                )
    if len(data) == 0:
        return False    
    for shift in data:
        if not shift.get("end_date") and not shift.get('start_date'):
            return shift
        elif not shift.get("end_date") and  shift.get('start_date') :
            if shift.get("start_date") <= time_now.date() :
                return shift
        elif  shift.get("end_date") and not shift.get('start_date') :
            if shift.get("end_date") >= time_now.date() :
                return shift
        else :
            if shift.get("end_date") >= time_now.date()  and shift.get("start_date") <= time_now.date() :
                return shift

# next shift
def nextshift(employee_name,time_now) :
    data = (frappe.qb.from_(ShiftType)
                        .inner_join(ShiftAssignment)
                        .on(ShiftType.name == ShiftAssignment.shift_type)
                        .where(
                            (ShiftAssignment.employee == employee_name) & 
                            (ShiftAssignment.status == "Active") & 
                            (ShiftAssignment.docstatus == 1) 
                            & (time_now.time() <= ShiftType.start_time) 
                            )
                        .orderby(ShiftType.start_time,order= Order.asc)
                        .select(ShiftAssignment.end_date,ShiftAssignment.start_date,ShiftType.name, ShiftType.start_time, ShiftType.end_time, ShiftType.allow_check_out_after_shift_end_time, ShiftType.begin_check_in_before_shift_start_time)
                        .run(as_dict=True)
                        )
    if len(data) == 0:
        return False
    for shift in data:
        if not shift.get("end_date") and not shift.get('start_date'):
            return shift
        elif not shift.get("end_date") and  shift.get('start_date') :
            if shift.get("start_date") <= time_now.date() :
                return shift
        elif  shift.get("end_date") and not shift.get('start_date') :
            if shift.get("end_date") >= time_now.date() :
                return shift
        else :
            if shift.get("end_date") >= time_now.date()  and shift.get("start_date") <= time_now.date() :
                return shift
    return False