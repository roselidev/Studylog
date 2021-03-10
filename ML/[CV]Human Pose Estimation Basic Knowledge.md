# Introduction to Human Pose Estimation

## 용어 및 개념 Terminology

### 카메라 파라미터 Camera parameters

#### [카메라 캘리브레이션이란?](https://darkpgmr.tistory.com/32) Camera calibration

- **카메라의 위치와 방향이 아닌 카메라 자체 사양 등 내부 요인을 규명하는 과정.**
- **3D 공간좌표와 2D 영상좌표 사이의 변환관계 또는 이를 설명하는 파라미터를 찾는 과정.**
    
우리가 실제로 보는 3차원 세상을 카메라로 찍으면 2차원이 된다.  
이 때 3차원의 점들이 이미지 상의 어디에 위치하는지를 기하학적으로 따져보면,  
이는 사진을 찍을 당시의 카메라 위치 및 방향에 의해 결정된다.  

하지만 실제 이미지는 렌즈 종류, 센서와의 거리, 각도 등  
카메라 자체 사양에 의해 영향을 받기도 한다.  
따라서 이미지 좌표로부터 3차원 공간좌표를 얻으려면  
이러한 내부요인을 제거하여야 정확한 계산이 가능해지며,  
이 내부 파라미터 값을 구하는 과정을 카메라 캘리브레이션이라고 한다.  

#### 캘리브레이션 개요
    
