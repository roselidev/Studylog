Express 알아보기  
==============

Node.js에서 사용할 수 있는 Web Framework 중 가장 인기있는 Express에 대해 알아보자
--------------

Express는 Fast, Minimalist, **Unopinionated** 를 표방하는 오픈소스 **라우팅** 및 **미들웨어** 프레임워크이다. Express는 왜 중요하고, 어떤 일을 하는지 알아보자.

---
이 문서는 Express [공식가이드](https://expressjs.com/)문서를 참조하여 작성하였음.  
  
이 문서는 독자가 [Node](https://github.com/roselidev/Studylog/blob/master/Node.js/Node01.md)를 이미 알고있다는 전제 하에 작성하였음.
  

---
  
## Terminology  
  
  
- ### Unopinionated?  
  어떤 Software가 Opinionated라는 말은, 그 Software를 사용하는 방식이 엄격하게 정의되어 있다는 뜻이다.  
    
  예를 들어 Framework가 Opinionated라면 Framework의 사용법을 철저히 숙지해야만 그 Framework를 쉽게 사용할 수 있을 것이다.
    
  그렇다면 Express가 Unopinionated한 Framework라는 말은?  
  즉, 자유도가 타 소프트웨어에 비해 높다는 뜻으로 해석할 수 있을 것이다.
  
- ### Router?
  https:/???.com/ 이라는 웹사이트에 들어가 여기저기 돌아다니다 보면, 주소창의 url이  
  https:/???.com/main/category/subcategory/ 와 같은 식으로 늘어나는 것을 본 적이 있는가?  
  여기서 위의 url을 **root url**,  
  root url 뒤에 붙은 여러 태그를(/main, /category, /subcategory) **endpoint**라 한다.  


    Routing이란 클라이언트가 이러한 endpoint로 리퀘스트를 보낼 때 어떻게 응답할지를 정의하는 것이다.  
    즉, request의 **루트Route**를 정해주는 것이다.  
    Express에서는 `apt` 오브젝트를 이용하여 라우팅을 정의한다.  

- ### MiddleWare?  
  미들웨어의 일반적인 정의는 소프트웨어 사이에 위치하는 소프트웨어이다.  
  Express MiddleWare는 약간 의미가 다른데, Client의 Request가 서버로 들어와 특정 업무를 수행하고 빠져나가는 한 주기 동안 수행되는 일련의 함수들을 말한다.  
  따라서 Express Application이라고 하면 본질적으로 여러 Express MiddleWare를 호출하는 일련의 동작을 말하는 것이다.  
  MiddleWare라고 하는 이유는 요청(Request) - 응답(Response) 중간에 있는 함수이기 때문인 듯..
    
  미들웨어 여러 개를 chaning할 수도 있는데, 다음 미들웨어로 Request를 넘길 때 `next()`함수를 이용한다고 한다.  
    
  Express 미들웨어에는 몇가지 종류가 있으니, 바로 아래와 같다. 
   
  | 구분 | 설명 |
  |------------------|---------------------|
  |Application_level | `app.use()`를 이용한 가장 기본적인 미들웨어 타입으로, next()로 chaining되고 순차적으로 수행됨 |
  |Router_level | API는 App_level과 비슷하고 다만 `express()`가 아닌 `express.Router()`로 생성되며 App_level의 인자로 들어갈 수 있음. |
  |Error-handling| 다른 종류의 미들웨어와 달리 err 인자까지 총 4개 인자를 가짐 (`app.use( function ( er, req, res, next ))`) |
  |Third-party| 자유도 보장을 위해 필요한 모듈을 [여기](https://expressjs.com/en/resources/middleware.html)서 추가로 받을 수 있다고 함|
  |Built-in| 내장함수로 Express 4.xx부터 [express.static](https://expressjs.com/en/4x/api.html#express.static), [express.json](https://expressjs.com/en/4x/api.html#express.json), [express.urlencoded](https://expressjs.com/en/4x/api.html#express.urlencoded)가 있음|
    
  ---  
    


- ### Template Engine?
  템플릿 엔진을 사용하여 템플릿 파일을 사용할 수 있다.  
    
  템플릿 파일은 화면 구성요소와 함께 변수를 함께 정의하고 있고,  
  엔진을 이용하여 runtime 동안 각 변수에 적절한 값을 넣어준다.  
    
  유명한 템플릿 엔진에는 [Pug](https://pugjs.org/api/getting-started.html), [Mustache](https://www.npmjs.com/package/mustache), [EJS](https://www.npmjs.com/package/ejs)가 있음.

  사용법은 [여기](https://expressjs.com/en/guide/using-template-engines.html)
    
  

