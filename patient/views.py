from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from patient.models import pp_patient_master
from patient.serializer import pp_patient_master_masterSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
import jwt , datetime
@csrf_exempt
@api_view(['POST'])

def patient_reg(request):
    if not request.COOKIES.get('jwt'):
        raise exceptions.AuthenticationFailed('unauthenticated')
    token = request.COOKIES.get('jwt')
    try:
        payload = jwt.decode(token,'secret_key',algorithms=['HS256'])  

    except jwt.ExpiredSignatureError:
       raise exceptions.AuthenticationFailed('unauthenticated')

    data = request.data
    data['pp_pm'] = payload['id']
    serializer = pp_patient_master_masterSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'patient added'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   




@csrf_exempt
@api_view(['GET'])
def get_patient(request):
    if not request.COOKIES.get('jwt'):
        raise exceptions.AuthenticationFailed('unauthenticated')
    token = request.COOKIES.get('jwt')
    try:
        payload = jwt.decode(token,'secret_key',algorithms=['HS256'])  

    except jwt.ExpiredSignatureError:
       raise exceptions.AuthenticationFailed('unauthenticated')
    
    data =  pp_patient_master.objects.filter(pp_pm = payload['id'])
    serializer = pp_patient_master_masterSerializer(data,many =True)
    return Response(serializer.data,status=status.HTTP_200_OK)

    
@csrf_exempt
@api_view(['GET','POST'])

def search(request):
    try:
        query = pp_patient_master.objects.filter(first_name__icontains = request.data['query'])
        if query.count()>0:
            serializer = pp_patient_master_masterSerializer(query,many = True)
            print(serializer.data)
            return Response(serializer.data,status = status.HTTP_200_OK) 
        return Response(status=status.HTTP_404_NOT_FOUND)   

    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)     
 


 
from django.http import JsonResponse
@csrf_exempt
def error_500(request):
    return JsonResponse({"message": "internal server error"}, status=500)

@csrf_exempt    
def error_404(request, exception):
    return JsonResponse({"message": "invalide API"}, status=404)
