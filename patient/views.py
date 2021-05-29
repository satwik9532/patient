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

    

