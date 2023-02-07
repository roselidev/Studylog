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
High-to-low process는 저해상 고수준 표현을 목적으로 하는 과정이며,  
Low-to-high process는 고해상도 표현을 목적으로 하는 과정이다.  
두 과정 모두 반복작업으로 성능을 개선할 수 있다.  

대표할만한 신경망 디자인패턴은 다음과 같다.  
1. 대칭형 high-to-low & low-to-high  
    Hourglass 및 그 후속연구에서는 low-to-high를 high-to-low 과정의 mirror로 사용한다.  
2. 무거운 high-to-low & 가벼운 low-to-high  
    ImageNet 분류 신경망에 기반한 high-to-low 과정(e.g. ResNet) 뒤에 
    몇 개의 bilinear-upsampling 또는 transpose convolution layer를 붙여 low-to-high process를 구성한다.  
3. dilated convolution 가미  
    dilated convolution을 ResNet 이나 VGGNet의 마지막 두 단계에 도입하여 공간적인 해상도 유실률을 낮추고, 가벼운 low-to-high 프로세스를 더해 해상도를 더욱 높인다.  
    이 방법은 비싼 컴퓨팅 리소스를 dilated convolutions를 사용함으로써 줄일 수 있는 방법이다.  

### Multi-scale fusion
가장 직관적인 방법은 다양한 해상도의 이미지를 각각 다른 신경망에 넣고 결과물을 모으는 것이다.  
Hourglass 및 그 응용 연구는 high-to-low process 내의 저수준 feature를 동해상도의 low-to-high process 내의 고수준 feature 에 skip connections를 통해 점진적으로 합한다.  
cascaded pyramid network에서는, globalnet이 high-to-low process 내의 저수준 및 고수준 feature를 low-to-high process로 점진적으로 합치고, 그 다음 refinenet이 convolution을 통과한 저수준 및 고수준 feature를 합친다.  
우리의 접근방식은 multi-scale fusion을 반복하며, deep fusion 및 그 응용에 부분적으로 영감을 받았다.  

### Intermediate supervision
Intermediate supervision 또는 deep supervision은 이미지 분류를 위해 생겼으며, 심층신경망 학습 및 히트맵 계산 품질을 높이기 위해 차용되기도 한다.  
Hourglass 접금방식과 convolutional pose machine approach 방식이 중간 히트맵을 나머지 subnetwork 또는 그 일부의 입력으로 넣는 방식이다.  

### Our approach
본고의 신경망은 high-to-low subnetworks를 병렬적으로 연결한다.  
이는 고해상도 표현을 모든 과정동안 유지하며 공간적으로 더 간단한 히트맵을 계산한다.  
또한 반복적인 fusing 작업으로 고해상도 표현의 신뢰도를 더한다.  
우리의 접근 방식은 별도의 low-to-high upsampling process 및 저수준 고수준 표현을 합치는 과정이 존재하는 대부분의 연구와 다르다.  
우리의 접근 방식은 intermediate heatmap supervision을 사용하지 않고, 키포인트 감지 정확도 및 컴퓨팅 성능 복잡도, 파라미터수 면에서 우월함을 보였다.  

## Approach 상세 설명
인체 자세 측정, 또는 키포인트 감지는 K개의 키포인트 또는 신체부위를 W\*H\*3(RGB) 크기의 이미지 I로부터 찾아내는 것을 목표로 한다.  
현재의 SOTA 방법은 이 문제를 W\*H 크기의 히트맵 K개(각 히트맵은 n번째 신체부위의 location confidence를 나타냄)를 만드는 것으로 변환하기도 한다.  

우리는 우선 human keypoints를 찾기 위해 널리 알려진 CNN을 이용하는 과정을 거쳤다.  
이 방법은 해상도를 낮추는 CNN stem 하나와 동해상도의 feature map을 생성하는 main body, 히트맵을 계산하여 full resolution으로 변형하는 regressor 하나로 이루어진다.  
우리는 main body 디자인에 초점을 맞추어 High-Resolution Net(HRNet)을 소개하고자 한다.  

### Sequential multi-resolution subnetworks
현존하는 자세 측정 신경망은 high-to-low resolution subnetworks를 직렬로 연결하여, 각 subnetwork이 한 stage를 구성하며, 인접 subnetwork를 지나면서 해상도를 반으로 줄이며 down-sampling한다.  

### Parallel multi-resolution subnetworks
반면 본고에서는 high-resolution subnetwork 하나가 첫번째 stage를 구성하며, 점진적으로 high-to-low resolution subnetworks가 stage마다 하나씩 증가한다. 결과적으로, 각 stage의 subnetwork 개수는 이전 stage보다 1개 더 많으며, 한 stage의 해상도는 앞선 stage의 해상도에 한 단계 낮은 해상도 하나를 더하여 구성된다.  

### Repeated multi-scale fusion
우리는 병렬 subnetworks에 exchange units를 도입하여 각 subnetwork가 반복적으로 다른 병렬 subnetworks로부터 정보를 받도록 하였다.  

