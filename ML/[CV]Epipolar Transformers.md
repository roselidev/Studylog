# Epipolar Transformers

## Abstract
synchronized & calibrated 다시점 카메라 환경에서 3D 자세 좌표를 특정하기 위한 흔한 방법 중 하나는 two-step 접근방식이다.  
1) 2D detector를 각 시점(카메라)마다 적용하여 2D 좌표를 뽑아낸다.  
2) robust triangulation을 1)에 적용하여 3D 좌표를 계산한다.  

그러나 1)의 2D detector는 3D 정보를 이용하지 않으므로, 가림 문제나 비스듬한 시야각 등 잠재적으로 3D에서 더 잘 해결될 가능성이 있는 어려운 경우에서는 제한적이다.  

따라서 우리는 미분 가능한 "epipolar transformer"를 제안하여 2D detector가 3D-aware feature를 이용하여 2D pose estimation을 개선할 수 있음을 보이고자 한다.  

우리의 직관적인 메시지는 이렇다.  
 > "특정 시점의 2D 위치 p에 대하여, 이웃하는 시점의 상응하는 위치 p'를 찾아낸 다음, p'와 p를 합쳐 p 위치의 3D-aware feature를 얻을 수 있다.  

stereo matching에 영감을 받은 epipolar transformer는 epipolar constraints와 feature matching을 이용하여 p'의 feature 값을 근사할 수 있다.

InterHand와 Human3.6M 데이터셋에 대하여 실험한 결과 baseline에 대한 일관적인 개선 효과를 보였다.  
특히 외부 데이터를 전혀 이용하지 않은 상황에서도, ResNet-50 backbone, image size 256*256, Human3.6M으로 훈련된 모델이 SOTA 성능을 4.23mm 차이로 능가하여 MPJPE 26.9mm 를 달성하였다.  

## Introduction
사람의 신체부위나 손을 추정하기 위하여 사용되는 두 가지 방식은 크게 첫째, 단일 이미지로부터 자세를 바로 추정하는 단시점 3D 자세 추정 방식과 둘째, 동기화된 캘리브레이션 된 여러 이미지를 사용하여 depth ambiguity 문제를 해결할 수 있는 다시점 3D 자세 추정이다.  

두번째 방식을 구현하기 위해 흔히 차용하는 프레임워크는, (1) 기존 2D 자세 추정 모델을 이용하여 2D로 자세를 추정한 후 (2) 카메라 캘리브레이션 및 각 시점의 2D 자세를 이용하여 3D 자세를 robust한 삼각측량법으로 계산하는 것이다.  
이 때 robust 삼각측량법을 사용하는 이유는 2D 추정기가 추정한 자세가 가림 문제 등으로 인하여 틀릴 수 있기 때문이다.  
이 프레임워크의 주요 문제점 중 하나는 (1)번째 단계에서 모든 시점이 각각 독립적으로 2D 자세를 추정하고, 다른 시점의 정보는 이용하지 않는다는 것이다.  
이로 인해 3D 자세 추정에서 균일하지 않은 2D 자세가 추정될 수 있으며, 이를 해결하기 위해 더 많은 학습 데이터가 요구된다.  

본고에서는 이에 대해, 미분가능한 "epipolar transformer"라는 모듈을 제안하여, 2D 자세 추정 모델이 모델 내부에서, 그리고 마지막 robust 삼각측량 과정 뿐 아니라 다른 단계에서도 3D 자세 정보에 접근할 수 있는 방법을 제시한다.  
epipolar transformer는 2D 자세추정 과정에서 특정 시점 이미지의 중간 feature를 이웃 시점들의 feature를 이용하여 증강함으로써 중간 feature가 3D-aware한 특성을 가지도록 한다.  

![image](https://user-images.githubusercontent.com/48943581/124526917-16b1f780-de3f-11eb-8c2a-4f29c1a3d9fc.png)

특정 시점 이미지 상의 위치 p에 있는 3D-aware한 중간 feature를 만들기 위하여, 이웃 시점에서 p에 상응하는 위치인 p'를 찾는다. 그리고 p'에 있는 feature를 p의 feature와 fuse하여 3D-aware feature를 만든다.  
이 때, 문제는 p'가 어디인지 알 수 없으므로 epipolar line을 이용하여 p'의 잠재 위치를 찾고, 해당 잠재 위치 내의 feature들과 유사도를 계산하여 유사도를 가중치로 모든 잠재 p' 후보의 가중합을 구한다.  
p와 p' 위의 features를 fuse하기 위해 non-local networks에서 영감을 받은 여러 방법을 사용하였다.  

epipolar transformer는 미분가능하며 input 및 output feature의 dimension이 같기 때문에 2D 자세 추정기의 어느 부분에든 삽입될 수 있으며 훈련이 가능하다.    
Human36M에서 26.9mm 달성 (ResNet-50, 256x256)  

epipolar transformer의 장점은 다음과 같다.  
1. 기존 네트워크 아키텍처에 어디든지 삽입 가능  
2. 학습 파라미터가 적음 (입력 feature channel size를 C라고 할 때, 파라미터 수는 CxC)  
3. 검증 가능 (similarity 직접 계산하여 검증 및 해석 가능)  
4. 카메라 파라미터만 있다면 학습 데이터에 없던 새로운 카메라 환경에도 일반화 가능  
