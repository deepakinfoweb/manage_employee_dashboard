"""
Python and django define package 
"""
from django.shortcuts import render
from datetime import datetime
import pytz
from rest_framework.views import APIView
from rest_framework.views import Response
import smtplib
"""
user define file
"""
from user.models import account,AccountSerializer,user,UserSerializer

def home(request):
    output_json = get_account_status(request)
    return render(request,'index.html',output_json)


def thankYouPage(request):
    output_json = {}
    if request.method == 'POST' and request.FILES['photo']:
        input_json = request.POST.dict()
        try:
            insert_param = {}
            insert_param['name'] = input_json['name']
            insert_param['phone_id'] = input_json['phone']
            insert_param['email'] = input_json['email']
            insert_param['photo'] = request.FILES['photo']
            insert_param['account_type'] = input_json['status']
            serialized_user_params = UserSerializer(data = insert_param)
            if serialized_user_params.is_valid(raise_exception = True):
                serialized_user_params.save()
            output_json['Status'] = "Success"
            output_json['Message'] = "Data has been insert successfully"
        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Data could not be inserted successfully" +str(ex)
            output_json['Payload'] = str(ex)
    return render(request,'thankyou.html',output_json)

def all_User(request):
    output_json = {}
    output_json['Payload'] = {}
    user_info_obj = None
    # import pdb ; pdb.set_trace()
    try:
        if request.method == 'GET':
            user_info_obj=user.objects.all()
        else:
            user_info_obj=user.objects.filter(status=request.POST.get('status',None))
        user_info = UserSerializer(user_info_obj,many = True).data
        user_info_list = []
        for item in user_info:
            user_info = {}
            user_info['profile_id'] = item.get('profile_id',None) 
            user_info['name'] = item.get('name',None) 
            user_info['phone_id'] = item.get('phone_id',None) 
            user_info['email'] = item.get('email',None) 
            user_info['photo'] = item.get('photo',None) 
            user_status=account.objects.filter(account_id = item.get('account_type',None),isactive=True).values('account_name')
            user_info['account_type'] = user_status[0]['account_name']
            user_info['status'] = item.get('status',None) 
            datetime_object = datetime.strptime(str(item.get('last_modified_date',None).replace('T',' ').replace('Z','')), '%Y-%m-%d %H:%M:%S.%f')
            time_zone = pytz.timezone('Asia/Calcutta')
            user_info['added_date'] = time_zone.localize(datetime_object)
            user_info['last_modified_date'] = time_zone.localize(datetime_object)
            user_info_list.append(user_info)
        output_json['Status'] = "Success"
        output_json['Message'] = "data has been insert successfully"
        output_json['Payload'] = user_info_list
        # output_json['account_status'] = get_account_status(request)
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json['Message'] = "Data could not be fetched successfully" +str(ex)
        output_json['Payload'] = str(ex)
    return render(request,'alluser.html',output_json)

class ChangeStatus(APIView):
    def post(self,request,format = 'Json'):
        input_json = request.data
        output_json = {}
        output_json = changeStatus(input_json)
        return Response(output_json)

def changeStatus(input_json):
    output_json ={}
    output_json['Payload'] = {}
    try:
        user.objects.filter(profile_id=input_json.get('profile_id',None)).update(status=input_json.get('status',None))
        mail_status=sendmail(input_json.get('status',None),input_json.get('profile_id',None))
        if mail_status.get('Status',None) == 'Success':
            output_json['Status'] = "Success"
            output_json['Message'] = "Status have been update successfully"
        else:
            output_json['Status'] = "Failure"
            output_json['Message'] = "Mail have not been send successfully"
        return output_json
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json['Message'] = "Status have not been successfully. Exception encountered is " + str(ex)
        output_json['Payload'] = None
        return output_json
    
def get_account_status(request):
    output_json = {}
    try:
        account_info_obj=account.objects.all()
        account_info=AccountSerializer(account_info_obj,many = True).data
        current_list = []
        for item in account_info:
            current_status = {}
            current_status['account_id'] = item.get('account_id',None)
            current_status['account_name'] = item.get('account_name',None)
            current_list.append(current_status)
        output_json['Status'] = 'Success'
        output_json['Payload'] = current_list
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json['Message'] = "Data could not be fetched successfully" +str(ex)
        output_json['Payload'] = str(ex)
    return output_json

def pie_chart(request):
    output_json = {}
    try:
        pending_obj_count=user.objects.filter(status='Pending').count()
        reject_obj_count=user.objects.filter(status='Reject').count()
        approve_obj_count=user.objects.filter(status='Approve').count()
        counter_list = []
        counter_list.append(pending_obj_count)
        counter_list.append(reject_obj_count)
        counter_list.append(approve_obj_count)
        output_json['Status'] = "Success"
        output_json['Message'] = "Data has been insert successfully"
        output_json['Payload'] = counter_list
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json['Message'] = "Data could not be inserted successfully" +str(ex)
        output_json['Payload'] = str(ex)
    return render(request,'pie_chart.html',output_json)

def sendmail(status,profileid):
    output_json = {}
    try:
        user_email= user.objects.filter(profile_id=profileid).values('email')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('testing.deepak.sharma@gmail.com', 'Deepaktesting@123')
        reciever = user_email[0]['email']
        server.sendmail('testing.deepak.sharma@gmail.com',reciever,'Subject:Your Account Status\nHi,\nYour account has been '+status+'.')
        output_json['Status'] = "Success"
        output_json['Message'] = "Mail has been send successfully"
    except Exception as ex:
        output_json['Status'] = "Failure"
        output_json['Message'] = "Mail could not be send successfully" +str(ex)
        output_json['Payload'] = str(ex)
    return output_json
