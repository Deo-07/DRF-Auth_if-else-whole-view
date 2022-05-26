from functools import partial
from Api_data.utils import request_is_authenticated,get_user_from_token
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.timezone import now
from sales.models import Customer
from hrm_app.models import EmployeesInfo

# API
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from notifications.models import *
from rest_framework import serializers, status
from rest_framework.response import Response 
from rest_framework   import generics 



# Django Filter Backend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from rest_framework import filters  


# Serializer and model
from .models import Leads_User_profile,Leads_Task,Leads_Account, Leads_Meeting,Leads_Contact,Leads_Deal,Leads_Leads_Data,Leads_Campaign,Lead_Task_Status_Data,Lead_Task_Priority_Data,Lead_Account_Type_Data,Lead_Account_Industry_Data,Lead_Account_Rating_Data,Lead_Account_Ownership_Data,Lead_Contact_Leads_Source,Leads_Deal_Stage_Choices,Leads_Lead_Status,Leads_Feed,Leads_Call,leadQuote,Related_to,Leads_call_Purpose_Choices
from .serializers import User_profileSerializer,TaskSerializer,AccountSerializer, Customer_Serializer,  Leads_MeetingSerializer,Leads_ContactSerializers,Leads_DealSerializers,Leads_Leads_DataSerializers,Leads_CampaignSerializers,Lead_Task_Status_DataSerializers,Lead_Task_Priority_DataSerializers,Lead_Account_Type_DataSerializers,Lead_Account_Industry_DataSerializers,Lead_Account_Rating_DataSerializers,Lead_Account_Ownership_DataSerializers,Lead_Contact_Leads_SourceSerializers,Leads_Deal_Stage_ChoicesSerializers,Leads_Lead_StatusSerializers,Leads_FeedSerializers,Leads_CallSerializers,leadQuoteSerializers,Related_toSerializers,Leads_call_Purpose_ChoicesSerializers


#Shreyash sales api views
@api_view(['POST'])
@csrf_exempt
def customer_add(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive':
            if request.method == 'POST':
                customer_serializer = Customer_Serializer(data = request.data)
                if customer_serializer.is_valid():
                    print('yes')
                    customer_serializer.save()
                    return Response(data= {'msg':"Success",'response_code':200}, status=status.HTTP_200_OK)
                return Response(data= {'msg':customer_serializer.errors}, status=400)
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)




# Deo abhinav  ---------------------------------------------            Task (Done)

