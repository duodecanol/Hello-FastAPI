# GET TO KNOW FASTAPI

FASTapi 알아가기. 2주정도 짬짬이 살펴본 것들을 적었습니다.

## 작업시 장점

* API document 생성 편리
  * 
* 강력한 DI system
  * `Depends()`
* Parameter-based API endpoint construction

## 일반적인 장점

* Django에 비해서 NoSQL database (MongoDB, Cassandra, etc) 연동이 용이한 점
* Django도 async가 불가능하지 않다고는 들었으나, FastAPI는 뼛속부터 `asyncio`로 되어있어 I/O 측면에서 많은 속도향상이 있다고 함. 

## DRF와 비교할만한 점
* DRF의 `ModelViewSet` 등은 endpoint 작성시에 코딩량을 많이 줄여줬는데 그와 비슷한 점은 보이지 않음
* 단, DRF에서는 `Serializer`를 별도 구성하는데, 그 수고를 덜 수 있음
* 그렇지만, DRF에서는 `Serializer`를 통해 response에 담길 field의 value에 상당히 다채로운 옵션을 줄 수 있었는데, 아직까지 이에 대해 상세히 기술한 문서를 보지 못함.
  * 예를 들어, DRF에서는 아래와 같은 field 구성을 즐겨 썼는데 FastAPI 식의 구성은 어떨지 궁금.
    * [HyperlinkRelatedField](https://www.django-rest-framework.org/api-guide/relations/#hyperlinkedrelatedfield)
    * [Nested Relationships](https://www.django-rest-framework.org/api-guide/relations/#nested-relationships)
* Django ORM과는 다르게 SQL Alchemy를 쓰면서 차이점이 보임
  * Migration할 때에는 Django ORM이 보다 편리했다고 느껴짐. FastAPI에서는 Alembic을 사용해서 SQLlite로 마이그레이션하는데 손이 많이감
  * Entity Column 구성하는 문법에서 차이가 보이는데 아무래도 Django가 익숙해서 그런지 이질감이 느껴지고 친절하지 않다고 느껴짐.  많이 쓰다보면 개선될 듯.
  * 테이블의 상세사양이 구성된 Schema와 Type hinting을 위한 Model을 각각 상응하게 업데이트해나가야 함 이것이 장점인지 단점인지 판단하려면 더 많은 경험이 필요

## 하위 프로젝트 설명

학습용으로 하고있어 폴더구성에 큰 의미는 없습니다.
* /ChristopherGS
  * 자상한 Christopher의 FastAPI tutorial
  * https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-11-dependency-injection/
* /FastAPITutorials
  * [FastAPI 공식문서](https://fastapi.tiangolo.com/)의 튜토리얼