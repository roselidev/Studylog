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

InterHand와 Human3.6M 데이터셋에 대하여 실험한 결과 baseline에 대한 지속적인 개선을 보였다.  
외부 데이터를 전혀 이용하지 않은 상황에서, ResNet-50 backbone, image size 256*256, Human3.6M으로 훈련된 모델이 SOTA 성능을 4.23mm 차이로 능가하여 MPJPE 26.9mm 를 달성하였다.  