@api_view(['POST','GET'])
@csrf_exempt
def task(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                tasks = Leads_Task.objects.all()
                serializer = TaskSerializer(tasks, many=True)
                return Response(data = {'msg':'success','data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'POST':  
                task_serializer =  TaskSerializer(data = request.data)               
                if  task_serializer.is_valid():
                    print('yes')
                    task_serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)

        return Response(data= {'msg':'task_serializer.errors','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)



@api_view(['GET','PATCH'])
@csrf_exempt
def task_data_patch(request, pk): 
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            
            if request.method == 'GET': 
                try:
                    task_serializer = TaskSerializer(Leads_Task.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data': task_serializer.data,'status':True,'response_code':200,'token':token},status=status.HTTP_200_OK)  

    
            elif  request.method == 'PATCH':  
                try:
                    task_serializer = TaskSerializer(Leads_Task.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Data Not Saved','status':'false','response_code':'201'})        
                # return Response(data = {'msg':'success Data Saved Successfully','status':'true','response code':'200'},status=status.HTTP_200_OK)  
                profile_id = Leads_Task.objects.get(pk=pk)
                task_serializer = TaskSerializer(profile_id,data = request.data, partial=True)                 
                if task_serializer.is_valid():
                    print('yes')
                    task_serializer.save()
                    return Response(data= {'msg':'Data saved Successfully' ,'status':True,'response_code':200}, status=status.HTTP_200_OK)
                return Response(data= {'msg':task_serializer.errors,'status':'False','response_code':201}, status=status.HTTP_201_CREATED) 
            else:
                return Response(data= {'msg':"You Don't have access"},)
    else:
        return Response(data={'msg':'Something with tokens','response_code':'201','status':'false'})









# Deo abhinav  --------------------------------------- USER_PROFILE  (Done)

@api_view(['GET'])
@csrf_exempt
def notice_board(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                notice = NoticeBoardData.objects.all()
                serializer = NoticeBoardDataSerializer(notice, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','status_code':201}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@csrf_exempt
def user_profile_data(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'POST':  
                profile_serializer = User_profileSerializer(data = request.data)                 
                if profile_serializer.is_valid():
                    print('yes')
                    profile_serializer.save()
                    return Response(data= {'msg':"Success",'response_code':200,'token':token}, status=status.HTTP_200_OK)

        return Response(data= {'msg':'profile_serializer.errors','response_code':201}, status=400) 
    else:
        return Response(data= {'msg':"You Don't have access",'response_code':'201'}, status=status.HTTP_201_CREATED)



@api_view(['GET','PATCH'])
@csrf_exempt
def user_profile_data_patch(request, pk): 
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            

            if request.method == 'GET': 
                try:
                    profile_serializer = User_profileSerializer(Leads_User_profile.objects.get(pk=pk))
                    print(profile_serializer)
                except : 
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':profile_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  



            elif  request.method == 'PATCH':  
                try:
                    profile_serializer = User_profileSerializer(Leads_User_profile.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Data Not Saved','status':'false','response_code':201}, status=status.HTTP_201_CREATED)        
                profile_id = Leads_User_profile.objects.get(pk=pk)
                profile_serializer = User_profileSerializer(profile_id,data = request.data, partial=True)                 
                if profile_serializer.is_valid():
                    print('yes')
                    profile_serializer.save()
                    return Response(data= {'msg':'Data saved Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
                return Response(data= {'msg':profile_serializer.errors,'status':'False','response_code':201}, status=status.HTTP_201_CREATED) 
            else:
                return Response(data= {'msg':"You Don't have access"}, status=status.HTTP_201_CREATED)
    else:
        return Response(data={'msg':'Something with tokens','response_code':201,'status':'false'},status=status.HTTP_201_CREATED)












# Deo abhinav(20/04/2022)  --------------------         ACCOUNT  (Done)


@api_view(['GET','POST'])
@csrf_exempt
def account_leads(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
           
           
            if request.method == 'GET':
                customer =  Leads_Account.objects.all()
                serializer =AccountSerializer(customer, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        
        
            elif request.method == 'POST':
                    # print('hhhhhhhhhhhh')
                    customer_serializer = AccountSerializer(data = request.data)  
                    print(customer_serializer)               
                    if customer_serializer.is_valid():
                        # print('lllllllllllllllllll')
                        # print('yes')
                        customer_serializer.save()
                        return Response(data= {'msg':"Success",'response_code':200,}, status=status.HTTP_200_OK)
        
        
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
  
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','status_code':201}, status=status.HTTP_201_CREATED)




@api_view(['GET'])
@csrf_exempt
def account_data_get(request, pk):   
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            
            if request.method == 'GET': 
                try:
                    account_serializer = AccountSerializer(Leads_Account.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':account_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@csrf_exempt
def account_data_patch(request,pk):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')  
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            if request.method == 'PATCH':
                account=Leads_Account.objects.get(pk=pk)
                account_serializer=AccountSerializer( account,data=request.data, partial=True)
                if account_serializer.is_valid():
                    account_serializer.save()
                    return Response({'msg':'Data Updated Successfully','Status Code':200})
                return Response(account_serializer.errors,{'msg':'Data Not Sent','response_code':201})

    else:
        return Response(data={'msg':'Somegthing Went Wrong With the Tokens','response_code':201},status=status.HTTP_201_CREATED)



@api_view(['DELETE'])
@csrf_exempt
def account_data_delete(request,pk):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')  
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
          
            if request.method == 'DELETE':
                try:
                    account=Leads_Account.objects.get(pk=pk)
                except:
                    return Response(data={'msg':'User Allready Deleted or Not Exists','response_code':201},status=status.HTTP_201_CREATED)
                account_serializer=AccountSerializer(account,data=request.data)
                # account_serializer.delete()
                account.delete()
                return Response({'msg':'Data Deleted Successfully','response_code':200},status=status.HTTP_200_OK)
            else :
                return Response(data={'msg':'User Not Deleted','response_code':201,})  
        else:
            return Response(data={'msg':'Somthing went wrong with the user','response_code':201},status=status.HTTP_201_CREATED)
    else:
        return Response(data={'msg':'Somegthing Went Wrong with the Tokens','response_code':201},status=status.HTTP_201_CREATED)




# deo abhinav (22-04-1:03)                  --------   (Meeting )

@api_view(['GET','POST'])
@csrf_exempt
def leed_meeting(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                meeting = Leads_Meeting.objects.all()
                meeting_count=Leads_Meeting.objects.count()
                serializer =Leads_MeetingSerializer(meeting, many=True)
                return Response(data = {'msg':'success','meeting_count':meeting_count,'response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','status_code':201}, status=status.HTTP_201_CREATED)
    if request_is_authenticated(request):
            user = get_user_from_token(request.META.get('HTTP_TOKEN'))
            token=request.META.get('HTTP_TOKEN')
            if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
                if request.method == 'POST':  
                    meeting_serializer = Leads_MeetingSerializer(data = request.data)                 
                    if meeting_serializer.is_valid():
                        print('yes')
                        meeting_serializer.save()
                        return Response(data= {'msg':"Success",'response_code':200,}, status=status.HTTP_200_OK)

            return Response(data= {'msg':'meeting_serializer.errors','response_code':201}, status=400) 
    else:
            return Response(data= {'msg':"You Don't have access",'response_code':'201'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@csrf_exempt
def meeting_data_patch(request,pk):
    if request.method == 'PATCH':
        meet=Leads_Meeting.objects.get(pk=pk)
        meeting_serializer=Leads_MeetingSerializer(meet,data=request.data, partial=True)
        if meeting_serializer.is_valid():
            meeting_serializer.save()
            return Response({'msg':'Data Updated Successfully','Status Code':200})
        return Response(meeting_serializer.errors,{'msg':'Data Not Sent','response_code':201})




#Deo Abhinav (29/04/2022)  -------  -----         ( Contact )

@api_view(['POST','GET'])
@csrf_exempt
def contact_leads(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                contact = Leads_Contact.objects.all()
                serializer = Leads_ContactSerializers(contact, many=True)
                return Response(data = {'msg':'success','data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")
            if request.method == 'POST':  
                contact_serializer = Leads_ContactSerializers(data = request.data)               
                if  contact_serializer.is_valid():
                    print('yes')
                    contact_serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)

        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)




#Deo Abhinav (30/04/2022)  -------  -----         ( Deals )

@api_view(['POST','GET'])
@csrf_exempt
def deal_leads(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                deal = Leads_Deal.objects.all()
                deal_count=Leads_Deal.objects.count()
                serializer =Leads_DealSerializers(deal, many=True)
                return Response(data = {'msg':'success','deal_count':deal_count,'data':serializer.data,'token':token,'response_code':200},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")
            if request.method == 'POST':  
                deal_serializer =Leads_DealSerializers(data = request.data)               
                if  deal_serializer.is_valid():
                    print('yes')
                    deal_serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)

        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)



#Deo Abhinav (30/04/2022)  -------  -----     ------    ( Leads_Data )

@api_view(['POST','GET'])
@csrf_exempt
def leads_data_leads(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                lead = Leads_Leads_Data.objects.all()
                lead_count = Leads_Leads_Data.objects.count()

                serializer =Leads_Leads_DataSerializers(lead, many=True)
                return Response(data = {'msg':'success','lead_count':lead_count,'response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)


    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")
            
            if request.method == 'POST':  
                lead_serializer =Leads_Leads_DataSerializers(data = request.data)               
                if  lead_serializer.is_valid():
                    print('yes')
                    lead_serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)






# Deo Abhinav (04/05/2022)  -------  -----  ---   ------    ( Campaign )

@api_view(['POST','GET'])
@csrf_exempt
def leads_campaign(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                campaign = Leads_Campaign.objects.all()
                serializer =Leads_CampaignSerializers(campaign, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)


    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")

            if request.method == 'POST':  
                campaign_serializer = Leads_CampaignSerializers(data = request.data)               
                if  campaign_serializer.is_valid():
                    print('yes')
                    campaign_serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
     
        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)


    


# Deo Abhinav (04/05/2022)  -------  -----  ---   ------    ( Task Status Choices Fields )

@api_view(['GET'])
@csrf_exempt
def task_status_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                task_status_data = Lead_Task_Status_Data.objects.all()
                serializer =Lead_Task_Status_DataSerializers(task_status_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)


# Deo Abhinav (04/05/2022)  -------  -----  -         (Task priority Choice Fields)

@api_view(['GET'])
@csrf_exempt
def task_priority_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                task_priority_data =Lead_Task_Priority_Data.objects.all()
                serializer =Lead_Task_Priority_DataSerializers(task_priority_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)





# Deo Abhinav (04/05/2022)  -------  -----  -         (Account Type  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def account_type_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                account_type_data =Lead_Account_Type_Data.objects.all()
                serializer =Lead_Account_Type_DataSerializers(account_type_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)



# Deo Abhinav (04/05/2022)  -------  -----  -         (Account Industry  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def account_industry_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                account_industry_data =Lead_Account_Industry_Data.objects.all()
                serializer =Lead_Account_Industry_DataSerializers(account_industry_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)



# Deo Abhinav (05/05/2022)  -------  -----  -         (Account Rating  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def account_rating_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                account_rating_data =Lead_Account_Rating_Data.objects.all()
                serializer =Lead_Account_Rating_DataSerializers(account_rating_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)





# Deo Abhinav (05/05/2022)  -------  -----  -         (Account Ownership  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def account_ownership_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                account_ownership_data =Lead_Account_Ownership_Data.objects.all()
                serializer = Lead_Account_Ownership_DataSerializers(account_ownership_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)








# Deo Abhinav (05/05/2022)  -------  -----  -         (Contact Leads Source  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def contact_leads_source_choice(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                contact_leads_source =Lead_Contact_Leads_Source.objects.all()
                serializer = Lead_Contact_Leads_SourceSerializers(contact_leads_source, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)






# Deo Abhinav (05/05/2022)  -------  -----  -         (Deals  Stage  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def deals_stage_choice(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                contact_leads_source =Leads_Deal_Stage_Choices.objects.all()
                serializer = Leads_Deal_Stage_ChoicesSerializers(contact_leads_source, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)




# Deo Abhinav (05/05/2022)  -------  -----  -         (Leads  Status  Choice Fields)

@api_view(['GET'])
@csrf_exempt
def leads_status_choice(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                leads_status_source =Leads_Lead_Status.objects.all()
                serializer = Leads_Lead_StatusSerializers(leads_status_source, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)







# Deo Abhinav (06/05/2022)  -------  -----  -         (Leads  Status  Choice Fields)
@api_view(['GET','POST'])
@csrf_exempt
def leads_feed(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
         
            if request.method == 'GET':
                leads_feed_data =Leads_Feed.objects.all()
                serializer = Leads_FeedSerializers(leads_feed_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        
            elif request.method == 'POST':  
                serializer = Leads_FeedSerializers(data = request.data)
                print('hhhhhhhhhh')               
                if  serializer.is_valid():
                    print('yes')
                    serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
        
                return Response(data= {'msg':"Data not valid",'response_code':201}, status=status.HTTP_201_CREATED)

        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)






# Deo Abhinav (06/05/2022)  -------  -----  -         (Lead  Call API)    GET/  POST  /    PATCH
@api_view(['POST','GET'])
@csrf_exempt
def leads_call(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
         
            if request.method == 'GET':
                call = Leads_Call.objects.all()
                serializer =Leads_CallSerializers(call, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)


    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")

            if request.method == 'POST':  
                serializer = Leads_CallSerializers(data = request.data)               
                if  serializer.is_valid():
                    print('yes')
                    serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
     
        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)






# Leads Call Patch API
@api_view(['PATCH'])
@csrf_exempt
def lead_call_data_patch(request,pk):
    if request.method == 'PATCH':
        call=Leads_Call.objects.get(pk=pk)
        serializer=Leads_CallSerializers(call,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated Successfully','Status Code':200})
        return Response(serializer.errors,{'msg':'Data Not Sent','response_code':201})



    

@api_view(['PATCH'])
@csrf_exempt
def lead_call_data_patch(request,pk):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':                                            
            if request.method == 'PATCH':
                    print('hello')
                    call=Leads_Call.objects.get(pk=pk)
                    serializer=Leads_CallSerializers(call,data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg':'Data Updated Successfully','data':serializer.data,'Status Code':200})
                    return Response(serializer.errors,{'msg':'Data Not Sent','response_code':201})

        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)







# Deo Abhinav (06/05/2022)  -------  -----  -         (Lead  Quoets)    GET/  POST 
@api_view(['POST','GET'])
@csrf_exempt
def leads_quote(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
         
            if request.method == 'GET':
                quote = leadQuote.objects.all()
                serializer =leadQuoteSerializers(quote, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)


    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")

            if request.method == 'POST':  
                serializer = leadQuoteSerializers(data = request.data)               
                if  serializer.is_valid():
                    print('yes')
                    serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
     
        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)






# All Filter API's -----------------------

# (1)   -    Leads filter API's

#Deo Abhinav (30/04/2022)  -------  -----     ------    ( Leads_Data )

@api_view(['GET'])
@csrf_exempt
def filter_leads_data(request):


    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                tutorials = Leads_Leads_Data.objects.all()
                myFilter = Leads_Leads_DataSerializers(request.GET, queryset=tutorials)

                if myFilter.is_valid():
                    tutorials = filterset.qs
                    serializer = Leads_Leads_DataSerializers(tutorials, many=True)
                    return Response(serializer.data)
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
 
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        print("hello")
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print("hello")
            
            if request.method == 'POST':  
                lead_serializer =Leads_Leads_DataSerializers(data = request.data)               
                if  lead_serializer.is_valid():
                    print('yes')
                    lead_serializer.save()
                    return Response(data= {'msg':'  Data sent Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
        return Response(data= {'msg':'Some','status':201}, status=status.HTTP_201_CREATED) 
    else:
         return Response(data= {'msg':'Something Wrong with the tokens','status':'false','response_code':201}, status=status.HTTP_201_CREATED)


# Deo Abhinav Create Report API (10/05/2022)
@api_view(['GET'])
@csrf_exempt
def report_api_data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
         
            if request.method == 'GET':
            
                lead_serializer = Leads_Leads_DataSerializers(Leads_Leads_Data.objects.all().order_by('-id'), many=True)
                deal_serializer = Leads_DealSerializers(Leads_Deal.objects.all().order_by('-id'), many=True)
                meeting_serializer =Leads_MeetingSerializer(Leads_Meeting.objects.all().order_by('-id'), many=True)
                # report_data = Report_API_Data.objects.all()
                # serializer =Report_API_DataSerializers(report_data, many=True)
                return Response(data = {'msg':'success','response_code':200,'meeting_report_data':meeting_serializer.data,'deal_report_data':deal_serializer.data,'lead_report_data':lead_serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)








# Create Filter API for Leads   -------    (12/05/2022)

@api_view(['GET','POST'])
@csrf_exempt
def LeadFilterViewSet(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method =='POST':


                search = request.data.get('search')
                leads_owner=request.data.get('leads_owner')
                first_name = request.data.get('first_name')
                last_name=request.data.get('last_name')
                title=request.data.get('title')
                company=request.data.get('company')
                phone=request.data.get('phone')
                mobile=request.data.get('mobile')
                lead_source=request.data.get('lead_source')
                lead_status=request.data.get('lead_status')
                industry=request.data.get('industry')
                rating=request.data.get('rating')
                fax=request.data.get('fax')
                website=request.data.get('website')
                no_of_employees=request.data.get('no_of_employees')
                skype_id=request.data.get('skype_id')
                secondary_email=request.data.get('secondary_email')
                twitter=request.data.get('twitter')
                street=request.data.get('street')
                country=request.data.get('country')
                city=request.data.get('city')
                zip_code=request.data.get('zip_code')
                description=request.data.get('description')

            


                if search:
                    data = Leads_Leads_Data.objects.filter(Q(leads_owner=search) , Q(first_name__icontains=search) ,
                        Q(last_name=search) , Q(title=search) , Q(company=search) ,  Q(mobile=search) , Q(phone=search) ,
                        Q(lead_source=search) , Q(lead_status=search) , Q(industry=search) ,
                        Q(rating=search)      , Q(fax=search),  Q(website=search), Q(no_of_employees=search) ,  Q(annual_revenue=search) , Q(state=search) , 
                        Q(skype_id=search) , Q(secondary_email=search) , Q(twitter=search) , Q(street=search)  ,Q(country=search) ,  Q(city=search)) , Q(zip_code=search) , Q(description=search)
                  

                

                    data_serializer = Leads_Leads_DataSerializers(data, many=True)
                              
                elif leads_owner:
                    leads_owner_data = Leads_Leads_Data.objects.filter(Q(leads_owner__icontains=leads_owner))
                    data_serializer = Leads_Leads_DataSerializers(leads_owner_data, many=True)

                elif first_name:
                    first_name_data = Leads_Leads_Data.objects.filter(Q(first_name__icontains=first_name))
                    data_serializer = Leads_Leads_DataSerializers(first_name_data, many=True)

                elif last_name:
                    last_name_data = Leads_Leads_Data.objects.filter(Q(last_name__icontains=last_name))
                    data_serializer = Leads_Leads_DataSerializers(last_name_data, many=True)

                elif title:
                    title_data = Leads_Leads_Data.objects.filter(Q(title__icontains=title))
                    data_serializer = Leads_Leads_DataSerializers(title_data, many=True)

                elif company:
                    company_data = Leads_Leads_Data.objects.filter(Q(company__icontains=company))
                    data_serializer = Leads_Leads_DataSerializers(company_data, many=True)

                elif phone:
                    phone_data = Leads_Leads_Data.objects.filter(Q(phone__icontains=phone))
                    data_serializer = Leads_Leads_DataSerializers(phone_data, many=True)

                elif mobile:
                    mobile_data = Leads_Leads_Data.objects.filter(Q(mobile__icontains=mobile))
                    data_serializer = Leads_Leads_DataSerializers(mobile_data, many=True)


                elif lead_source:
                    lead_source_data = Leads_Leads_Data.objects.filter(Q(lead_source__icontains=lead_source))
                    data_serializer = Leads_Leads_DataSerializers(lead_source_data, many=True)


                elif lead_status:
                    lead_status_data = Leads_Leads_Data.objects.filter(Q(lead_status__icontains=lead_status))
                    data_serializer = Leads_Leads_DataSerializers(lead_status_data, many=True)


                elif industry:
                    industry_data = Leads_Leads_Data.objects.filter(Q(industry__icontains=industry))
                    data_serializer = Leads_Leads_DataSerializers(industry_data, many=True)


                elif rating:
                    rating_data = Leads_Leads_Data.objects.filter(Q(rating__icontains=rating))
                    data_serializer = Leads_Leads_DataSerializers(rating_data, many=True)


                elif fax:
                    rating_data = Leads_Leads_Data.objects.filter(Q(fax__icontains=fax))
                    data_serializer = Leads_Leads_DataSerializers(rating_data, many=True)


                elif website:
                    website_data = Leads_Leads_Data.objects.filter(Q(website__icontains=website))
                    data_serializer = Leads_Leads_DataSerializers(website_data, many=True)


                elif no_of_employees:
                    no_of_employees_data = Leads_Leads_Data.objects.filter(Q(no_of_employees__icontains=no_of_employees))
                    data_serializer = Leads_Leads_DataSerializers(no_of_employees_data, many=True)


                elif skype_id:
                    skype_id_data = Leads_Leads_Data.objects.filter(Q(skype_id__icontains=skype_id))
                    data_serializer = Leads_Leads_DataSerializers(skype_id_data, many=True)


                elif secondary_email:
                    secondary_email_data = Leads_Leads_Data.objects.filter(Q(secondary_email__icontains=secondary_email))
                    data_serializer = Leads_Leads_DataSerializers(secondary_email_data, many=True)


                elif twitter:
                    twitter_data = Leads_Leads_Data.objects.filter(Q(twitter__icontains=twitter))
                    data_serializer = Leads_Leads_DataSerializers(twitter_data, many=True)


                elif street:
                    street_data = Leads_Leads_Data.objects.filter(Q(street__icontains=street))
                    data_serializer = Leads_Leads_DataSerializers(street_data, many=True)


                elif country:
                    country_data = Leads_Leads_Data.objects.filter(Q(country__icontains=country))
                    data_serializer = Leads_Leads_DataSerializers(country_data, many=True)


                elif zip_code:
                    zip_code_data = Leads_Leads_Data.objects.filter(Q(zip_code__icontains=zip_code))
                    data_serializer = Leads_Leads_DataSerializers(zip_code_data, many=True)

                elif description:
                    zip_code_data = Leads_Leads_Data.objects.filter(Q(description__icontains=description))
                    data_serializer = Leads_Leads_DataSerializers(zip_code_data, many=True)


                else:
                    data = Leads_Leads_Data.objects.all()
                    data_serializer = Leads_Leads_DataSerializers(data, many=True)
                return Response(data= {'msg':'API Hit Successfully' ,'data':data_serializer.data ,}, status=status.HTTP_200_OK)
                    






class ProductList(generics.ListAPIView):
    queryset = Leads_Leads_Data.objects.all()
    serializer_class = Leads_Leads_DataSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']











# Create Filter API for Deals Filter API  -------    (12/05/2022)



# Filter API By Using ViewSets ------------------------------------------ Not so useful but may importnat 

class DealFilterViewSet(viewsets.ModelViewSet):
    serializer_class=Leads_DealSerializers
    def get_queryset(self):
        report_queryset=Leads_Deal.objects.all()
        return report_queryset
    def retrieve(self, request, *args , **kwargs):
        if request_is_authenticated(request):
            user = get_user_from_token(request.META.get('HTTP_TOKEN'))
            token=request.META.get('HTTP_TOKEN')
            if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
                try:       
                     params=kwargs
                     report_data=Leads_Deal.objects.filter(Q(deal_owner=params['pk']) | Q(deal_name=params['pk']) | Q(deal_type=params['pk']) | Q(lead_source=params['pk']) | Q(campaign_source=params['pk']) | Q(stage=params['pk']))
                     report_serializer=Leads_DealSerializers(report_data,many=True)
                     return Response(report_serializer.data)

                except:
                      print('Hello')
                      return Response(data= {'msg':'Something Wrong With the First Name','response_code':201}, status=status.HTTP_200_OK)
        else:
            return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------------------------------








# Create Filter API for Deals Filter API  -------    (14/05/2022)
@api_view(['GET'])
@csrf_exempt
def search_filter(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        print(user)
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            print('heloooo')
            if request.method =='GET':
                print('jhfjhjhjghjh')
                try:
                    first_name = request.query_params.get('first_name')
                    print(first_name)
                except:
                    first_name = None   
                try:
                    last_name = request.query_params.get('last_name')
                    print(last_name)
                except:
                    last_name = None

                if first_name or last_name:
                    data = Leads_Leads_Data.objects.filter(Q(first_name__icontains=first_name) | Q(last_name__icontains=last_name))
                    print(data)
                    data_serializer = Leads_Leads_DataSerializers(data, many=True)
                    print(data_serializer)
                    return Response(data= {'msg':'Data got successfully', 'data':data_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response(data={'msg':' No data found'})
            return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)
        else:
            return Response(data= {'msg':'You do not have access','response_code':201}, status=status.HTTP_200_OK)












# Deo Abhinav Create Report API (10/05/2022)


@api_view(['GET'])
@csrf_exempt
def Call_api_data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
         
            if request.method == 'GET':
            
                lead_serializer = Leads_Leads_DataSerializers(Leads_Leads_Data.objects.all().order_by('-id'), many=True)
                contact_serializer = Leads_ContactSerializers(Leads_Contact.objects.all().order_by('-id'), many=True)

                return Response(data = {'msg':'success','response_code':200,'contact_report_data':contact_serializer.data,'lead_report_data':lead_serializer.data,'token':token},status=status.HTTP_200_OK)  
      
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)




# Deo abhinav  --------------------------------------- Related to API   (Done) (16-05-2022)

@api_view(['GET'])
@csrf_exempt
def related_to(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                related = Related_to.objects.all()
                serializer = Related_toSerializers(related, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','status_code':201}, status=status.HTTP_201_CREATED)




# Deo abhinav  --------------------------------------- Call Purpose  API   (Done) (16-05-2022)

@api_view(['GET'])
@csrf_exempt
def call_purpose(request):
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
            if request.method == 'GET':
                call_purpose = Leads_call_Purpose_Choices.objects.all()
                serializer = Leads_call_Purpose_ChoicesSerializers(call_purpose, many=True)
                return Response(data = {'msg':'success','response_code':200,'data':serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','status_code':201}, status=status.HTTP_201_CREATED)








@api_view(['GET'])
@csrf_exempt
def Related_To_Data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
         
            if request.method == 'GET':
                account_serializer = AccountSerializer(Leads_Account.objects.all().order_by('-id'), many=True)
                deal_serializer = Leads_DealSerializers(Leads_Deal.objects.all().order_by('-id'), many=True)
                campaign_serializer = Leads_CampaignSerializers(Leads_Campaign.objects.all().order_by('-id'), many=True)
  
                return Response(data = {'msg':'success','response_code':200,'account_data':account_serializer.data,'campaign_data':campaign_serializer.data,'deal_data':deal_serializer.data,'token':token},status=status.HTTP_200_OK)  
        else:
            return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)




# Acccount Filter . . . . . . . . .  (16/05/2022)



@api_view(['POST'])
@csrf_exempt
def account_Filter_Data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
      
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
        
            if request.method == 'POST':
                queryset=Leads_Account.objects.all()
                count = Leads_Account.objects.all().count()

                start_date=request.data.get('start_date',None)   #(1 query)
              
                end_date=request.data.get('end_date',None)    #2(query)
                
                check_account_owner=request.data.get('check_account_owner',None)   #(1 query)
                check_account_name=request.data.get('check_account_name',None)   #(1 query)
                check_account_site=request.data.get('check_account_site',None)   #(1 query)
                check_parent_account=request.data.get('check_parent_account',None)   #(1 query)
                check_account_number=request.data.get('check_account_number',None)   #(1 query)

                check_account_type=request.data.get('check_account_type',None)   #(1 query)
                check_industry=request.data.get('check_industry',None)    #2(query)
                check_rating=request.data.get('check_rating',None)    #2(query)
                check_annual_revenue=request.data.get('check_annual_revenue',None)    #2(query)
                check_ownership=request.data.get('check_ownership',None)    #2(query)
                check_phone=request.data.get('check_phone',None)    #2(query)
                check_fax=request.data.get('check_fax',None)    #2(query)
                check_website=request.data.get('check_website',None)    #2(query)
                check_ticker_symbol=request.data.get('check_ticker_symbol',None)    #2(query)
                check_employess=request.data.get('check_employess',None)    #2(query)
                check_sic_code=request.data.get('check_sic_code',None)    #2(query)
                check_billing_street=request.data.get('check_billing_street',None)    #2(query)
                check_billing_city=request.data.get('check_billing_city',None)    #2(query)
                check_billing_state=request.data.get('check_billing_state',None)    #2(query)
                check_billing_country=request.data.get('check_billing_country',None)    #2(query)
                check_shipping_street=request.data.get('check_shipping_street',None)    #2(query)
                check_shipping_city=request.data.get('check_shipping_city',None)    #2(query)
                check_shipping_state=request.data.get('check_shipping_state',None)    #2(query)
                check_shipping_code=request.data.get('check_shipping_code',None)    #2(query)
                check_shipping_country=request.data.get('check_shipping_country',None)    #2(query)

             
                if check_account_owner:  #check if key is not None
                    queryset=queryset.filter(account_owner=check_account_owner)
        # --
                if check_account_name:  #check if key is not None
                    queryset=queryset.filter(account_name=check_account_name)
                if check_account_site:  #check if key is not None
                    queryset=queryset.filter(account_site=check_account_site)
                if check_parent_account:  #check if key is not None
                    queryset=queryset.filter(parent_account=check_parent_account)

                if check_account_number:  #check if key is not None
                    queryset=queryset.filter(account_number=check_account_number)

                if check_account_type:  #check if key is not None
                    queryset=queryset.filter(account_type=check_account_type)
        # -
                if check_industry:  #check if key is not None
                    queryset=queryset.filter(industry=check_industry)
        # --
                if check_rating:  #check if key is not None
                    queryset=queryset.filter(rating=check_rating)

                if check_annual_revenue:  #check if key is not None
                    queryset=queryset.filter(annual_revenue=check_annual_revenue)

                if check_ownership:  #check if key is not None
                    queryset=queryset.filter(ownership=check_ownership)

                if check_phone:  #check if key is not None
                    queryset=queryset.filter(phone=check_phone)

                if check_fax:  #check if key is not None
                    queryset=queryset.filter(fax=check_fax)

                if check_website:  #check if key is not None
                    queryset=queryset.filter(website=check_website)

                if check_ticker_symbol:  #check if key is not None
                    queryset=queryset.filter(ticker_symbol=check_ticker_symbol)

                if check_employess:  #check if key is not None
                    queryset=queryset.filter(employess=check_employess)

                if check_sic_code:  #check if key is not None
                    queryset=queryset.filter(sic_code=check_sic_code)

                if check_billing_street:  #check if key is not None
                    queryset=queryset.filter(billing_street=check_billing_street)


                if check_billing_city:  #check if key is not None
                    queryset=queryset.filter(billing_city=check_billing_city)


                if check_billing_state:  #check if key is not None
                    queryset=queryset.filter(billing_state=check_billing_state)


                if check_billing_country:  #check if key is not None
                    queryset=queryset.filter(billing_country=check_billing_country)


                if check_shipping_street:  #check if key is not None
                    queryset=queryset.filter(shipping_street=check_shipping_street)


                if check_shipping_city:  #check if key is not None
                    queryset=queryset.filter(shipping_city=check_shipping_city)

                if check_shipping_state:  #check if key is not None
                    queryset=queryset.filter(shipping_state=check_shipping_state)


                if check_shipping_code:  #check if key is not None
                    queryset=queryset.filter(shipping_code=check_shipping_code)


                if check_shipping_country:  #check if key is not None
                    queryset=queryset.filter(shipping_country=check_shipping_country)


                
           
                if start_date and end_date:  #check if key is not None
                    # queryset=queryset.filter(created_at=check_created_at)
                    queryset = queryset.filter(created_date__range=[start_date,end_date])

                serializer=AccountSerializer(queryset,many=True)
                # count = AccountSerializer(queryset, many=True)
                return Response(data= {'msg':"data Getting Succesfully",'Data':serializer.data,'response_code':200}, )

    
            else:
                return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)






# Deal Filter  API. . . . . . . . .  (16/05/2022)



@api_view(['POST'])
@csrf_exempt
def deal_Filter_Data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
      
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
        
            if request.method == 'POST':
                queryset=Leads_Deal.objects.all()
                
                start_date=request.data.get('start_date',None)   #(1 query)
              
                end_date=request.data.get('end_date',None)    #2(query)

                only_start_date=request.data.get('only_start_date',None)   #(1 query)             
                only_end_date=request.data.get('only_end_date',None)    #2(query)

                check_deal_owner=request.data.get('check_deal_owner',None)   #(1 query)

                check_deal_name=request.data.get('check_deal_name',None)   #(1 query)

                check_account_name=request.data.get('check_account_name',None)   #(1 query)

                check_deal_type=request.data.get('check_deal_type',None)   #(1 query)

                check_next_step=request.data.get('check_next_step',None)   #(1 query)

                check_lead_source=request.data.get('check_lead_source',None)    #2(query)

                check_ammount=request.data.get('check_ammount',None)    #2(query)

                check_closing_date=request.data.get('check_closing_date',None)    #2(query)

                check_campaign_source=request.data.get('check_campaign_source',None)    #2(query)
                
                check_description=request.data.get('check_description',None)    #2(query)

                check_contact_name=request.data.get('check_contact_name',None)    #2(query)

                only_start_date=request.data.get('only_start_date',None)   #(1 query)             
                only_end_date=request.data.get('only_end_date',None)    #2(query)


                if only_start_date:  #check if key is not None
                    queryset=queryset.filter(start_date=only_start_date)

                if only_end_date:  #check if key is not None
                    queryset=queryset.filter(end_date=only_end_date)


                if check_deal_owner:  #check if key is not None
                    queryset=queryset.filter(deal_owner=check_deal_owner)

                if check_deal_name:  #check if key is not None
                    queryset=queryset.filter(deal_name=check_deal_name)

                if check_account_name:  #check if key is not None
                    queryset=queryset.filter(account_name=check_account_name)

                if check_deal_type:  #check if key is not None
                    queryset=queryset.filter(deal_type=check_deal_type)

                if check_next_step:  #check if key is not None
                    queryset=queryset.filter(next_step=check_next_step)

                if check_lead_source:  #check if key is not None
                    queryset=queryset.filter(lead_source=check_lead_source)

                if check_ammount:  #check if key is not None
                    queryset=queryset.filter(ammount=check_ammount)

                if check_campaign_source:  #check if key is not None
                    queryset=queryset.filter(campaign_source=check_campaign_source)

                if check_description:  #check if key is not None
                    queryset=queryset.filter(description=check_description)

                if check_contact_name:  #check if key is not None
                    queryset=queryset.filter(contact_name=check_contact_name)

                
           
                if start_date and end_date:  #check if key is not None
                    # queryset=queryset.filter(created_at=check_created_at)
                    queryset = queryset.filter(created_date__range=[start_date,end_date])


                serializer=Leads_DealSerializers(queryset,many=True)
                # count = AccountSerializer(queryset, many=True)
                # return Response(serializer.data)
                return Response(data= {'msg':"Data Getting Succefully",'data':serializer.data,'response_code':200})

    
            else:
                return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)







# --------------------------Leads Filter API

@api_view(['POST'])
@csrf_exempt
def leads_Filter_Data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
      
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
        
            if request.method == 'POST':
                
                queryset=Leads_Leads_Data.objects.all()
                
                start_date=request.data.get('start_date',None)   #(1 query)
              
                end_date=request.data.get('end_date',None)    #2(query)

                check_lead_owner=request.data.get('check_lead_owner',None)   #(1 query)

                check_first_name=request.data.get('check_first_name',None)   #(1 query)

                check_last_name=request.data.get('check_last_name',None)   #(1 query)

                check_title=request.data.get('check_title',None)   #(1 query)

                check_company=request.data.get('check_company',None)   #(1 query)

                check_phone=request.data.get('check_phone',None)   #(1 query)

                check_mobile=request.data.get('check_mobile',None)   #(1 query)

                check_lead_source=request.data.get('check_lead_source',None)   #(1 query)

                check_lead_status=request.data.get('check_lead_status',None)   #(1 query)

                check_industry=request.data.get('check_industry',None)   #(1 query)

                check_rating=request.data.get('check_rating',None)   #(1 query)
              
                check_annual_revenue=request.data.get('check_annual_revenue',None)   #(1 query)

                check_email=request.data.get('check_email',None)   #(1 query)
                check_fax=request.data.get('check_fax',None)   #(1 query)

                check_website=request.data.get('check_website',None)   #(1 query)

                check_no_of_employees=request.data.get('check_no_of_employees',None)   #(1 query)
               
                check_skype_id=request.data.get('check_skype_id',None)   #(1 query)

                check_secondary_email=request.data.get('check_secondary_email',None)   #(1 query)

                check_twitter=request.data.get('check_twitter',None)   #(1 query)

                # check_twitter=request.data.get('check_twitter',None)   #(1 query)
          
                check_street=request.data.get('check_street',None)   #(1 query)
                check_state=request.data.get('check_state',None)   #(1 query)
                            
                check_country=request.data.get('check_country',None)   #(1 query)

                check_city=request.data.get('check_city',None)   #(1 query)
                check_zip_code=request.data.get('check_zip_code',None)   #(1 query)
                check_description=request.data.get('check_description',None)   #(1 query)

           

                if check_lead_owner:  #check if key is not None
                    queryset=queryset.filter(leads_owner=check_lead_owner)

                if check_first_name:  #check if key is not None
                    queryset=queryset.filter(first_name=check_first_name)

                if check_last_name:  #check if key is not None
                    queryset=queryset.filter(last_name=check_last_name)

                if check_title:  #check if key is not None
                    queryset=queryset.filter(title=check_title)

                if check_company:  #check if key is not None
                    queryset=queryset.filter(company=check_company)

                if check_phone:  #check if key is not None
                    queryset=queryset.filter(phone=check_phone)

                if check_mobile:  #check if key is not None
                    queryset=queryset.filter(mobile=check_mobile)

                if check_lead_source:  #check if key is not None
                    queryset=queryset.filter(lead_source=check_lead_source)

                if check_lead_status:  #check if key is not None
                    queryset=queryset.filter(lead_status=check_lead_status)

                if check_industry:  #check if key is not None
                    queryset=queryset.filter(industry=check_industry)


                if check_rating:  #check if key is not None
                    queryset=queryset.filter(rating=check_rating)
                

                if check_annual_revenue:  #check if key is not None
                    queryset=queryset.filter(annual_revenue=check_annual_revenue)

                if check_email:  #check if key is not None
                    queryset=queryset.filter(email=check_email)

                if check_fax:  #check if key is not None
                    queryset=queryset.filter(fax=check_fax)
                
                if check_website:  #check if key is not None
                    queryset=queryset.filter(website=check_website)
                
                if check_no_of_employees:  #check if key is not None
                    queryset=queryset.filter(no_of_employees=check_no_of_employees)
                
                if check_skype_id:  #check if key is not None
                    queryset=queryset.filter(skype_id=check_skype_id)

                if check_secondary_email:  #check if key is not None
                    queryset=queryset.filter(secondary_email=check_secondary_email)

                if check_twitter:  #check if key is not None
                    queryset=queryset.filter(twitter=check_twitter)

                if check_street:  #check if key is not None
                    queryset=queryset.filter(street=check_street)
                
                if check_state:  #check if key is not None
                    queryset=queryset.filter(state=check_state)

                
                if check_country:  #check if key is not None
                    queryset=queryset.filter(country=check_country)


                if check_city:  #check if key is not None
                    queryset=queryset.filter(city=check_city)


                if check_zip_code:  #check if key is not None
                    queryset=queryset.filter(zip_code=check_zip_code)


                if check_description:  #check if key is not None
                    queryset=queryset.filter(description=check_description)
                

                
                                           
           
                if start_date and end_date:  #check if key is not None
                    # queryset=queryset.filter(created_at=check_created_at)
                    queryset = queryset.filter(created_date__range=[start_date,end_date])

                serializer=Leads_Leads_DataSerializers(queryset,many=True)
                # count = AccountSerializer(queryset, many=True)
                return Response(data= {'data':serializer.data,'response_code':200},)

    
            else:
                return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)









# --------------------------Contact  Filter API  (17-05-2022)


@api_view(['GET','POST'])
@csrf_exempt
def contact_Filter_Data(request):

    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')
      
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager':
        
            if request.method == 'POST':

                queryset=Leads_Contact.objects.all()


                start_date=request.data.get('start_date',None)   #(1 query)
              
                end_date=request.data.get('end_date',None)    #2(query)
              
                check_account_name=request.data.get('check_account_name',None)    #2(query)
              
                check_contact_owner=request.data.get('check_contact_owner',None)   #(1 query)
              
                check_first_name=request.data.get('check_first_name',None)   #(1 query) ----(modify)
              
                check_last_name=request.data.get('check_last_name',None)   #(1 query)
              
                check_email=request.data.get('check_email',None)   #(1 query)
              
                check_phone=request.data.get('check_phone',None)   #(1 query)
              
                check_other_phone=request.data.get('check_other_phone',None)   #(1 query)
                
                check_mobile=request.data.get('check_mobile',None)   #(1 query)
 
                check_assistant=request.data.get('check_assistant',None)   #(1 query)              
              
              
                check_lead_choice_source=request.data.get('check_lead_choice_source',None)   #(1 query)
              
                check_title=request.data.get('check_title',None)   #(1 query)
              
                check_department=request.data.get('check_department',None)   #(1 query)
              
                check_home_phone=request.data.get('check_home_phone',None)   #(1 query)


                check_fax=request.data.get('check_fax',None)   #(1 query)
              
                check_dob=request.data.get('check_dob',None)   #(1 query)
               
                check_asst_phone=request.data.get('check_asst_phone',None)   #(1 query)

                check_skype_id=request.data.get('check_skype_id',None)   #(1 query)
              
                check_secondary_email=request.data.get('check_secondary_email',None)   #(1 query)
           
                check_twitter=request.data.get('check_twitter',None)   #(1 query)
              
                check_reporting_to=request.data.get('check_description',None)   #(1 query)
              
                check_mailing_street=request.data.get('check_twitter',None)   #(1 query)
                
                check_mailing_city=request.data.get('check_city',None)   #(1 query)

                check_mailing_state=request.data.get('check_state',None)   #(1 query)
              
                check_mailing_country=request.data.get('check_country',None)   #(1 query)
              
                check_mailing_code=request.query_params.get('check_zip_code',None)   #(1 query)
              

                check_other_street=request.query_params.get('check_other_street',None)   #(1 query)
              
                check_other_state=request.query_params.get('check_other_state',None)   #(1 query)
              
                check_other_city=request.query_params.get('check_other_city',None)   #(1 query)
              
                check_other_code=request.query_params.get('check_other_code',None)   #(1 query)
              
                check_other_country=request.query_params.get('check_other_country',None)   #(1 query)
              
                check_description=request.query_params.get('check_description',None)   #(1 query)

           


                if check_account_name:  #check if key is not None
                    queryset=queryset.filter(account_name=check_account_name)

                if check_contact_owner:  #check if key is not None
                    queryset=queryset.filter(contact_owner=check_contact_owner)

                if check_first_name:  #check if key is not None
                    queryset=queryset.filter(first_name=check_first_name)

                if check_last_name:  #check if key is not None
                    queryset=queryset.filter(last_name=check_last_name)

                if check_email:  #check if key is not None
                    queryset=queryset.filter(email=check_email)

                if check_phone:  #check if key is not None
                    queryset=queryset.filter(phone=check_phone)

                if check_other_phone:  #check if key is not None
                    queryset=queryset.filter(other_phone=check_other_phone)




                if check_mobile:  #check if key is not None
                    queryset=queryset.filter(mobile=check_mobile)

                if check_assistant:  #check if key is not None
                    queryset=queryset.filter(assistant=check_assistant)

                if check_mobile:  #check if key is not None
                    queryset=queryset.filter(mobile=check_mobile)

                if check_assistant:  #check if key is not None
                    queryset=queryset.filter(assistant=check_assistant)

                if check_lead_choice_source:  #check if key is not None
                    queryset=queryset.filter(annual_revenue=check_annual_revenue)
                    

                if check_title:  #check if key is not None
                    queryset=queryset.filter(title=check_title)
                

                if check_department:  #check if key is not None
                    queryset=queryset.filter(department=check_department)
                
                if check_home_phone:  #check if key is not None
                    queryset=queryset.filter(home_phone=check_home_phone)

                    
                
                if check_fax:  #check if key is not None
                    queryset=queryset.filter(fax=check_fax)
                
                if check_dob:  #check if key is not None
                    queryset=queryset.filter(dob=check_dob)


                if check_asst_phone:  #check if key is not None
                    queryset=queryset.filter(asst_phone=check_asst_phone)




                if check_skype_id:  #check if key is not None
                    queryset=queryset.filter(skype_id=check_skype_id)


                if check_secondary_email:  #check if key is not None
                    queryset=queryset.filter(secondary_email=check_secondary_email)
                
                if check_twitter:  #check if key is not None
                    queryset=queryset.filter(twitter=check_twitter)


                
                if check_reporting_to:  #check if key is not None
                    queryset=queryset.filter(reporting_to=check_reporting_to)




                if check_mailing_street:  #check if key is not None
                    queryset=queryset.filter(mailing_street=check_mailing_street)



                if check_mailing_city:  #check if key is not None
                    queryset=queryset.filter(mailing_city=check_mailing_city)


                if check_mailing_state:  #check if key is not None
                    queryset=queryset.filter(description=check_description)

                if check_mailing_country:  #check if key is not None
                    queryset=queryset.filter(mailing_country=check_mailing_country)
                

                if check_mailing_code:  #check if key is not None
                    queryset=queryset.filter(mailing_code=check_mailing_code)
                

                if check_other_street:  #check if key is not None
                    queryset=queryset.filter(check_other_street=check_other_street)
                

                if check_other_state:  #check if key is not None
                    queryset=queryset.filter(other_state=check_other_state)
                

                if check_other_city:  #check if key is not None
                    queryset=queryset.filter(other_city=check_other_city)

                

                if check_other_code:  #check if key is not None
                    queryset=queryset.filter(other_code=check_other_code)
                


                if check_other_country:  #check if key is not None
                    queryset=queryset.filter(other_country=check_other_country)

                if check_description:  #check if key is not None
                    queryset=queryset.filter(description=check_description)
             


                
           
                if start_date and end_date:  #check if key is not None
                    # queryset=queryset.filter(created_at=check_created_at)
                    queryset = queryset.filter(created_date__range=[start_date,end_date])


                serializer=Leads_ContactSerializers(queryset,many=True)
                # count = AccountSerializer(queryset, many=True)
                return Response(data= {'msg':"You Don't have access",'data':serializer.data ,'response_code':200},)

    
            else:
                return Response(data= {'msg':"You Don't have access",'response_code':201}, status=status.HTTP_201_CREATED)
    else:
        return Response(data= {'msg':'Something Wrong With the Tokens','response_code':201}, status=status.HTTP_200_OK)











# Deo ABhinav _--- 16/05/2022    API for get data from Lead
@api_view(['GET'])
@csrf_exempt
def leads_data_get(request, pk):   
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            if request.method == 'GET': 
                try:
                    leads_serializer = Leads_Leads_DataSerializers(Leads_Leads_Data.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':leads_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)





# Deo ABhinav _--- 16/05/2022    API for get data from Lead

@api_view(['GET'])
@csrf_exempt
def leads_data_get(request, pk):   
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            
            if request.method == 'GET': 
                try:
                    leads_serializer = Leads_Leads_DataSerializers(Leads_Leads_Data.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':leads_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)





# Deal Search API 

@api_view(['GET'])
@csrf_exempt
def deals_search_api(request): 
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            if request.method == 'GET': 
                try:
                    queryset = Leads_Deal.objects.all()  
                    deal_owner = request.query_params.get('search')
                    deal_name = request.query_params.get('search')
                    deal_type = request.query_params.get('search')
                    next_step = request.query_params.get('search')
                    lead_source = request.query_params.get('search')
                    ammount = request.query_params.get('search')
                    stage = request.query_params.get('search')
                    probability = request.query_params.get('search')
                    expected_revenue = request.query_params.get('search')
                    campaign_source = request.query_params.get('search')
                    description = request.query_params.get('search')                    
                    

                    if deal_owner:
                        queryset = queryset.filter(Q(deal_owner__icontains=deal_owner)|
                        Q(deal_name__icontains=deal_name) | Q(deal_type__icontains=deal_type)|
                        Q(next_step__icontains=next_step)|Q(lead_source__icontains=lead_source)
                        |Q(ammount__icontains=ammount)|Q(stage__icontains=stage)|
                        Q(probability__icontains=probability)|Q(expected_revenue__icontains=expected_revenue)|
                        Q(campaign_source__icontains=campaign_source))

                        deal_serializer = Leads_DealSerializers(queryset, many=True)
                        return Response(data = {'msg':'success','data':deal_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
                    else:
                        return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                except :
                    
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':deal_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)






# Leads Filter  API - -  - - - - - -  (18-05-2022)



@api_view(['GET'])
@csrf_exempt
def leads_search_api(request): 
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            if request.method == 'GET': 
             
                try:
                    queryset = Leads_Leads_Data.objects.all()  

                    leads_owner = request.query_params.get('search')
                    first_name = request.query_params.get('search')
                    last_name = request.query_params.get('search')
                    title = request.query_params.get('search')
                    company = request.query_params.get('search')
                    phone = request.query_params.get('search')
                    mobile = request.query_params.get('search')
                    lead_source = request.query_params.get('search')
                    industry = request.query_params.get('search')                    
                    rating = request.query_params.get('search')
                    annual_revenue = request.query_params.get('search')
                    email = request.query_params.get('search') 
                    fax=request.query_params.get('search')
                    website=request.query_params.get('search')
                    no_of_employees=request.query_params.get('search')
                    skype_id=request.query_params.get('search')
                    secondary_email=request.query_params.get('search')
                    twitter=request.query_params.get('search')
                    street=request.query_params.get('search')
                    state=request.query_params.get('search')
                    country=request.query_params.get('search')
                    city=request.query_params.get('search')
                    zip_code=request.query_params.get('search')
                    description=request.query_params.get('search')
                                 

                    if leads_owner:
                        queryset = queryset.filter(Q(leads_owner__icontains=leads_owner)|
                        Q(first_name__icontains=first_name)|Q(title__icontains=title)   |
                        Q(company__icontains=company)      | Q(phone__icontains=phone)|
                        Q(mobile__icontains=mobile)        | Q(lead_source__icontains=lead_source)|
                        Q(industry__icontains=industry)    | Q(rating__icontains=rating)|
                        Q(annual_revenue__icontains=annual_revenue)    | Q(email__icontains=email)|
                        Q(fax__icontains=fax)    | Q(website__icontains=website)|
                        Q(no_of_employees__icontains=no_of_employees)    | Q(skype_id__icontains=skype_id)|
                        Q(secondary_email__icontains=secondary_email)    | Q(twitter__icontains=twitter) |Q(street__icontains=street)|
                        Q(state__icontains=state)    |  Q(country__icontains=country) | Q(city__icontains=city)|
                        Q(zip_code__icontains=zip_code) |Q(city__icontains=description))



                        lead_serializer = Leads_Leads_DataSerializers(queryset, many=True)
                        return Response(data = {'msg':'success','data':lead_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
                    else:
                        return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                except :
                    
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':lead_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)





# Account Search  API - -  - - - - - -  (18-05-2022)

@api_view(['GET'])
@csrf_exempt
def account_search_api(request): 
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            if request.method == 'GET': 
             
                try:
                    queryset = Leads_Account.objects.all()  
                    account_owner = request.query_params.get('search')
                    account_name = request.query_params.get('search')
                    account_site = request.query_params.get('search')
                    parent_account = request.query_params.get('search')
                    account_number  = request.query_params.get('search')
# ----    
                    account_type = request.query_params.get('search')
                    industry = request.query_params.get('search')
                    rating = request.query_params.get('search')
                    annual_revenue = request.query_params.get('search')
                    ownership = request.query_params.get('search')                    
# ----
                    phone = request.query_params.get('search')
                    fax = request.query_params.get('search')
                    website = request.query_params.get('search')
                    ticker_symbol = request.query_params.get('search')
                   
                    employess = request.query_params.get('search')
                    sic_code = request.query_params.get('search')                     
                    billing_street = request.query_params.get('search')
                    billing_city = request.query_params.get('search')
                    billing_state = request.query_params.get('search')
                    billing_country = request.query_params.get('search')                    
                    shipping_street = request.query_params.get('search')
                    shipping_city = request.query_params.get('search')
                    shipping_state = request.query_params.get('search')                    
                    shipping_code = request.query_params.get('search')
                    shipping_country = request.query_params.get('search')
                    description = request.query_params.get('search')                    
                                                
                    if account_owner:
                        queryset = queryset.filter(Q(account_owner__icontains=account_owner)|
                        Q(account_name__icontains=account_name)|Q(account_site__icontains=account_site)   |
                        Q(parent_account__icontains=parent_account) |   Q(account_number__icontains=account_number) |
                        
                        Q(account_type__icontains=account_type) |   Q(industry__icontains=industry) |

                        Q(rating__icontains=rating) |   Q(annual_revenue__icontains=annual_revenue) |

                        Q(ownership__icontains=ownership) |   Q(phone__icontains=phone)|
                        
                        Q(fax__icontains=fax) |   Q(website__icontains=website)|
                        
                        Q(ticker_symbol__icontains=ticker_symbol) |   Q(employess__icontains=employess)|
                        
                        Q(sic_code__icontains=sic_code) |   Q(billing_street__icontains=billing_street)|
                      
                        Q(billing_city__icontains=billing_city) |   Q(billing_state__icontains=billing_state)|
                        
                        Q(billing_country__icontains=billing_country) |   Q(shipping_street__icontains=shipping_street)|

                        Q(shipping_city__icontains=shipping_city) |   Q(shipping_state__icontains=shipping_state)|
                        
                        Q(shipping_code__icontains=shipping_code) |   Q(shipping_country__icontains=shipping_country)|
                       
                        Q(description__icontains=description))




                        account_serializer = AccountSerializer(queryset, many=True)
                        return Response(data = {'msg':'success','data':account_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
                    else:
                        return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                except :
                    
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':account_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)






# Leads_ContactSerializers
# Contact Search  API - -  - - - - - -  (18-05-2022)

@api_view(['GET'])
@csrf_exempt
def contact_search_api(request): 
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            if request.method == 'GET': 
             
                try:

                    queryset = Leads_Contact.objects.all()  

                    account_name = request.query_params.get('search')
                    contact_owner = request.query_params.get('search')
                    first_name = request.query_params.get('search')
                    last_name = request.query_params.get('search')
                    email  = request.query_params.get('search')
# ----    
                    phone = request.query_params.get('search')
                    other_phone = request.query_params.get('search')
                    mobile = request.query_params.get('search')
                    assistant = request.query_params.get('search')
                   
                    title = request.query_params.get('search')                    
                    department = request.query_params.get('search')
                    home_phone = request.query_params.get('search')
                    fax = request.query_params.get('search')
                   
                    dob = request.query_params.get('search')
                   
                    asst_phone = request.query_params.get('search')
                    skype_id = request.query_params.get('search')
                    secondary_email = request.query_params.get('search')
                    twitter = request.query_params.get('search')
                    reporting_to = request.query_params.get('search')

                    mailing_street = request.query_params.get('search')
                    mailing_city = request.query_params.get('search')
                    mailing_state = request.query_params.get('search')
                   
                    mailing_code = request.query_params.get('search')                    
                    mailing_country = request.query_params.get('search')
                    other_street = request.query_params.get('search')
                    other_city = request.query_params.get('search')                    
                    other_state = request.query_params.get('search')
                    other_code = request.query_params.get('search')
                    other_country = request.query_params.get('search')                    
                    description = request.query_params.get('search')                    
                        
                    if contact_owner:
                        queryset = queryset.filter(Q(account_name__icontains=account_name)|

                        
                        Q(contact_owner__icontains=contact_owner) | Q(first_name__icontains=first_name)|
                        Q(last_name__icontains=last_name) | Q(email__icontains=email)|

                        Q(phone__icontains=phone) | Q(other_phone__icontains=other_phone)|
                        Q(mobile__icontains=mobile) | Q(assistant__icontains=assistant)|

                        Q(title__icontains=title) | Q(department__icontains=department)|
                        Q(home_phone__icontains=home_phone) | Q(fax__icontains=fax)|

                        Q(dob__icontains=dob) | Q(asst_phone__icontains=asst_phone)|
                        Q(skype_id__icontains=skype_id) | Q(secondary_email__icontains=secondary_email)|
                        

                        Q(twitter__icontains=twitter) | Q(reporting_to__icontains=reporting_to)|
                        Q(mailing_street__icontains=mailing_street) | Q(mailing_city__icontains=mailing_city)|
                        
                        Q(mailing_state__icontains=mailing_state) | Q(mailing_code__icontains=mailing_code)|
                        Q(mailing_country__icontains=mailing_country) | Q(other_street__icontains=other_street)|
                        
                        Q(other_city__icontains=other_city) | Q(other_state__icontains=other_state)|
                        Q(other_code__icontains=other_code) | Q(other_country__icontains=other_country)|
                        Q(description__icontains=description))




                        contact_serializer = Leads_ContactSerializers(queryset, many=True)
                        return Response(data = {'msg':'success','data':contact_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
                    else:
                        return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                except :
                    
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':contact_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)









# Deo ABhinav _--- 16/05/2022    API for get data from Lead

@api_view(['GET'])
@csrf_exempt
def contact_data_get(request, pk):   
    if request_is_authenticated(request):
        user = get_user_from_token(request.META.get('HTTP_TOKEN'))
        token=request.META.get('HTTP_TOKEN')    
        if EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Executive' or EmployeesInfo.objects.get(user=user).department.dept_name == 'Sales Manager': 
            
            if request.method == 'GET': 
                try:
                    contact_serializer = Leads_ContactSerializers(Leads_Contact.objects.get(pk=pk))
                except : 
                    return Response(data={'msg':'Failed Please Entera a valid id','status':'false','response_code':201,}, status=status.HTTP_201_CREATED)        
                return Response(data = {'msg':'success','data':contact_serializer.data,'status':'true','response_code':200,'token':token},status=status.HTTP_200_OK)  
    
    else:
        return Response(data={'msg':'Something went wrong with the tokens','response_code':201},status=status.HTTP_201_CREATED)






