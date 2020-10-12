## [CV]Unsupervised Learning of Depth and Ego-Motion from Video

[원문](https://people.eecs.berkeley.edu/~tinghuiz/projects/SfMLearner/cvpr17_sfm_final.pdf) 

용어 정리

- monocular depth : The **Monocular Depth** Estimation is the task of estimating scene **depth** using a single image.
- motion estimation : **Motion estimation** is the process of determining **motion** vectors that describe the transformation from one 2D image to another
- End-to-end learning : **End**-to-**end learning** refers to **training** a possibly complex **learning** system by applying gradient-based **learning** to the system as a whole. 
- view synthesis : **view synthesis** is the task of generating new images that render the object from a different viewpoint than the one given.
- ego-motion : 환경 내에서 카메라의 3차원 이동. 에고모션 추정이란 환경내에서 카메라의 이동을 카메라에 의해 캡쳐된 일련의 이미지들에 기초하여 추정하는 것

### Basics of Depth Estimation

- To compute distances of objects in image, we need at least 2 cameras having different viewpoints. 
- Disparity : difference of location seen in image. Depth is proportional to 1 / Disparity.

### Brief Review of the Paper

- Deep learning network that performs depth estimation in unsupervised way
- Depth Network and Pose Network
- Depth Network is to predict the depth of a single image
- Pose Network is to predict the camera motion between the consecutive video frames.

