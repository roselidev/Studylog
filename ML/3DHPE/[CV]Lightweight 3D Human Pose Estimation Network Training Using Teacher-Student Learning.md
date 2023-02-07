# Lightweight 3D Human Pose Estimation Network Training Using Teacher-Student Learning

## Abstraction 
MovNect 는 단안 RGB 카메라를 이용한 3D 자세 측정을 위한 경량 심층신경망이다.  
모델의 성능 개선을 위해, 우리는 teacher-student learning 기반의 지식 추출 기법을 이용하였다.  
실시간 후처리를 통해 CNN 결과값이 일시적으로 안정적인 3D 골격 정보를 생성하게 하여, 응용 프로그램에 곧바로 사용할 수 있도록 하였다.  
우리는 모바일용 실시간 3D 아바타 어플리케이션을 만들어 우리의 모델이 정확도와 속도 모두를 상당수준 달성하였음을 보였다.  
Extensive evaluation을 통해 우리의 경량 모델이 모바일 환경 및 Human3.6M 데이터셋에서 우위를 가짐을 보였다.  

## Introduction
최근 자세 측정 분야는 sports analyctics, 자세 및 제스쳐 동작 캡처, AR 및 VR 분야에서 많은 발전을 보였다.  
AR의 경우 따로 하드웨어 장비가 필요하지 않기 때문에 더더욱 관심을 받고 있다.  
그럼에도 불구하고, 여전히 양질의 AR/VR 컨텐츠를 만들기 위해서는 특정 환경 및 하드웨어 장비가 필요하다.  
기존 모션 캡처 시스템은 마커 기반의 여러 센서가 달린 착장과 depth camera를 필요로 하였다. (Microsoft Kinect, Intel RealSense)  
이 방법은 특수장비가 필요하기 때문에 비쌀 뿐만 아니라 claibration 및 조명 문제로 실내 환경에 제한되어 있다.  
최근 딥러닝을 이용하여 RGB 이미지만을 이용한 연구가 비약적으로 발전하였다.  
그러나, 높은 성능을 위해서는 레이어의 크기와 갯수가 많아지기 때문에 비용 또한 증가한다.  
이는 FLOPS(FLoating point OPerations per Seconds)를 증가시키며 컴퓨팅 리소스가 제한적인 모바일 디바이스나 임베디드 환경에서는 사용하기 어렵다.  
FLOPS를 줄이기 위해, 더 적은 수의 파라미터로 효율적으로 동작하는 경량모델이 연구되며 한 예로는 depthwise convolutions가 있다.  
그러나, 축소된 양의 파라미터는 모델 정확도에 영향을 미친다.  

본고에서, 우리는 성능 손실이 가장 적으면서 파라미터 수를 효율적으로 줄일 수 있는 학습 방법을 소개하고자 한다.  
우리는 2D HPE 모델 학습 방법을 확장하여 MoVNect라는 경량 3D 자세 측정 모델을 구현하였다.  
본고에서 소개한 방식으로 훈련된 이 모델이 기존 방식으로 훈련될 때보다 높은 정확도를 달성함을 보였다.  

## Related Works
- 2D HPE  
    처음에는 CNN을 이용하여 직접적으로 joint 좌표를 추출하였으나, 이후 히트맵 산출 방식이 제안되었고, 더 높은 성능을 보였다. 대부분의 후속 연구에서 heatmap regression-based method 가 사용된다.  
- 3D HPE  
    3D HPE 문제는 기본적으로 z축이 이미지 상에 나타나지 않는 under-constrained 문제를 가지고 있다.  
    대부분의 연구는 CNN을 이용하여 two step 방식을 채택한다. 즉,  
    (1) 2D 조인트를 계산하고,  
    (2) 해당 2D 조인트값을 2D로 lift한다.  
    이는 구현하기가 쉽지만 3D 결과값이 2D 값에 크게 의존한다는 문제가 있다.  
    또한 CNN 레이어 결과값의 공간정보를 활용하지 않기 때문에 일반화 성능이 떨어진다.   

    최근 연구는 위 두 단계를 합치려는 경향이 있다.  
    volumetric heatmap regression 방법이 제안되었으나, 이 방식은 컴퓨팅 리소스가 많이 든다는 문제점이 있다.  
    현재 SOTA 방식은 multi-view geometry를 이용하여 신경망을 훈련하는 방법을 보였으나, 이 또한 multi-view 이미지를 처리하는 데에 많은 컴퓨팅 리소스를 요구한다.  

    또 다른 연구(Vnect: Real-time 3d human pose estimation with a single rgb camera)는 각각의 픽셀이 특정 좌표 평가값을 가진 location map을 회귀분석한다.  
    이 방법은 2차원 location map을 이용하기 때문에 컴퓨팅 리소스가 적게 들며, 실시간 처리 및 고사양 PC에서 실행이 가능하다.  
    본고에서 소개하는 방법은 이 연구방법을 기반으로 설계되었다. 
- Knowledge Distillation  
    Knowledge distillation(transfer)란 각기 다른 용량을 가진 신경망 사이에 정보를 전달하는 것을 말한다.  
    핵심 아이디어는 teacher model을 이용하여 class probabilities, feature representations, inter-layer flows에서 추가적인 supervision을 수행하는 것이다.  

## MoVNect 
- CNN 기반 3D 자세 측정 모델 아키텍처
    