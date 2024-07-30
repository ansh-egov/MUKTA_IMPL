import csv
import pandas as pd
from numpy import *
import requests
import json
from dateutil import parser
import datetime as dt
import psycopg2
import logging
import calendar
import time
import os
import pytz
import pytz
from datetime import datetime
import re
from dotenv import load_dotenv

load_dotenv('.env')

MUKTA_ADAPTER_HOST = os.getenv('MUKTA_ADAPTER_HOST')
EXPENSE_HOST = os.getenv('EXPENSE_HOST')
MUSTER_HOST = os.getenv('MUSTER_HOST')
PROJECT_HOST = os.getenv('PROJECT_HOST')
CONTRACT_HOST = os.getenv('CONTRACT_HOST')
INDIVIDUAL_HOST = os.getenv('INDIVIDUAL_HOST')
USER_HOST = os.getenv('USER_HOST')
WORKFLOW_HOST = os.getenv('WORKFLOW_HOST')
ESTIMATE_HOST = os.getenv('ESTIMATE_HOST')


tenantids = [
    "od.jatni"
    # "od.dhenkanal"
    # "od.balangir"
    # "od.balasore"
    # "od.padampur",
    # "od.bhadrak",
    # "od.boudhgarh",
    # "od.cuttack",
    # "od.athagarh",
    # "od.berhampur",
    # "od.hinjilicut",
    # "od.chatrapur",
    # "od.paradeep",
    # "od.jajpur",
    # "od.jharsuguda",
    # "od.kesinga",
    # "od.phulbani",
    # "od.keonjhargarh",
    # "od.jeypore",
    # "od.kotpad",
    # "od.baripada",
    # "od.puri",
    # "od.sambalpur",
    # "od.rourkela",
    # "od.bhubaneswar"
]



def convert_epoch_to_indian_time(epoch_time):
    # Convert epoch time to seconds
    epoch_time_seconds = epoch_time / 1000
    
    # Define the timezone for India
    india_tz = pytz.timezone('Asia/Kolkata')
    
    # Convert epoch time to datetime object
    dt = datetime.fromtimestamp(epoch_time_seconds, tz=india_tz)
    
    # Format the datetime object to "dd-mm-yyyy"
    formatted_time = dt.strftime('%d-%m-%Y')
    
    return formatted_time

def format_tenant_id(tenant_id):
    # Extract the relevant part of the tenant ID and capitalize it
    return tenant_id.split('.')[1].capitalize()