![카메라좌표 - world 좌표 변환식](https://t1.daumcdn.net/cfile/tistory/24758441510E994028)

    (X,Y,Z) :  월드좌표계(world coordinate system) 상의 3D 좌표
    [R|t] :  좌표 변환을 위한 회전/이동변환 행렬
    A : intrinsic camera matrix
    
    여기서 [R|t]를 카메라 외부 파라미터, A를 내부 파라미터라고 부른다.
    그리고 A와 [R|t]를 합쳐서 camera matrix 또는 projection matrix 라고 부른다.

#### 카메라 내부 파라미터

A. 초점거리 (focal length) : fx, fy  
B. 주점 (principal point) : cx, cy  
C. 비대칭계수 (skew coefficient) : skew_c : tanα  

*A. 초점거리 focal length*
- 렌즈 중심(pinhole)과 이미지 센서(CCD/CMOS) 간의 거리  
- pixel 단위로 표현한다.  
    한 pixel은 이미지센서의 cell 하나에 대응한다.   
    따라서 이미지센서의 cell 크기가 0.1mm이고 초점거리가 `f = 500 pixel`이면 물리적 초점거리는 50mm이다.  

*B. 주점 principal point*
- 렌즈 중심(pinhole)에서 이미지 센서에 내린 수선의 발의 영상좌표
- image center와는 다른 개념이다. 예를들어 카메라 조립 과정에서 오차로 인해 렌즈와 이미지 센서의 수평이 어긋나면 principal point != image center이다.

*C. 비대칭계수 skew coefficient*
- 이미지 센서의 cell array의 y축이 기울어진 정도 
- skew_c = tanα
![skew_coefficient](https://t1.daumcdn.net/cfile/tistory/192F8344510E9B3A33)
- 요즘은 거의 skew 에러가 없기 때문에 보통 고려하지 않음 (skew_c = 0)

#### 카메라 외부 파라미터 extrinsic parameters

- 카메라의 위치, 방향, 월드좌표계의 정의에 따라 달라지는 파라미터
- 외부 파라미터를 구하기 위해서 먼저 캘리브레이션 툴을 이용해 내부 파라미터를 구한 뒤, 3D - 2D 좌표쌍을 이용하여 변환행렬을 구한다. [OpenCV - solvePnP 함수 이용]

#### 핀홀 카메라 모델

![pinhole_camera_model](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Pinhole-camera.svg/220px-Pinhole-camera.svg.png)
- 하나의 바늘구멍을 통해 외부의 상이 이미지로 투영된다는 모델링 중 하나.  
- 영상처리 분야에서 영상에 대한 모든 기하학적 해석은 이 핀홀 카메라 모델을 바탕으로 이루어진다.
- 실제로는 렌즈 특성에 따른 영상 왜곡도 고려되어야 한다.

#### 렌즈 왜곡 종류

- 방사왜곡 : 왜곡의 정도가 카메라 중심에서의 거리에서 멀 수록 심해진다  
- 접선왜곡 : 왜곡의 정도가 카메라 중심에서 거리에서 멀 수록 심해지나, 분포가 타원형  형태이다. 이는 부품간 수평이 맞지 않거나 렌즈 자체 하자로 인해 발생한다.  

#### 렌즈계 왜곡의 수학적 모델

- 카메라 내부 파라미터의 영향을 제거한 normalized image plane에서 정의  
- radical distortion, tangential distortion을 적용하여 normalized image plane 위의 좌표를 구한 뒤 실제 영상 픽셀 좌표는 카메라 내부 파라미터를 반영하여 도출

#### 영상 왜곡 보정

- 카메라 캘리브레이션을 통해 카메라 내부 파라미터를 구한 후, 보정 후 좌표에 이를 역으로 적용하여 normalized 좌표로 변환
- 그런 다음 렌즈중심까지의 거리를 구하고 왜곡모델을 적용하여 왜곡좌표를 구함
- 마지막으로 왜곡좌표를 다시 픽셀좌표계로 변환하면(즉 카메라 내부 파라미터를 곱하면) 왜곡 영상에서의 좌표가 됨

### 영상 기하 image geometry

#### 좌표계 coordinate system

- 월드좌표계, 카메라좌표계, 정규좌표계, 픽셀좌표계  
- 월드좌표계 : 사물의 위치를 표현할 때 기준으로 삼는 좌표계
- 카메라좌표계 : 카메라를 기준으로 한 좌표계. 단위는 월드좌표계와 통일할 것
![camery_coordinate_system](https://t1.daumcdn.net/cfile/tistory/2413B54751EF9E6618)
- 픽셀좌표계(영상좌표계) : 이미지 왼쪽 상단을 원점으로 두고 x축과 y축을 잡은 이미지 평면(image plane)이라고 부른다.  
기하학적으로 볼 떄 3D 공간 상의 한 점  P(X,Y,Z)는 이미지 평면의 한 점 p(x,y)에 투영(projection)된다. 
- 정규좌표계(Normalized Image Coordinate System) : 편의상 도입하는 가상의 좌표계.  
카메라 내부 파라미터의 영향을 제거한 가상의 이미지 좌표계.  
좌표계 단위를 없앤(정규화된) 좌표계이며 카메라 초점과의 거리가 1인 가상의 이미지 평면을 말함.  
정규좌표계의 원점은 정규 이미지 평면의 중점이며, 픽셀좌표계의 원점과 다름.

#### Epipolar Geometry

- 두 가지 서로 다른 시점에서 같은 대상을 찍는 상황에서, 3차원 공간 상의 한 점 P가 영상 A에서는 p에 투영되고 영상 B에서는 p'에 투영된다. 이 때, 두 카메라 원점을 잇는 선과 이미지 평면이 만나는 점 e, e'를 epipole 이라 부르고 pinhole과 epipole을 잇는 직선 l, l'를 epiline 또는 epipolar line이라 부른다.
- 이 때 두 영상좌표 p와 p' 사이에는 다믕 관계를 만족하는 Essential Matrix가 항상 존재한다.  
![epipolar_geometry1](https://t1.daumcdn.net/cfile/tistory/233F803E51EF18460F)  
![epipolar_geometry](https://t1.daumcdn.net/cfile/tistory/277AC34451EF18731B)

### Triangulation

#### 들로네 삼각분할 Delaunay triangulagtion
- 평면 위의 점들을 삼각형으로 연결하여 공간을 분할 할 때, 이 삼각형들이 최대한 정삼각형이 되도록 하는 분할 = 이 삼각형들의 내각의 최소값이 최대가 되도록 하는 분할  
![triangulation](https://t1.daumcdn.net/cfile/tistory/2528183552299CE91E)
- (c)가 아닌 (b)처럼 되도록 분할하는 것
- 어떤 삼각형의 외접원도 그 삼각형의 세 꼭지점을 제외한 다른 점을 포함하지 않는다는 중요한 특징을 가진다.  
- 들로네 삼각분할을 이용하면 클러스터링을 효과적으로 할 수 있는데, 먼저 데이터 점들을 들로네 삼각분할로 연결한 이후 일정한 길이 이상의 긴 변을 제거하고 남은 연결된 성분을 구하면 된다.