# [Learnable Triangulation of Human Pose](https://arxiv.org/pdf/1905.05754v1.pdf)
의역 및 오역 다수

## Abstract


다시점 3D human pose estimation에 대한 두 가지의 새로운 솔루션을 제안한다.  

이 둘은 여러 개의 2D view로부터 3D 정보를 합성하는 새로운 Learnable Triangulation 방법을 기반으로 한 방법이다.  

첫번째 baseline 솔루션은 미분 가능한 기본 대수 삼각 분할로서, 입력 이미지로부터 신뢰 가중치(confidence weights)를 추가한 것이다.  

두번째 솔루션은 intermediate 2D backbone feature map 에서 새로운 볼륨 집계 방법을 기반으로한다.  

집계된 볼륨은 3D convolutions를 거쳐 최종 3D joint heatmap을 생성하고 사전 human pose modelling을 돕는다.  

여기서 중요한 점은 위 두 방법 모두 end-to-end, 즉 종단간 미분 가능한 방법이며, 이로인해 target metric을 직접 최적화 할 수 있게 된다는 것이다.  

본 연구는 Humans3.6M dataset에서 SOTA 성능을 달성하였다.  


## Introduction

### 카메라 한 대 말고 여러 대를 쓰자
현재까지 대부분의 연구는 단시점 자세 측정(monocular 3D pose estimation)에 치중되어 있다.

> :question: [monocular 3D human pose estimation](https://link.springer.com/10.1007%2F978-0-387-31439-6_584)란 통상적으로 하나의 모노 이미지(monocular image)에서 3D 자세 정보를 추출하는 것을 이른다.  
c.f) 스테레오 이미지란 카메라 2개로 촬영된 이미지이다.

그러나 실무에서는 단시점 자세 측정은 사용하기에 문제가 많다.  

이에 다시점 자세 측정(multi-view human pose estimation)이 흥미로운 이유를 두 가지 들어보자면,


1. 다시점 자세 측정은 단시점 자세 측정의 실제 정답 값(ground truth)을 얻기 위한 가장 좋은 방법이다.  
왜냐하면 다시점 자세 측정의 경쟁 기술이라고 할 수 있는 마커 기반 모션캡처(marker-based motion capture)와 관성 센서 기법(visual-inertial method)은 다양한 의상과 풍부한 자세 표현을 캡처하는데에 한계가 있기 때문이다.  
다만 다시점 자세 측정의 단점은 이전 연구들이 multi-view triangulation 데이터셋을 구축할 때 과도한, 거의 불가능한 수의 view (camera)를 이용하여 양질의 3D 정답값을 구하였다는 점이다.  
이 방법으로 실무에서 쓰일 수 있는 새로운 3D pose estimation 데이터셋을 구축하는 것은 매우 도전적이며, 따라서 정확한 triangulation을 통해 view의 수를 몇 대 수준으로 줄일 수 밖에 없다.  

2. 다시점 자세 측정이 흥미로운 두 번째 이유는 몇몇 제한된 환경에서 실시간 자세 측정이 가능하기 때문이다.  
이것이 가능한 이유는 여러 대의 카메라를 이용하는 환경이 실생활에서 점진적으로 증가하고 있기 때문이다. 예를들면 스포츠 경기 또는 장애인 컴퓨터 보조 기기 등이 있다.  
이러한 상황에서 현대의 다시점 기법의 정확도가 기존 잘 연구된 단시점 기법의 정확도에 비견할 정도로 성장하고 있다.  

본고에서는 다시점 자세 측정이 그 중요성에 비해 거의 관심을 받지 못하고 있음을 주장하는 바이다.  
본고는 두 가지의 연관된 기법을 사용하여 다시점 자세 측정을 제안하고 연구하였다.  
두 방법 모두 learnable triangulation, 학습가능한 삼각측량법을 사용한다.  
학습가능 삼각측량법을 이용하면 3D 자세를 정확히 측정하기 위해 필요한 카메라(view)수를 현저히 줄일 수 있다.  
학습 과정 중에 우리는 마커 기반 모션 캡처로 얻은 정답값 또는 과도한 수의 view를 사용하여 얻은 메타 정답값(meta ground truth)을 사용하였다.  

두 방법은 다음과 같다.  
1. camera-joint confidence weights를 학습매개변수로 한 대수 삼각측량법 접근으로 더 간단한 방법.
2. 정보의 밀도 분포에 대한 기하학적 집계에 기반한 볼륨 삼각 측량 접근 방식으로 더 복잡하지만 modelling a human pose prior이 가능한 방법.  
중요한 점은 두 방법 모든 과정에서 완전히 미분가능하다는 것이다.

지금부터 단시점 및 다시점 자세 측정에 관한 관련 연구를 리뷰한 다음, 본고의 연구에 대해 자세히 이야기 하도록 하겠다.

본고의 실험 파트에서, 우리는 유명한 데이터셋인 Humans3.6M 및 CMU Panoptic 데이터셋을 사용하였으며, 제안한 기법을 이용하여 SOTA 성능 및 범데이터셋 일반화 가능성을 보였다.

## Related Work

### Single view 3D pose estimation
현재 단시점 3D 자세측정 분야의 SOTA 기술은 크게 두가지로 분류할 수 있다.  
1. 고화질 2D 자세측정 엔진에서 추출한 2D 좌표를 심층신경망을 통해 3D 좌표로 개별 변환하는 것이다.  
이는 < A simple yet effective baseline for 3d human pose estimation > 논문에서 대중화되었으며  
간단하고, 빠르고, 모션캡처 데이터로 훈련할 수 있으며 훈련 후에 2D 백본 엔진을 교체할 수 있다는 장점이 있다.
2. 컨벌루션 신경망을 사용하여 2D 이미지에서 직접 3D 좌표를 추출하는 것이다.  
현존하는 가장 좋은 솔루션은 < Integral human pose regression >로 자세의 volumetric representation을 이용한다.  
이는 Humans3.6M의 single-frame SOTA 결과와 함께 가장 좋은 솔루션으로 꼽힌다.

### Multi-view view 3D pose estimation
