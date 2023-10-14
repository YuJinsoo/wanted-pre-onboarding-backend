import json
from django.test import TestCase
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
# from rest_framework.test import APIClient
# from rest_framework.authentication import SessionAuthentication

from .serializers import JobOpeningSerializer, UpdateJobOpeningSerializer,CompanySerializer
from .models import JobOpening, Company

class TestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.company1 = Company.objects.create(name="원티드랩")
        cls.company2 = Company.objects.create(name="원티드코리아")
        cls.company3 = Company.objects.create(name="네이버")
        cls.company4 = Company.objects.create(name="카카오")
        
        data = {
            "company": cls.company1,
            "country":"한국",
            "location":"서울",
            "position":"백엔드 주니어 개발자",
            "reward":1000000,
            "content":"원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "tech":"Python"
        }
        
        cls.job_opening1 = JobOpening.objects.create(**data)
        cls.job_opening2 = JobOpening.objects.create(**data)
        
        data2 = {
            "company": cls.company2,
            "country":"한국",
            "location":"부산",
            "position":"프론트엔드 개발자",
            "reward":5000000,
            "content":"원티드코리아에서 프론트 개발자를 채용합니다.",
            "tech":"JavaScript"
        }
        cls.job_opening3 = JobOpening.objects.create(**data2)
        
        data3 = {
            "company":cls.company3,
            "country":"한국",
            "location":"판교",
            "position":"Django 백엔드 개발자",
            "reward":1000000,
            "content": "네이버에서 백엔드 개발자를 적극 채용하고 있습니다!",
            "tech":"Django"
        }
        cls.job_opening4 = JobOpening.objects.create(**data3)
        
        data4 = {
            "company":cls.company4,
            "country":"한국",
            "location":"판교",
            "position":"Django 백엔드 개발자",
            "reward":500000,
            "content": "카카오에서 백엔드 개발자를 적극 채용하고 있습니다!",
            "tech":"Python"
        }
        cls.job_opening5 = JobOpening.objects.create(**data4)
        
        data5 = {
            "company": cls.company1,
            "country":"한국",
            "location":"성남",
            "position":"SW 개발자",
            "reward":2000000,
            "content":"원티드랩에서 SW개발자를 채용합니다. 자격요건은..",
            "tech":"JAVA"
        }
        cls.job_opening6 = JobOpening.objects.create(**data5)
        data6 = {
            "company": cls.company1,
            "country":"한국",
            "location":"여의도",
            "position":"윈도우 개발자",
            "reward":2000000,
            "content":"원티드랩에서 윈도우개발자를 채용합니다. 자격요건은..",
            "tech":"C++"
        }
        cls.job_opening7 = JobOpening.objects.create(**data6)
    
    def test_create_JobOpening(self):
        company = Company.objects.create(name="원티드")
        
        expected = {
            "company": company.pk,
            # "company": company.id,
            "position":"백엔드 주니어 개발자",
            "reward":1000000,
            "content":"원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "tech":"Python"
        }
        
        response = self.client.post("/recruit/jobopening/",
                                    data=json.dumps(expected),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        result = response.data.get("data")
        
        self.assertEqual(result["company"], expected["company"])
        self.assertEqual(result["position"], expected["position"])
        self.assertEqual(result["reward"], expected["reward"])
        self.assertEqual(result["content"], expected["content"])
        self.assertEqual(result["tech"], expected["tech"])
    
    
    def test_update_JobOpening(self):
        jo_pk = self.job_opening1.pk
        
        serializer = JobOpeningSerializer(self.job_opening1)
        origin = serializer.data
        
        expected = {
            "reward":1500000,
            "content":"원티드랩에서 백엔드 주니어 개발자를 '적극' 채용합니다. 자격요건은.."
        }
        
        response = self.client.put(f"/recruit/jobopening/{jo_pk}/",
                                   data=json.dumps(expected),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        updated_job_opening1 = JobOpening.objects.get(pk=jo_pk)
        
        self.assertEqual(updated_job_opening1.id, origin.get("id"))
        self.assertEqual(updated_job_opening1.tech, origin.get("tech"))
        self.assertEqual(updated_job_opening1.reward, expected.get("reward"))
        self.assertEqual(updated_job_opening1.content, expected.get("content"))
        
        ## company 바꾸려고 하는 경우
        jo_pk = self.job_opening2.pk
        self.assertEqual(self.job_opening2.company.id, self.company1.id)
        
        serializer = JobOpeningSerializer(self.job_opening2)
        origin = serializer.data
        
        expected = {
            "company": self.company2.pk,
            # "company": company_serializer.data,
            "tech": "Django",
        }
        
        print("expected:", expected)
        
        with self.assertRaises(ValidationError):
            response = self.client.put(f"/recruit/jobopening/{jo_pk}/",
                                    data=json.dumps(expected),
                                    content_type='application/json')
        
        updated_job_opening2 = JobOpening.objects.get(pk=jo_pk)
        self.assertEqual(updated_job_opening2.id, origin.get("id"))
        self.assertEqual(updated_job_opening2.tech, origin.get("tech"))
        self.assertEqual(updated_job_opening2.reward, origin.get("reward"))
        self.assertEqual(updated_job_opening2.content, origin.get("content"))
        
    
    def test_delete_JobOpening(self):
        jo_pk = self.job_opening1.pk
        
        response = self.client.delete(f"/recruit/jobopening/{jo_pk}/")
        
        self.assertEqual(response.status_code, 200)
        
        with self.assertRaises(JobOpening.DoesNotExist):
            JobOpening.objects.get(pk=jo_pk)
    
    def test_list_JobOpening(self):
        expected_obj = JobOpening.objects.all()
        expected = [x.pk for x in expected_obj]
        
        response = self.client.get("/recruit/jobopening/list/",
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        # print(json.dumps(response.data.get("data"), ensure_ascii=False))
        result = [x.get("id") for x in response.data.get("data")]
        result.sort()
        
        for res, expect in zip(result, expected):
            self.assertEqual(res, expect)
    
    def test_search_JobOpening(self):
        # '원티드' 검색결과
        expected = [self.job_opening1.pk, self.job_opening2.pk, self.job_opening3.pk]
        expected.sort()
        
        response = self.client.get("/recruit/jobopening/list/?search=원티드",
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = [x.get("id") for x in response.data.get("data")]
        result.sort()
        
        for res, expect in zip(result, expected):
            self.assertEqual(res, expect)
        
    def test_search_JobOpening2(self):
        # 'Django' 검색결과
        expected = [self.job_opening4.pk, self.job_opening5.pk]
        expected.sort()
        
        response = self.client.get("/recruit/jobopening/list/?search=Django",
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = [x.get("id") for x in response.data.get("data")]
        result.sort()
        
        for res, expect in zip(result, expected):
            self.assertEqual(res, expect)
    
    def test_detail_JobOpening(self):
        jo_pk = self.job_opening1.pk
        
        expected_other = [self.job_opening2.pk, self.job_opening6.pk, self.job_opening7.pk]
        expected_other.sort()
        
        response = self.client.get(f"/recruit/jobopening/{jo_pk}/",
                                   content_type='application/json')
        
        result = sorted(response.data.get("data").get("other_opening"))
        print(result)
        
        for res, expect in zip(result, expected_other):
            self.assertEqual(res, expect)
        