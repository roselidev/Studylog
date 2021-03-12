# [Learnable Triangulation of Human Pose](https://arxiv.org/pdf/1905.05754v1.pdf)

Karim Iskakov, Egor Burkov, Victor Lempitsky, Yura Malkov, Samsung AI Center (Moscow), Skolkovo Institute of Science and Technology (Moskow)  

## Abstract


multi-view 3D human pose estimation에 대한 두 가지의 새로운 솔루션을 제안한다.  
이 둘은 여러 개의 2D view로부터 3D 정보를 합성하는 새로운 Learnable Triangulation 방법을 기반으로 한 방법이다.  
첫번째 baseline 솔루션은 미분 가능한 기본 대수 삼각 분할로서, 입력 이미지로부터 신뢰 가중치(confidence weights)를 추가한 것이다.  
두번째 솔루션은 intermediate 2D backbone feature map 에서 새로운 체적 집계 방법을 기반으로한다.  
집계된 볼륨은 3D convolutions를 거쳐 최종 3D joint heatmap을 생성하고 사전 human pose modelling을 돕는다.  
여기서 중요한 점은 위 두 방법 모두 end-to-end, 종단간 미분 가능한 방법이며, 이로인해 target metric을 직접적으로 최적화 할 수 있게 된다.  
본 연구는 Humans3.6M dataset에서 SOTA 성능을 달성하였다.  


## Introduction

현재까지 대부분의 연구는 monocular 3D pose estimation에 치중되어 있다.

> :question: [monocular](https://snacky.tistory.com/96)란 통상적으로 하나의 카메라(mono-view)만을 이용했다는 뜻이며 2개 이상의 카메라를 이용할 시 stereo라고 이른다.