def getWorkflowDates(bussinessId, tenantId):
    data = {}
    try:
        host = WORKFLOW_HOST + os.getenv('PROCESS_INSTANCE_SEARCH') +"?tenantId="+tenantId+"&businessIds="+ bussinessId +"&history=true"
        request_payload = {"RequestInfo": {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11","userName": "MUKTAUAT","name": "MUKTAUAT","mobileNumber": "9036774122","emailId": None,"locale": None,"type": "EMPLOYEE","roles": [{"name": "ESTIMATE APPROVER","code": "ESTIMATE_APPROVER","tenantId": "od.testing"},{"name": "WORK ORDER CREATOR","code": "WORK_ORDER_CREATOR","tenantId": "od.testing"},{"name": "Organization viewer","code": "ORG_VIEWER","tenantId": "od.testing"},{"name": "MB_VERIFIER","code": "MB_VERIFIER","tenantId": "od.testing"},{"name": "ESTIMATE CREATOR","code": "ESTIMATE_CREATOR","tenantId": "od.testing"},{"name": "MDMS Admin","code": "MDMS_ADMIN","tenantId": "od.testing"},{"name": "MB_VIEWER","code": "MB_VIEWER","tenantId": "od.testing"},{"name": "State Dashboard Admin","code": "STADMIN","tenantId": "od.testing"},{"name": "MUKTA Admin","code": "MUKTA_ADMIN","tenantId": "od.testing"},{"name": "Employee Common","code": "EMPLOYEE_COMMON","tenantId": "od.testing"},{"name": "TECHNICAL SANCTIONER","code": "TECHNICAL_SANCTIONER","tenantId": "od.testing"},{"name": "BILL_CREATOR","code": "BILL_CREATOR","tenantId": "od.testing"},{"name": "BILL_ACCOUNTANT","code": "BILL_ACCOUNTANT","tenantId": "od.testing"},{"name": "WORK_ORDER_VIEWER","code": "WORK_ORDER_VIEWER","tenantId": "od.testing"},{"name": "BILL_VERIFIER","code": "BILL_VERIFIER","tenantId": "od.testing"},{"name": "ESTIMATE VERIFIER","code": "ESTIMATE_VERIFIER","tenantId": "od.testing"},{"name": "MUSTER ROLL APPROVER","code": "MUSTER_ROLL_APPROVER","tenantId": "od.testing"},{"name": "ESTIMATE VIEWER","code": "ESTIMATE_VIEWER","tenantId": "od.testing"},{"name": "WORK ORDER APPROVER","code": "WORK_ORDER_APPROVER","tenantId": "od.testing"},{"name": "MB_APPROVER","code": "MB_APPROVER","tenantId": "od.testing"},{"name": "MDMS CITY ADMIN","code": "MDMS_CITY_ADMIN","tenantId": "od.testing"},{"name": "OFFICER IN CHARGE","code": "OFFICER_IN_CHARGE","tenantId": "od.testing"},{"name": "PROJECT CREATOR","code": "PROJECT_CREATOR","tenantId": "od.testing"},{"name": "BILL_VIEWER","code": "BILL_VIEWER","tenantId": "od.testing"},{"name": "WORK ORDER VERIFIER","code": "WORK_ORDER_VERIFIER","tenantId": "od.testing"},{"name": "PROJECT VIEWER","code": "PROJECT_VIEWER","tenantId": "od.testing"},{"name": "BILL_APPROVER","code": "BILL_APPROVER","tenantId": "od.testing"},{"name": "MB_CREATOR","code": "MB_CREATOR","tenantId": "od.testing"},{"name": "MUSTER ROLL VERIFIER","code": "MUSTER_ROLL_VERIFIER","tenantId": "od.testing"},{"name": "HRMS Admin","code": "HRMS_ADMIN","tenantId": "od.testing"}],"active": True,"tenantId": "od.testing","permanentCity": "Testing"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}}
        headers = {"Content-Type": "application/json"}
        response = requests.post(host,headers=headers,data=json.dumps(request_payload))
        countOfSendBacks = 0
        data["sendBacks"] = 0
        if response and response.status_code and response.status_code in [200, 202]:
            response = response.json()
            if response and response['ProcessInstances'] and len(response['ProcessInstances'])>0:
                for processInstance in response['ProcessInstances']:
                    if processInstance['action'] == "ACCEPT":
                        data['acceptDate'] = processInstance['auditDetails']['createdTime']
                    elif processInstance['action'] == "APPROVE":
                        data['approveDate'] = processInstance['auditDetails']['createdTime']
                    elif processInstance['action'] == "VERIFY_AND_FORWARD":
                        data['verifyDate'] = processInstance['auditDetails']['createdTime']
                    elif processInstance['action'] == "SENDBACK":
                        countOfSendBacks = countOfSendBacks + 1
                        data['sendBacks'] = countOfSendBacks
            
        return data
    except Exception as e:  
        raise e


def getWorkOrderData():
    data = []
    print("Getting WorkOrder Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            host = CONTRACT_HOST + os.getenv('CONTRACT_SEARCH')
            request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
            headers = {"Content-Type": "application/json"}
            api_limit = 100
            api_offset = 0
            while True:
                api_payload = {"tenantId": tenantid,"pagination": {"limit": api_limit,"offSet": api_offset},"RequestInfo": request_payload}
                response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                api_offset = api_offset + api_limit
                if response and response.status_code and response.status_code in [200, 202]:
                    response = response.json()
                    if response and response['contracts'] and len(response['contracts'])>0:
                        for contract in response['contracts']:
                            if contract['status'] == "ACTIVE":
                                print("Contract Number: " + contract['contractNumber'])
                                temp = {}
                                workflowDates = getWorkflowDates(contract['contractNumber'], tenantid)
                                temp['ULB Name'] = format_tenant_id(tenantid)
                                temp['Project ID'] = contract['additionalDetails']['projectId']
                                temp['CBO Name'] = contract['additionalDetails']['cboName']
                                temp['Work Order Creation Date'] = convert_epoch_to_indian_time(contract['auditDetails']['createdTime'])
                                temp['Work Order ID'] = contract['contractNumber']
                                temp['Work order Verification Date'] = convert_epoch_to_indian_time(workflowDates['verifyDate'])
                                temp['Work order Approval Date'] = convert_epoch_to_indian_time(workflowDates['approveDate'])
                                temp['Work Order Acceptance Date'] = convert_epoch_to_indian_time(workflowDates['acceptDate'])
                                temp['Value Of Work Order'] = contract['totalContractedAmount']
                                temp['Workflow Status'] = contract['wfStatus']
                                temp['Last Modified Date'] = convert_epoch_to_indian_time(contract['auditDetails']['lastModifiedTime'])
                                data.append(temp)
                            else:
                                continue
                    else:
                        break
                else:
                    break
        return data
    except Exception as e:
        raise e


def getProjectData():
    data = []
    print("Getting Project Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            api_limit = 100
            api_offset = 0
            while True:
                host = PROJECT_HOST + os.getenv('PROJECT_SEARCH') + "?tenantId=" + tenantid + "&limit=" + str(api_limit) + "&offset=" + str(api_offset) + "&createdFrom=1680307200000"  # "&limit=1000&offset=0&createdFrom=1680307200000" 
                request_payload = {"apiId": "Rainmaker", "authToken": "e091dbec-959c-4268-ad07-ff6c8793a61a", "userInfo": {"id": 4747, "uuid": "71d23f7e-30c9-4ba4-b81b-e1862cd3fd9d", "userName": "SUPERUSERA", "name": "SUPERUSERA", "mobileNumber": "9000000006", "type": "EMPLOYEE", "roles": [{"name": "BILL_ACCOUNTANT", "code": "BILL_ACCOUNTANT", "tenantId": "pg.citya"}, {"name": "WORK ORDER VIEWER", "code": "WORK_ORDER_VIEWER", "tenantId": "pg.citya"}, {"name": "BILL_VERIFIER", "code": "BILL_VERIFIER", "tenantId": "pg.citya"}, {"name": "ESTIMATE VERIFIER", "code": "ESTIMATE_VERIFIER", "tenantId": "pg.citya"}, {"name": "OFFICER IN CHARGE", "code": "OFFICER_IN_CHARGE", "tenantId": "pg.citya"}, {"name": "PROJECT CREATOR", "code": "PROJECT_CREATOR", "tenantId": "pg.citya"}, {"name": "BILL_CREATOR", "code": "BILL_CREATOR", "tenantId": "pg.citya"}, {"name": "ESTIMATE VIEWER", "code": "ESTIMATE_VIEWER", "tenantId": "pg.citya"}, {"name": "MB_APPROVER", "code": "MB_APPROVER", "tenantId": "pg.citya"}, {"name": "MUKTA Admin", "code": "MUKTA_ADMIN", "tenantId": "pg.citya"}, {"name": "WORK ORDER CREATOR", "code": "WORK_ORDER_CREATOR", "tenantId": "pg.citya"}, {"name": "ESTIMATE APPROVER", "code": "ESTIMATE_APPROVER", "tenantId": "pg.citya"}, {"name": "MB_VERIFIER", "code": "MB_VERIFIER", "tenantId": "pg.citya"}, {"name": "WORK ORDER VERIFIER", "code": "WORK_ORDER_VERIFIER", "tenantId": "pg.citya"}, {"name": "MB_CREATOR", "code": "MB_CREATOR", "tenantId": "pg.citya"}, {"name": "PROJECT VIEWER", "code": "PROJECT_VIEWER", "tenantId": "pg.citya"}, {"name": "BILL_APPROVER", "code": "BILL_APPROVER", "tenantId": "pg.citya"}, {"name": "MUSTER ROLL VERIFIER", "code": "MUSTER_ROLL_VERIFIER", "tenantId": "pg.citya"}, {"name": "Employee Common", "code": "EMPLOYEE_COMMON", "tenantId": "pg.citya"}, {"name": "BILL_VIEWER", "code": "BILL_VIEWER", "tenantId": "pg.citya"}, {"name": "TECHNICAL SANCTIONER", "code": "TECHNICAL_SANCTIONER", "tenantId": "pg.citya"}, {"name": "MUSTER ROLL APPROVER", "code": "MUSTER_ROLL_APPROVER", "tenantId": "pg.citya"}, {"name": "WORK ORDER APPROVER", "code": "WORK_ORDER_APPROVER", "tenantId": "pg.citya"}, {"name": "ESTIMATE CREATOR", "code": "ESTIMATE_CREATOR", "tenantId": "pg.citya"}, {"name": "MB_VIEWER", "code": "MB_VIEWER", "tenantId": "pg.citya"}, {"name": "State Dashboard Admin", "code": "STADMIN", "tenantId": "pg.citya"}, {"name": "SUPER USER", "code": "SUPERUSER", "tenantId": "pg.citya"}], "tenantId": "pg.citya",}, "msgId": "1712148865295|en_IN", "plainAccessRequest": {}}
                headers = {"Content-Type": "application/json"}
                api_payload = {"Projects": [{"tenantId": tenantid,"createdFrom": 1680307200000}],"pagination": {"limit": api_limit,"offSet": api_offset},"RequestInfo": request_payload}
                response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                api_offset = api_offset + api_limit
                if response.status_code in [200, 202]:
                    response = response.json()
                    if response and response["Project"] and len(response["Project"])>0:
                        for project in response["Project"]: 
                            print("Project Number: " + project['projectNumber'])
                            temp = {}
                            temp['ULB Name'] = format_tenant_id(tenantid)
                            temp['Project Name'] = project['name']
                            temp['Project ID'] = project['projectNumber']
                            temp['Project Type'] = project['projectType']
                            temp['Ward no'] = project['address']['boundary']
                            temp['Project Value'] = project['additionalDetails']['estimatedCostInRs']
                            data.append(temp)
                    else:
                        break        
                else:
                    break
        return data
    except Exception as e:
        raise e

def format_business_service(business_service):
    # Extract the part after the dot and capitalize it
    return business_service.split('.')[1].capitalize() if '.' in business_service else business_service

def getUserName(id):
    try:
        print(id)
        host = USER_HOST + os.getenv('USER_SEARCH')
        request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
        headers = {"Content-Type": "application/json"}
        api_payload = {"uuid": [id],"RequestInfo": request_payload}
        response = requests.post(host,headers=headers,data=json.dumps(api_payload))
        print(response)
        if response and response.status_code and response.status_code in [200, 202]:
            response = response.json()
            if response and response['user'] and len(response['user'])>0:
                return response['user'][0]['name']
            else:
                return "NA"
        else:
            return "NA"
    except Exception as e:
        raise e

def getBillData():
    data = []
    print("Getting Bill Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            host = EXPENSE_HOST + os.getenv('BILL_SEARCH')
            request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
            headers = {"Content-Type": "application/json"}
            api_limit = 100
            api_offset = 0
            while True:
                api_payload = {"billCriteria": {"tenantId": tenantid, "isPaymentStatusNull": "false"},"pagination": {"limit": api_limit,"offSet": api_offset},"RequestInfo": request_payload}
                response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                api_offset = api_offset + api_limit
                if response and response.status_code and response.status_code in [200, 202]:
                    response = response.json()
                    if response and response['bills'] and len(response['bills'])>0:
                        for bill in response['bills']:
                            print("Bill Number: " + bill['billNumber'])
                            temp = {}
                            temp['ULB Name'] = format_tenant_id(tenantid)
                            temp['Project ID'] = bill['additionalDetails']['projectId']
                            temp['Bill ID'] = bill['billNumber']
                            temp['Bill Type'] = format_business_service(bill['businessService'])
                            temp['Muster roll Number'] = "NA"
                            if bill['businessService'] == "EXPENSE.WAGES":
                                temp['Muster roll Number'] = bill['billDetails'][0]['referenceId']
                            temp['Bill Amount in rs'] = bill['totalAmount']
                            temp['Prepared by (Engineer Name)'] = getUserName(bill['auditDetails']['createdBy'])
                            temp['Bill Creation Date'] = convert_epoch_to_indian_time(bill['auditDetails']['createdTime'])
                            temp['Workflow status'] = bill['wfStatus']
                            temp['Last Modified Date'] = convert_epoch_to_indian_time(bill['auditDetails']['lastModifiedTime'])
                            data.append(temp)
                    else:
                        break
                else:
                    break
        return data
    except Exception as e:
        raise e
    

def getMusterRollData():
    data = []
    print("Getting MusterRoll Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            api_limit = 100
            api_offset = 0
            while True:
                host = MUSTER_HOST + os.getenv('MUSTER_ROLL_SEARCH') + "?tenantId=" + tenantid + "&limit=" + str(api_limit) + "&offset=" + str(api_offset)
                request_payload = {"apiId": "Rainmaker", "authToken": "b09a28f2-3bb4-4c9b-9731-b1cbd98d9018", "userInfo": {"id": 271, "uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11", "userName": "MUKTAUAT", "name": "MUKTAUAT", "mobileNumber": "9036774122", "type": "EMPLOYEE", "roles": [{"name": "ESTIMATE APPROVER", "code": "ESTIMATE_APPROVER", "tenantId": "od.testing"}, {"name": "WORK ORDER CREATOR", "code": "WORK_ORDER_CREATOR", "tenantId": "od.testing"}, {"name": "Organization viewer", "code": "ORG_VIEWER", "tenantId": "od.testing"}, {"name": "MB_VERIFIER", "code": "MB_VERIFIER", "tenantId": "od.testing"}, {"name": "ESTIMATE CREATOR", "code": "ESTIMATE_CREATOR", "tenantId": "od.testing"}, {"name": "MDMS Admin", "code": "MDMS_ADMIN", "tenantId": "od.testing"}, {"name": "MB_VIEWER", "code": "MB_VIEWER", "tenantId": "od.testing"}, {"name": "State Dashboard Admin", "code": "STADMIN", "tenantId": "od.testing"}, {"name": "MUKTA Admin", "code": "MUKTA_ADMIN", "tenantId": "od.testing"}, {"name": "Employee Common", "code": "EMPLOYEE_COMMON", "tenantId": "od.testing"}, {"name": "TECHNICAL SANCTIONER", "code": "TECHNICAL_SANCTIONER", "tenantId": "od.testing"}, {"name": "BILL_CREATOR", "code": "BILL_CREATOR", "tenantId": "od.testing"}, {"name": "BILL_ACCOUNTANT", "code": "BILL_ACCOUNTANT", "tenantId": "od.testing"}, {"name": "WORK_ORDER_VIEWER", "code": "WORK_ORDER_VIEWER", "tenantId": "od.testing"}, {"name": "BILL_VERIFIER", "code": "BILL_VERIFIER", "tenantId": "od.testing"}, {"name": "ESTIMATE VERIFIER", "code": "ESTIMATE_VERIFIER", "tenantId": "od.testing"}, {"name": "MUSTER ROLL APPROVER", "code": "MUSTER_ROLL_APPROVER", "tenantId": "od.testing"}, {"name": "ESTIMATE VIEWER", "code": "ESTIMATE_VIEWER", "tenantId": "od.testing"}, {"name": "WORK ORDER APPROVER", "code": "WORK_ORDER_APPROVER", "tenantId": "od.testing"}, {"name": "MB_APPROVER", "code": "MB_APPROVER", "tenantId": "od.testing"}, {"name": "MDMS CITY ADMIN", "code": "MDMS_CITY_ADMIN", "tenantId": "od.testing"}, {"name": "OFFICER IN CHARGE", "code": "OFFICER_IN_CHARGE", "tenantId": "od.testing"}, {"name": "PROJECT CREATOR", "code": "PROJECT_CREATOR", "tenantId": "od.testing"}, {"name": "BILL_VIEWER", "code": "BILL_VIEWER", "tenantId": "od.testing"}, {"name": "WORK ORDER VERIFIER", "code": "WORK_ORDER_VERIFIER", "tenantId": "od.testing"}, {"name": "PROJECT VIEWER", "code": "PROJECT_VIEWER", "tenantId": "od.testing"}, {"name": "BILL_APPROVER", "code": "BILL_APPROVER", "tenantId": "od.testing"}, {"name": "MB_CREATOR", "code": "MB_CREATOR", "tenantId": "od.testing"}, {"name": "MUSTER ROLL VERIFIER", "code": "MUSTER_ROLL_VERIFIER", "tenantId": "od.testing"}, {"name": "HRMS Admin", "code": "HRMS_ADMIN", "tenantId": "od.testing"}], "tenantId": "od.testing", "permanentCity": "Testing"}, "msgId": "1705558029324|en_IN", "plainAccessRequest": {}}
                headers = {"Content-Type": "application/json"}
                api_payload = {"pagination": {"limit": api_limit,"offSet": api_offset},"RequestInfo": request_payload}
                response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                api_offset = api_offset + api_limit
                if response and response.status_code and response.status_code in [200, 202]:
                    response = response.json()
                    if response and response['musterRolls'] and len(response['musterRolls'])>0:
                        for roll in response['musterRolls']:
                            print("Muster Roll Number: " + roll['musterRollNumber'])
                            temp = {}
                            temp['ULB Name'] = format_tenant_id(tenantid)
                            temp['Project ID'] = roll['additionalDetails']['projectId']
                            temp['Muster roll ID'] = roll['musterRollNumber']
                            temp['Start date'] = convert_epoch_to_indian_time(roll['startDate'])
                            temp['End date'] = convert_epoch_to_indian_time(roll['endDate'])
                            temp['Submission date'] = convert_epoch_to_indian_time(roll['auditDetails']['createdTime'])
                            temp['Muster roll Status'] = roll['musterRollStatus']
                            temp['Last Modified Date'] = convert_epoch_to_indian_time(roll['auditDetails']['lastModifiedTime'])
                            idleDays = 0
                            daysEngaged = 0
                            wageSeekersEngaged = 0
                            males = 0
                            females = 0
                            others = 0
                            for entry in roll['individualEntries']:
                                print("Individual ID: " + entry['individualId'])
                                daysEngaged += entry['actualTotalAttendance']
                                idleDays += (7 - entry['actualTotalAttendance'])
                                if entry['actualTotalAttendance'] != 0:
                                    wageSeekersEngaged += 1
                                gender = entry['additionalDetails'].get('gender', 'NA')
                                if gender == "MALE":
                                    males += 1
                                elif gender == "FEMALE":
                                    females += 1
                                else:
                                    others += 1
                            temp['No of IdleDays'] = idleDays
                            temp['No of person days Engaged'] = daysEngaged
                            temp['No of wage seekers engaged'] = wageSeekersEngaged
                            temp['No of male'] = males
                            temp['No of female'] = females
                            temp['Others'] = others    
                            data.append(temp)
                    else:
                        break
                else:
                    break  
        return data
    except Exception as e:
        raise e

def getbeneficiaryNameIND(id, tenantid):
    try:
        host = INDIVIDUAL_HOST + os.getenv('INDIVIDUAL_SEARCH') + "?tenantId=" + tenantid + "&limit=1" + "&offset=0"
        request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
        headers = {"Content-Type": "application/json"}
        api_payload = {"Individual":{"id": [id]},"RequestInfo": request_payload}
        response = requests.post(host,headers=headers,data=json.dumps(api_payload))
        if response and response.status_code and response.status_code in [200, 202]:
            response = response.json()
            if response and response['Individual'] and len(response['Individual'])>0:
                return response['Individual'][0]['name']['givenName']
            else:
                return "NA"
        else:
            return "NA"
    except Exception as e:
        raise e

def getProjectIdfromContract(contract_number, tenantid):
    try:
        host = CONTRACT_HOST + os.getenv('CONTRACT_SEARCH')
        request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
        headers = {"Content-Type": "application/json"}
        api_payload = {"tenantId": tenantid,"contractNumber": contract_number,"RequestInfo": request_payload}
        response = requests.post(host,headers=headers,data=json.dumps(api_payload))
        if response and response.status_code and response.status_code in [200, 202]:
            response = response.json()
            if response and response['contracts'] and len(response['contracts'])>0:
                return response['contracts'][0]['additionalDetails']['projectId']
            else:
                return "NA"
        else:
            return "NA"
    except Exception as e:
        raise e
    
def extract_contract_number(reference_id):
    # Define the regular expression pattern to match the contract number
    pattern = r'WO/\d{4}-\d{2}/\d{6}'
    match = re.search(pattern, reference_id)
    if match:
        return match.group(0)
    return None


def getFailedPayments(payment_number):
    data = []
    try:
        host = MUKTA_ADAPTER_HOST + os.getenv('MUKTA_ADAPTER_PI_SEARCH')
        request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
        headers = {"Content-Type": "application/json"}
        api_limit = 100
        api_offset = 0
        print("Getting Failed Payments")
        while True:
            api_payload = {"criteria": {"payment_number": payment_number},"pagination": {"limit": api_limit,"offSet": api_offset,"sortBy": "createdtime","order": "DESC"},"RequestInfo": request_payload}
            response = requests.post(host,headers=headers,data=json.dumps(api_payload))
            api_offset = api_offset + api_limit
            if response and response.status_code and response.status_code in [200, 202]:
                response = response.json()
                if response and response['paymentInstructions'] and len(response['paymentInstructions'])>0:
                    pi = response['paymentInstructions'][0]
                    print("Payment Instruction ID: " + pi['jitBillNo'])
                    tenantId = pi['tenantId']
                    contract_number = extract_contract_number(pi['additionalDetails']['referenceId'][0])
                    project_id = getProjectIdfromContract(contract_number, tenantId)
                    # Extract data from the PI level
                    pi_data = {
                        'ULB Name': format_tenant_id(pi['tenantId']),
                        'Project ID': project_id,
                        'Payment Instruction ID': pi['jitBillNo'],
                        'Bill ID': pi['additionalDetails']['billNumber'][0],
                        'Payment Creation Date': convert_epoch_to_indian_time(pi['auditDetails']['createdTime'])
                    }
                    for beneficiary in pi['beneficiaryDetails']:
                        beneficiary_name = 'NA'
                        if beneficiary['beneficiaryType'] == 'IND':
                            beneficiary_name = getbeneficiaryNameIND(beneficiary['beneficiaryId'], tenantId)
                        # if beneficiary['beneficiaryType'] == 'ORG':
                        #     beneficiary_name = getbeneficiaryNameORG(beneficiary['beneficiaryId'])
                        # Extract account number and IFSC code from bankAccountId
                        account_info = beneficiary['bankAccountId'].split('@')
                        account_number = account_info[0] if len(account_info) > 0 else ''
                        ifsc_code = account_info[1] if len(account_info) > 1 else ''

                        # Extract data from the beneficiary level
                        beneficiary_data = {
                            'Beneficiary ID': beneficiary['beneficiaryNumber'],
                            'Beneficiary Name': beneficiary_name,
                            'Type Of Beneficiary': beneficiary['beneficiaryType'],
                            'Account Number': account_number,
                            'IFSC Code': ifsc_code    
                        }
                        # Combine PI data and beneficiary data
                        combined_data = {**pi_data, **beneficiary_data}
                        data.append(combined_data)
                else:
                    break
            else:
                break
        return data

    except Exception as e:
        raise e

def getFailedPaymentsDataFromExpense():
    data = []
    print("Getting Failed Payments Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            host = EXPENSE_HOST + os.getenv('EXPENSE_PAYMENT_SEARCH')
            request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
            headers = {"Content-Type": "application/json"}
            api_limit = 10
            api_offset = 0
            while True:
                api_payload = {"paymentCriteria": {"tenantId": tenantid, "status": "FAILED"},"pagination": {"limit": api_limit,"offSet": api_offset},"RequestInfo": request_payload}
                response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                api_offset = api_offset + api_limit
                if response and response.status_code and response.status_code in [200, 202]:
                    response = response.json()
                    if response and response['payments'] and len(response['payments'])>0:
                        for payment in response['payments']:
                            payment_number = payment['paymentNumber']
                            print("payment number: " + payment_number)
                            payment_data = getFailedPayments(payment_number)
                            data.extend(payment_data)
                    else:
                        break
                else:
                    break
        return data

    except Exception as e:
        raise e
    

def getSuccessData(payment_number):
    data = []
    try:
        host = MUKTA_ADAPTER_HOST + os.getenv('MUKTA_ADAPTER_PI_SEARCH')
        request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
        headers = {"Content-Type": "application/json"}
        api_limit = 100
        api_offset = 0
        print("Getting Success Payments")
        while True:
            api_payload = {"criteria": {"payment_number": payment_number},"pagination": {"limit": api_limit,"offSet": api_offset,"sortBy": "createdtime","order": "DESC"},"RequestInfo": request_payload}
            response = requests.post(host,headers=headers,data=json.dumps(api_payload))
            api_offset = api_offset + api_limit
            if response and response.status_code and response.status_code in [200, 202]:
                response = response.json()
                if response and response['paymentInstructions'] and len(response['paymentInstructions'])>0:
                    for pi in response['paymentInstructions']:
                        if pi['piStatus'] != 'FAILED' and pi.get('parentPiNumber') is None:
                            print("Payment Instruction ID: " + pi['jitBillNo'])
                            tenantId = pi['tenantId']
                            contract_number = extract_contract_number(pi['additionalDetails']['referenceId'][0])
                            project_id = getProjectIdfromContract(contract_number, tenantId)
                            # Extract data from the PI level
                            pi_data = {
                                'ULB Name': format_tenant_id(pi['tenantId']),
                                'Project ID': project_id,
                                'Bill ID': pi['additionalDetails']['billNumber'][0],
                                'Payment Instruction ID': pi['jitBillNo'],
                                'Payment Creation Date': convert_epoch_to_indian_time(pi['auditDetails']['createdTime']),
                                'Payment Status': pi['piStatus'],
                                'Total bill amount': pi['grossAmount']
                            }
                            data.append(pi_data)
                else:
                    break
            else:
                break
        return data

    except Exception as e:
        raise e


def getSuccessPaymentsDataFromExpense():
    data = []
    print("Getting Success Payments Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            host = EXPENSE_HOST + os.getenv('EXPENSE_PAYMENT_SEARCH')
            request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
            headers = {"Content-Type": "application/json"}
            api_limit = 10
            api_offset = 0
            statuses = ["SUCCESSFUL", "PARTIAL"]
            for status in statuses:
                while True:
                    api_payload = {"paymentCriteria": {"tenantId": tenantid, "status": status},"pagination": {"limit": api_limit,"offSet": api_offset},"RequestInfo": request_payload}
                    response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                    api_offset = api_offset + api_limit
                    if response and response.status_code and response.status_code in [200, 202]:
                        response = response.json()
                        if response and response['payments'] and len(response['payments'])>0:
                            for payment in response['payments']:
                                payment_number = payment['paymentNumber']
                                print("payment number: " + payment_number)
                                payment_data = getSuccessData(payment_number)
                                data.extend(payment_data)
                        else:
                            break
                    else:
                        break
        return data

    except Exception as e:
        raise e
        
def getEstimateData():
    data = []
    print("Getting Estimate Data")
    try:
        for tenantid in tenantids:
            print(tenantid)
            api_limit = 100
            api_offset = 0
            while True:
                host = ESTIMATE_HOST + os.getenv('ESTIMATE_SEARCH') +"?tenantId="+tenantid+"&limit=" + str(api_limit) + "&offset=" + str(api_offset)
                request_payload = {"apiId": "Rainmaker","authToken": "3bb0c045-6e5c-4002-8504-6069bf20a5ba","userInfo": {"id": 271,"uuid": "81b1ce2d-262d-4632-b2a3-3e8227769a11"},"msgId": "1705908972414|en_IN","plainAccessRequest": {}}
                headers = {"Content-Type": "application/json"}
                api_payload = {"RequestInfo": request_payload}
                response = requests.post(host,headers=headers,data=json.dumps(api_payload))
                api_offset = api_offset + api_limit
                if response and response.status_code and response.status_code in [200, 202]:
                    response = response.json()
                    if response and response['estimates'] and len(response['estimates'])>0:
                        for estimate in response['estimates']:
                            print("Estimate number: " + estimate['estimateNumber'])
                            temp = {}
                            temp['ULB Name'] = format_tenant_id(tenantid)
                            temp['Project ID'] = estimate['additionalDetails']['projectNumber']
                            temp['Estimate ID'] = estimate['estimateNumber']
                            temp['Date of Creation'] = convert_epoch_to_indian_time(estimate['auditDetails']['createdTime'])
                            temp['Prepared by (Name)'] = getUserName(estimate['auditDetails']['createdBy'])
                            print("Prepared by (Name): " + temp['Prepared by (Name)'])
                            # workFlowData = getWorkflowDates(estimate['estimateNumber'], tenantid)
                            # temp['send backs (No of times)'] = workFlowData['sendBacks']
                            temp['Estimate Value'] = estimate['additionalDetails']['totalEstimatedAmount']
                            temp['Current Status'] = estimate['wfStatus']
                            temp['Labour Cose'] = estimate['additionalDetails']['labourMaterialAnalysis']['labour']
                            temp['Material Cost'] = estimate['additionalDetails']['labourMaterialAnalysis']['material']
                            data.append(temp)
                    else:
                        break
                else:
                    break
        return data

    except Exception as e:
        raise e

def writeDataToCSV(data, filename):
    if not data:
        print("No data to write.")
        return
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    try:
        logging.info('Report Started Generating')

        directory = '/home/admin1/Music'
        # directory = '/mukta-report/muktareport'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Get current date in ddmmyyyy format
        current_date = dt.datetime.now().strftime('%d%m%Y')
        
        # Generate filenames with the current date
        workOrder_filename = f'workOrder_{current_date}.csv'
        failedPayments_filename = f'failed_payments_{current_date}.csv'
        bill_filename = f'bill_{current_date}.csv'
        musterRoll_filename = f'musterRoll_{current_date}.csv'
        project_filename = f'project_{current_date}.csv'
        success_payments_filename = f'success_payments_{current_date}.csv'
        estimate_filename = f'estimate_{current_date}.csv'
        
        # # Process work order data
        # workOrder_data = getWorkOrderData()
        # workOrder_file_path = os.path.join(directory, workOrder_filename)
        # writeDataToCSV(workOrder_data, workOrder_file_path)
        
        # # Process failed payments data
        # failed_payments_data = getFailedPaymentsDataFromExpense()
        # failed_payments_file_path = os.path.join(directory, failedPayments_filename)
        # writeDataToCSV(failed_payments_data, failed_payments_file_path)
        
        # # Process bill data
        # bill_data = getBillData()
        # bill_file_path = os.path.join(directory, bill_filename)
        # writeDataToCSV(bill_data, bill_file_path)
        
        # # Process muster roll data
        # muster_Data = getMusterRollData()
        # muster_file_path = os.path.join(directory, musterRoll_filename)
        # writeDataToCSV(muster_Data, muster_file_path)
        
        # # Process project data
        # project_data = getProjectData()
        # project_file_path = os.path.join(directory, project_filename)
        # writeDataToCSV(project_data, project_file_path)

        # # Process Success/Partial Payments
        # success_payments_data = getSuccessPaymentsDataFromExpense()
        # success_payments_file_path = os.path.join(directory, success_payments_filename)
        # writeDataToCSV(success_payments_data, success_payments_file_path)

        # Estimate data
        estimate_data = getEstimateData()
        estimate_file_path = os.path.join(directory, estimate_filename)
        # writeDataToCSV(estimate_data, estimate_file_path)

        logging.info('Report Generated Successfully')
        print(f"Reports saved in directory: {directory}")


    except Exception as ex:
        logging.error("Exception occured on main.", exc_info=True)
        raise(ex)