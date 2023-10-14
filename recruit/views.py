from django.shortcuts import render

from django.core.exceptions import ValidationError
from django.db.models import Q, ProtectedError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from recruit.models import JobOpening, Company
from recruit.serializers import JobOpeningSerializer, UpdateJobOpeningSerializer, CompanySerializer


class JobOpeningView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request, jo_pk):
        job_opening = JobOpening.objects.get(pk=jo_pk)
        serializer = JobOpeningSerializer(job_opening)
        
        other_opening = JobOpening.objects.filter(company=job_opening.company)
        other_opening_pk = [x.pk for x in other_opening]
        other_opening_pk.pop(other_opening_pk.index(jo_pk))
        
        data = serializer.data
        data["other_opening"] = other_opening_pk
        
        return Response({"message":"success get!", "data": data}, status=status.HTTP_200_OK)
    
    def put(self, request, jo_pk):
        data = request.data
        if data.get("company"):
            raise ValidationError("company cannot be changed.")
        
        serializer = UpdateJobOpeningSerializer(data=data, partial=True)
        job_opening = JobOpening.objects.get(pk=jo_pk)
        
        if serializer.is_valid():
            # serializer에 의해 company가 제외된다.
            print("serial data:", serializer.validated_data)
            obj = serializer.update(job_opening, serializer.validated_data)
            result = UpdateJobOpeningSerializer(obj)
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
        print(serializer.is_valid())
        print(serializer.errors)
        
        if serializer.is_valid():
            # serializer.data 는 Foreinkey의 pk만, serializer.validated_data는 object가 나옴
            obj = serializer.create(serializer.validated_data)
            result = JobOpeningSerializer(obj)
            return Response({"message": "success create!", "data": result.data }, status=status.HTTP_201_CREATED)
        
        return Response({"message": "fail", "error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class JobOpeningListView(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        search_query = request.GET.get('search', None)
        
        if search_query:
            print(search_query)
            
            try:
                results = JobOpening.objects.filter(
                    Q(company__name__icontains=search_query) | 
                    Q(position__icontains=search_query) | 
                    Q(content__icontains=search_query) | 
                    Q(tech__icontains=search_query)
                    )
            except Company.DoesNotExist as e:
                results = JobOpening.objects.filter(
                    Q(position__icontains=search_query) | 
                    Q(content__icontains=search_query) | 
                    Q(tech__icontains=search_query)
                    )
            finally:
                serializer = JobOpeningSerializer(results, many=True)
                for data in serializer.data:
                    data["company_name"] = Company.objects.get(pk=data.get("id")).name
            
                print("results:",results)
                return Response({"message": "success get!", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            result = JobOpening.objects.all()
            serializer = JobOpeningSerializer(result, many=True)
            
            return Response({"message": "success get!", "data": serializer.data}, status=status.HTTP_200_OK)