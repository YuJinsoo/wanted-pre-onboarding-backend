import json
from django.test import TestCase

# from rest_framework.test import APIClient
# from rest_framework.authentication import SessionAuthentication

from .serializers import JobOpeningSerializer, CompanySerializer
from .models import JobOpening, Company

class TestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.company1 = Company.objects.create(name="testCompany1")
        cls.company2 = Company.objects.create(name="testCompany2")
        
        data = {
            "company": cls.company1,
            "position":"백엔드 주니어 개발자",
            "reward":1000000,
            "content":"원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "tech":"Python"
        }
        
        cls.job_opening1 = JobOpening.objects.create(**data)
    
    def test_create_JobOpening(self):
        company = Company.objects.create(name="원티드")
        
        expected = {
            "company": company.id,
            "position":"백엔드 주니어 개발자",
            "reward":1000000,
            "content":"원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "tech":"Python"
        }
        
        response = self.client.post("/recruit/jobopening/",
                                    data=json.dumps(expected),
                                    content_type='application/json')
        
        result = response.data.get("data")
        
        self.assertEqual(result["company"], expected["company"])
        self.assertEqual(result["position"], expected["position"])
        self.assertEqual(result["reward"], expected["reward"])
        self.assertEqual(result["content"], expected["content"])
        self.assertEqual(result["tech"], expected["tech"])
    
    
    def test_update_JobOpening(self):
        print(self.job_opening1)
        
        expected = {
            "position":"백엔드 주니어 개발자",
            "reward":1000000,
            "content":"원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..",
            "tech":"Python"
        }
