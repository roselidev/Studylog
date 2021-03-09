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