### Heatmap estimation
우리는 마지막 exchange-units의 결과물인 고해상도 표현에서 히트맵을 회귀분석하였다.  
loss function은 mean squared error로 적용하여 히트맵 정답값과 비교하였다.  
정답값 히트맵은 2D 가우시안(표준편차 1px)을 각 정답 keypoint 주변에 적용하여 생성하였다.  

### Network instantiation
신경망 구조는 ResNet 디자인 규칙에 따라 각기 다른 depth를 각 stage에, 각기 다른 채널수를 각 해상도에 적용하였다.  

몸체를 구성하는 HRNet은 4개의 병렬 subnetworks로 이루어진 stage 4개로 구성된다. 해상도는 점차 반으로 줄어들어 width(채널수)는 2배가 된다.  
첫번째 stage는 4개의 residual units를 가지는데, 각 unit은 ResNet-50과 같으며 넓이 64의 bottleneck으로 구성된다.  
나머지 satge는 1,4,3 exchange block을 각각 가진다.  하나의 exchange block은 4개의 residual units를 가지며 각 unit은 해상도별로 두개의 3*3 convolution과 범해상도 exchane unit을 가진다.  
정리하면, 총 8개의 exchange unit이 있으므로, 8번의 multi-scale fusion이 수행된다.  

## 실험결과
### COCO Keypoint Detection
- Dataset : 200,000건 이상의 이미지 250,000건 이상의 인체 예시에 17가지의 keypoint 라벨링.  
    COCO train2017을 이용하여 훈련, val2017 및 test-dev2017을 이용하여 검증함
- 평가지표 : (OKS) Object Keypoint Similarity : 예측된 keypoint와 정답값 사이의 유클리디안 거리를 이용하였으며, 정답값이 이미지 상에서 가시적인지(어딘가에 가리지 않았는지) 표시한 지표, 크기값을 포함한 성과지표 산출식  
    standard 수준의 precision, recall 점수를 보임.  
- 훈련 : human detection box의 비율을 4:3으로 조정하여 크기를 좀 더 키우고, 이미지에서 crop 한 뒤 256\*192 또는 384\*288로 resize함.  
    data augmentation 작업 진행 시 random rotation[-45,45], random scale[0.65,1.35], flipping, half body 포함함.  
    adam optimizer 사용, base_lr = 1e-3
    210 epoch, 170 및 200번째 epoch에 optimizer lr을 각각 1e-4, 1e-5로 하향조정
- 검증 : 2단계 top-down 패러다임 이용.  
    즉, 인체를 감지한 후 키포인트 감지 수행  
    Simple Baseline에서 제공하는 인체 탐지기를 사용하여 validation 및 test를 수행함.  
    다른 대부분 연구에 따라 히트맵은 original 및 flipped images의 히트맵의 평균값으로 계산함. 각 keypoint 위치는 max값에서 그 다음 최대값 방향에 quarter offset을 적용하여 최대값을 계산하였음  

### MPII Human Pose Estimation
- Dataset : 40K가지 종류의 물체를 담은 25K 이미지에 COCO와 동일한 방식의 data augmentation 수행.  
- Testing : COCO와 같으나, detected person box가 아닌 제공된 person box를 사용함.  
- 평가지표 : PCKh(head-normalized probability of correct keypoint) at alpha=0.5

### Application to Pose Tracking
- Dataset : PoseTrack은 비디오 인체 자세 측정 및 articulated tracking 분야의 대규모 벤치마크이다. MPII Human Pose dataset에서 제공하는 raw video를 기반으로 총 66,374 프레임의 550 비디오 영상물로 이루어져 있다.  
- 평가지표 : mean Average Precision(mAP), multi-object tracking accuracy(MOTA)  
- 훈련 : PoseTrack2017 훈련셋

## Ablation Study
- Repeated multi-scale fusion : 단계간/단계별 exchange unit (8 fusions)
- Resolution maintenance : HRNet 구조에 따른 해상도 보존여부 : 저해상도 HRNet-W32가 최고성능 달성. 저해상도 subnetworks의 초기 단계에서 추출된 저수준 features는 도움이 덜 되는 것으로 보인다.  

## Conclusion
본고에서, 우리는 인체 자세 측정을 위한 고해상도 신경망을 보였으며, 보다 더 정확하고 공간적으로 간단한 keypoint heatmap을 산출함을 보였다.  
이 성과는 두가지 원인으로부터 비롯되었다.  
1. 고해상도를 복구하는 것이 아닌 모든 과정동안 고해상도를 유지하는 방법을 채택함
2. 다중 해상도 표현을 fusing하는 작업을 반복적으로 진행하여 신뢰도 높은 고해상도 표현을 생성함.  

앞으로의 연구는 인체 측정 이외에 다른 dense prediction task, 예를 들면 semantic segmentation, object detection, face alignment 등에 사용될 수 있을 것이다.  
