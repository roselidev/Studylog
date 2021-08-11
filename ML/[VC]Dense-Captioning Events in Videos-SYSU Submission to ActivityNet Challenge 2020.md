# Dense-Captioning Events in Videos: SYSU Submission to ActivityNet Challenge 2020

[2nd place in ActivityNet Challenge 2020]  
[codebase](https://github.com/ttengwang/dense-video-captioning-pytorch)  

## Abstract
우리의 접근 방식은 2 stage pipleline을 따른다.  
첫째로, 일련의 시간적 event 후보를 추출한다.  
그런 다음, multi-event captioning model로 event 단위의 시간적 관계와 multi-modal information을 융합한다.  
우리의 접근 방식은 9.28 METEOR 스코어를 달성하였다.  

## Introduction
Dense video cationing은 무편집 비디오 내의 모든 이벤트를 특정하고 설명하는 것을 목표로 하며, 최근 점점 더 많은 관심을 받고 있는 분야이다.  
한 영상 당 하나의 설명만을 생성하는 전통적인 video cationing 분야와 달리, dense video cationing은 장기간의 시계열 구조와 일련의 이벤트 속의 의미적 관계를 통합적으로 이해해야 한다.  

이전의 연구들은 각기 다른 종류의 context를 도입하여 event를 표현하였다. 예를들면, <>는 확장된 수용 공간 속에서 이웃하는 구간을 이용하였다. <>는 이벤트 수준의 semantic attention을 이용하였다.  <>는 클립 수준의 recurrent feature를 이용하였다.  

비록 굉장한 발전이 이루어졌지만, 위 모델들의 context modelling은 event sequence의 시간적 구조를 고려하지 않고 있다.  
즉, 다른 이벤트의 시간적 배치와 길이를 고려하지 않는다.  
따라서, 이벤트간의 시간적 관계 정보가 captioning stage에서 충분히 이용되지 못한다.  
본고에서 우리는 인코딩 단계에서 이벤트간의 시간적 관계를 탐색하는 방법을 제안한다.  
더하여, 우리는 계층적 RNN 구조에서 사용할 수 있는 cross-modal gating (CMG) 모듈을 고안하여, 더 나은 caption 생성을 위하여 언어 정보와 시각 정보간의 가중치를 점진적으로 조정할 수 있도록 하였다.   
