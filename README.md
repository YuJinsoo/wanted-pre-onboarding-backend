# wanted-pre-onboarding-backend

## 구글 드라이브 링크

https://drive.google.com/drive/folders/1ANS4cwSHVE3ZNE1slgCcPEsbHseR6BUg?usp=sharing

## 과제
### 사용 기술
- Python을 사용했고 Django(DRF) 를 사용해 개발했습니다.
- Djanog ORM과 SQLite3(Django 기본)을 이용했습니다.

### 모델링
- 예시에 표현된 자료를 모두 표현하고자 하도록 모델링했습니다.
- JopOpening이라는 테이블로 공고의 정보를 표현하도록 했습니다.
- 회사의 경우 Company라는 다른 테이블로 생성해 확장성을 고려했습니다.
- User의 경우 지원한 공고를 확인할 수 있도록 column을 추가했고, 여러군데에 지원할 수 있으므로 ManyToMany로 JobOpening 테이블과 관계를 표현했습니다.


### Unit Test 구현
- 명령어는 아래와 같습니다.
```shell
python manage.py test

python manage.py test recruit.tests.TestCase.
python manage.py test recruit.tests.TestCase.test_create_JobOpening
python manage.py test recruit.tests.TestCase.test_update_JobOpening
python manage.py test recruit.tests.TestCase.test_delete_JobOpening
python manage.py test recruit.tests.TestCase.test_list_JobOpening
python manage.py test recruit.tests.TestCase.test_search_JobOpening
python manage.py test recruit.tests.TestCase.test_search_JobOpening2
python manage.py test recruit.tests.TestCase.test_detail_JobOpening
python manage.py test recruit.tests.TestCase.test_apply_JobOpening
```