# Deep High-Resolution Representation Learning for Human Pose Estimation 
[official codebase](https://github.com/leoxiaobin/deep-high-resolution-net.pytorch)

## Abstract
이 논문에서 우리는 신뢰도 높은 고해상도 표현에 초점을 둔 인체 자세 측정 문제에 관심이 있다.  
현존하는 대부분의 방법은 고해상도 표현을 high-to-low resolution network에서 생성된 저해상도 표현으로부터 복구하는 방식을 사용한다.  
반면에, 우리가 제안하는 신경망은 모든 과정동안 고해상도 표현을 유지한다.   

첫 단계에서 고해상도 subnetwork로 시작하고, 점진적으로 high-to-low resolution subnetworks를 단계가 진행됨에 따라 하나씩 더하면서 muliti-resolution subnetworks를 병렬적으로 연결한다.  
이 과정을 여러 스케일에서 여러 조합으로 반복적으로 실행하였다. 예를 들어, high-to-low resolution representation이 다른 병렬 representation으로부터 입력받는 구조를 계속해서 중첩하면 풍부한 고해상도 표현을 얻을 수 있다.  

결과적으로, 본고의 모델이 추론한 키포인트 히트맵은 잠재적으로 더 정확하고 공간적으로는 더 간단하다.  
우리는 실제로 COCO keypoint detection dataset 과 MPII Human Pose Dataset 두 벤치마크 데이터셋에서 우월한 자세 측정 결과를 통해 우리 모델의 효율성을 시연하였다.  
또한, PoseTrack dataset에서 우리의 모델이 pose tracking에서도 우월함을 보였다.  

## Introduction
2D 인체 자세 측정은 CV 분야에서 매우 근본적이지만 도전적인 문제이다.  
2D 인체 자세 측정의 목표는 사람의 해부학적 키포인트(팔꿈치, 손목 등) 또는 신체부위를 localize하는 것이다.  
인체 행동 인식, HCI(human-computer interaction), 애니메이션 등 응용 분야는 매우 다양하다.  

본고에서는 단일 인체 자세 측정에 대해 다룰 것이다.  
단일 인체 자세 측정은 다수 인체 자세 측정, 영상 자세 측정, 그리고 자세 tracking 등의 여타 관련 문제의 근간이 되는 분야이다.  

최근 연구들은 SOTA 성능을 달성하는 심층 convolution 신경망을 공개해왔다.  
대부분의 기존 연구는 high-to-low 해상도 subnetwork로 이루어진 전형적인 신경망에 입력을 넣고, 해당 신경망을 일렬로 연결하여 결과물을 얻은 다음, 해상도를 높이는 작업을 진행한다.  
예를들어, Hourglass는 대칭되는 low-to-high 프로세스를 이용한다.  
SimpleBaseline은 전치된 convolution 층을 이용하여 고해상도 결과물을 생성한다.  

본고에서 소개하는 새로운 아키텍처의 이름은 HRNet (High-Resolution Net)으로, 모든 과정동안 고해상도 표현을 유지할 수 있다.  
첫 단계에서 고해상도 subnetwork로 시작하고, 점진적으로 high-to-low resolution subnetworks를 단계가 진행됨에 따라 하나씩 더하면서 muliti-resolution subnetworks를 병렬적으로 연결한다.  
이 과정을 여러 스케일에서 여러 조합으로 반복적으로 실행하였다.  

우리의  신경망은 다른 대중적인 자세측정 신경망에 비해 두가지 장점을 가지고 있다.  
1. high-to-low resolution subnets를 직렬이 아닌 병렬로 연결하여 해상도를 복구할 필요 없이 고해상도를 유지할 수 있으며, 따라서 히트맵도 공간적으로 저 간단해진다.  
2. 대부분의 현존하는 융합 전략(fusion scheme)은 low-level representation과 high-level representation을 집약하지만, 우리는 반복적  다중 스케일 융합으로 고해상도 표현을 같은 깊이와 비슷한 level의 저해상도 표현으로 강화하여, 고해상도 표현 또한 다양한 자세를 측정할 수 있도록 하였다. 이 결과 우리의 히트맵은 잠재적으로 더 높은 정확성을 가진다.  

## Related Work
단일 인체 자세 측정에 관한 대부분의 전통적인 방법은 확률 그래프 모델 또는 pictorial structure model을 차용하였으며, 최근 딥러닝을 이용하여 단수 또는 한쌍의 에너지를 모델링하거나 반복 추론 프로세스를 모방하여 성능을 개선하고 있다.  
근래에는 반복 추론 프로세스 모방보다 딥러닝을 이용한 솔루션이 대부분이며, 그 방법은 크게 두 부류로 나뉘어 진다.  

1. keypoint position regression
2. keypoint heatmap estimation --> heat가 가장 높은 위치를 keypoint로 선정

히트맵을 계산하는 대부분의 CNN은 분류 네트워크와 비슷한 subnetworks로 이루어져 있다.  
이 subnetwork는 해상도를 떨어뜨리며, 입력과 같은 해상도를 출력하는 주요 몸체 부분과 히트맵을 추론하여 keypoint가 계산되고 full-resolution으로 변환되는 후속 부분으로 이루어져 있다.  
주요 부분은 주로 high-to-low와 low-to-high framework를 차용하며, multi-scale fusion과 intermediate (deep) supervision으로 확장되기도 한다.  

### High-to-low and low-to-high

