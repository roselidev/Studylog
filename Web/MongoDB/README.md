MongoDB 알아보기
===
기존의 RDB(Relational DataBase)가 아닌 대표적인 **NoSQL** DB로서, **document data model**을 차용한 **분산 시스템** 오픈소스 DBMS MongoDB를 공부해보자.

---
- ## Terminology
  - ### NOSQL
    - **"Not only SQL"** 
    - 관계형 DB *(=RDB, 대표적으로 엑셀)* 에서 쓰이는 문법인 SQL의 기능 뿐 아니라 다른 기능도 지원한다는 의미
    - RDB가 보장하는 ACID(Atomicity, Consistency, Integrity, Durability)를 보장하지 않을 수도 있지만 성능이나 확장성이 뛰어나 특히 **대용량 데이터 처리**에 자주 사용됨  

    - 또한 최근 각광받는 **비정형데이터**(사진, 음성, SNS 텍스트 등) 처리에도 유용함

    |NoSQL 구분|설명|실례|
    |-------------|-------------------|----------------------|
    |Key-Value DB | Key-Value 데이터구조 채택 | Amazon-DynamoDB, Oracle-BerkeleyDB 등|
    |Wide Columnar Store | Two-dimensional Key-Value 구조로 Table 형태 구현 | Google-BigTable, ScyllaDB|
    |DocumentDB| Json, XML같은 Collection 데이터구조 채택 | **MongoDB** 등|
    |GraphDB| Node, Relationship, Key-Value 데이터구조 채택 | OreientDB 등| 
  - ### Document Database
    - MongoDB의 기본 데이터 구조는 `document`이다. json과 비슷하게 생겼다.
    ```
    {
        name : "sue",
        age : 26,
        status : "A",
        groups : [ "news" , "sports" ]
    }
    ```
    - Document data type의 장점은 다음과 같다.  
      1. Document 자체를 Data type으로 쓸 수 있다.
      2. Document 타입을 사용하면 [RDB의 Join Operation을 이용할 필요 없이 낮은 Cost로 원하는 업무를 수행할 수 있다.](https://stackoverflow.com/questions/2350495/how-do-i-perform-the-sql-join-equivalent-in-mongodb)
      3. 유동적인 스키마로 다형성이 보장된다. 
  - ### 분산 시스템
    - [Zone](https://docs.mongodb.com/manual/core/zone-sharding/#zone-sharding)이라는 구획을 사용하여 horizontal scalability 보장  
    (시스템이 더 많은 **컴퓨터**를 사용하여 확장 가능. <-> vertical scalability = 더 좋은 RAM, CPU 등 Power를 업그레이드하여 확장 가능)
- ## Language
  - ### MongoDB의 Query Language로
    - CRUD (Data I/O)
    - Data Aggregation
    - Text search
    - Geospatial Queries  
    
    작업을 수행할 수 있다고 한다.   
    
