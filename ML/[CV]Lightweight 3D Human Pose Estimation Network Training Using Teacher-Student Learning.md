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
 