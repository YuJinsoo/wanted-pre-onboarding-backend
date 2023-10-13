from django.shortcuts import render

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import JobOpening, Company
from .serializers import JobOpeningSerializer, CompanySerializer


class JobOpeningView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request, jo_pk):
        job_opening = JobOpening.objects.get(pk=jo_pk)
        serializer = JobOpeningSerializer(job_opening)
        
        return Response({"message":"success get!", "data": serializer.data}, status=status.HTTP_200_OK)
    
    
    def put(self, request, jo_pk):
        data = request.data
        serializer = JobOpeningSerializer(data=data)
        job_opening = JobOpening.objects.get(pk=jo_pk)
        
        if serializer.is_valid():
            obj = serializer.update(job_opening, serializer.validated_data)
            result = JobOpeningSerializer(obj)
            return Response({"message": "success update!", "data": result.data}, status=status.HTTP_200_OK)

        return Response({"message": "fail"}, status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self, request, jo_pk):
        job_opening = JobOpening.objects.get(pk=jo_pk)
        serializer = JobOpeningSerializer(job_opening)
        job_opening.delete()
        
        return Response({"message":"success delete!", "data": serializer.data}, status=status.HTTP_200_OK)


class JobOpeningCreateView(APIView):
    permission_classes = [AllowAny, ]
    
    def post(self, request):
        data = request.data
        serializer = JobOpeningSerializer(data=data)
        
        if serializer.is_valid():
            # serializer.data 는 Foreinkey의 pk만, serializer.validated_data는 object가 나옴
            obj = serializer.create(serializer.validated_data)
            result = JobOpeningSerializer(obj)
            return Response({"message": "success create!", "data": result.data }, status=status.HTTP_201_CREATED)
        
        return Response({"message": "fail", "error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class JobOpeningListView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        result = JobOpening.objects.all()
        serializer = JobOpeningSerializer(result, many=True)
        
        return Response({"message": "success get!", "data": serializer.data}, status=status.HTTP_200_OK)