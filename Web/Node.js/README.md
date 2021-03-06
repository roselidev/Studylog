Node.js 알아보기  
==============

웹개발에서 가장 베이직한 도구 중 하나인 Node.js를 공부해보자.  
--------------

노드는 Django나 Flask처럼 쉽고 간단한 API를 제공하지는 않지만, Node.js를 공부하면서 http 구조라던가, 웹사이트가 어떻게 만들어지는지에 대해 더 깊은 이해를 하고자 한다.  

---
이 문서는 w3schools.com의 [Node.js 튜토리얼](https://www.w3schools.com/nodejs/)문서를 참조하여 작성하였음.  


---
## What is Node??  
---

Node.js는 JavaScript 언어로 쓰는 Runtime Environment로, 웹 애플리케이션을 만드는 환경을 제공한다.  
[공식 홈페이지](https://nodejs.org/en/about/)에서는 **Asynchronous event driven JavaScript runtime**라고 Node를 소개하고 있으며,  Node는 *scalable network applications*를 구축하기 위해 만들어졌다고 한다.  
  
Asynchronous, event, runtime, scalable ... 이게 다 무슨 뜻일까? 하나하나 뜯어보자.  
  
  
### Asynchronous, 비동기 방식
  
비동기적 방식이란, 시간이 걸리는 작업들을 기다려주지 않고 처리하는 방식을 말한다.  
보통 시간이 걸리는 작업이란 I/O 작업을 가리킨다.  
  
예를 들어 카페에서,
  

*아메리카노 한 잔 주세요.*  
*카페라떼 두 잔 주세요.*  
*캬라멜 마끼아또 한 잔 주세요.*  
  

라는 오더를 받았을 때 두가지 방식으로 처리할 수 있다.  
  
1. 첫번째 주문한 커피가 나올 때까지 두번째 주문을 받지 않는다.  
1. 한 명은 주문만 받고 한 명은 커피만 만든다.
  
동기적 방식이란 1번을 이야기하는 것이다.  
즉 새로운 입력이 들어오기 전에 현재 상태가 latest update상태여야 한다는 것이고,  
비동기적 방식은 그와 달리 I/O 작업을 기다려주지 않고 계속해서 주문을 받아들이는 것이다.  
  
### Event Driven, 이벤트 위주 프로그래밍
  
이벤트란 말그대로 Node가 감지하는 모든 일을 말한다. 대표적으로는 Button Click, Http호출이 있다.   
기존의 프로그래밍 언어들은 Sequential Processing, 즉 먼저 호출한 함수가 먼저 수행되는 형태를 지니고 있다.  
  
예를 들어,  
```
(...)
int main void(){

(...)

firstFunction();
secondFunction();

(...)
}
```
이런 코드가 있으면 `firstFunction()`이 먼저 수행된 후 `secondFunction()`이 수행될 것이라는 예측을 할 수 있다.  
  
하지만 이렇게 하면 사용자는 프로그래머가 원할 때만 Input을 넣는 등의 동작을 할 수 있다.  
  
만약 사용자가 원하는 때에 원하는 동작을 할 수 있도록 하려면 어떻게 해야할까?    
특정 동작을 미리 정의하는 것이 아니라, 사용자의 요구에 따라 그 때 그 때 다른 응답을 보내야 할 것이다.  
이러한 이유로 *버튼을 클릭하면 이 함수를 호출하라* 는 식의 *Event Driven Programming*이라는 개념이 생겨났다고 이해할 수 있다.  
  
### Runtime, 런타임 환경  
  
Node 입문자들이 가장 많이 하는 오해 중 하나가 'Node.js가 웹서버다'라는 오해라고 한다.  
Runtime이란 쉽게 말해 프로그램이 돌아가는 '곳',  
즉,  
환경 그 자체를 말한다.  
  
정리하면,  
  
- Runtime Environment는 메모리(RAM)에 접근하고,  
- CPU에 Instruction을 보내고,  
- 프로그램에 오류가 나면 Debugging할 수 있도록 정보를 제공한다.
- **OS가 달라져도 프로그램이 동작할 수 있는 환경을 제공한다.**
  
이 일련의 동작은 우리가 프로그램을 작성할 때에는 명시적으로 정의하지 않는 동작이고,  
RTE(Runtime Environment)위에서 프로그램을 돌리면 RTE가 대신해서 이 동작들을 수행해주는 것이다.
  
IDE를 이용하지 않고 command창에서 바로 프로그램을 돌릴 때를 생각해보면, 쉽게 이해가 될 것이다.  
command창에서 프로그램을 돌리면 프로그램에 명시된 결과가 나오거나 Error메시지가 뜰 것이다.  
그 이후에 에러메시지에 대하여 Tracking과 같은 동작은 불가능하다.  
이는 IDE 내장 RTE위에서 프로그램을 돌릴 때와 OS를 바로 RTE로 이용하는 것 사이의 차이를 보여준다.  
물론 Runtime Environment가 에러메시지만 관리하는 것은 아니고 실제로는 OS와 프로그램 사이를 이어주는 역할을 한다.  
  
비유하자면 초석, 토대, 양탄자... 같은 느낌. ..?
  
  
***
  
  

[JAVA](https://www.javaworld.com/article/3304858/what-is-the-jre-introduction-to-the-java-runtime-environment.html)에서는 JRE(Java Runtime Environment)에 대하여 이렇게 이야기한다.  

  
---
    
>a **runtime environment** is **a piece of software** that is designed **to run other software.**
  
  
*Runtime Environment는 다른 소프트웨어를 돌리기 위한 소프트웨어이다.*  
  
  
>In the past, most software used the **operating system (OS)** as its runtime environment.  
  
  
*예전에는 대부분 OS를 runtime environment로 이용하여 소프트웨어를 돌렸다. (즉, OS위에 바로 돌렸다)*  
  
  
>The program ran inside whatever computer it was on, but relied on operating system settings for resource access. Resources in this case would be things like memory and program files and dependencies. The Java Runtime Environment changed all that, at least for Java programs.  
  
  
*따라서 프로그램은 리소스를 access할 때 OS세팅에 의존할 수 밖에 없었고(즉 컴퓨터간 이동이 불편했고), JRE가 이러한 한계를 극복하였다.* 
  
---
  
### Scalable, 확장성  
  
Scalable이라는 단어를 살펴보면 Scale을 정할 수 있다라는 뜻으로 이해할 수 있다.  
명사에 able이라는 단어가 붙어서 생소하기도 하고, 비슷해보이는 Sizable(quite big)과도 다른 의미라서 헷갈릴 수 있다.
꼭 확장성이라는 단어로 이해하기보다는, able to set scale 즉 scale이 작아지거나 커지더라도  
문제가 발생하지 않는다는 의미로도 이해할 수 있을 것이다.  
