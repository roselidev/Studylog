# End-to-End Dense Video Captioning with Masked Transformer
[codebase](https://github.com/salesforce/densecap)

## Abstract
**Dense Video Captioning**이란 무편집 비디오 내의 모든 이벤트에 대한 text 설명을 생성하는 것이 목표이다.   
**Dense Video Captioning** 내에는 감지(detection) 및 설명(description) 업무 두 가지가 포함되기 때문에, 이전까지의 대부분의 연구들은 각각의 업무를 해결하는 두 가지의 모델을 구축하였다. (event proposal model, captioning model)  
이 두 모델은 독립적으로 훈련하거나 번갈아 훈련하였으며 따라서 text 설명이 event proposal에 기여할 수 없었는데, 이는 정확한 설명 생성을 위해 아주 중요한 정보이다.  
이러한 문제를 해결하기 위해, 우리는 end-to-end transformer model을 제시한다.  

Encoder는 video representation을 encode하며, proposal decoder 은 각기 다른 anchor를 가진 encoding을 통해 video event proposal을 생성한다. captioning decoder는 masking network를 이용하여 attention과 proposal event를 encoding feature로 제한한다. 이 masking network는 event proposal을 미분가능한 mask로 바꾸어 주어, 훈련 동안 proposal 과 captionning의 일관성을 보장한다. 또한 이 모델은 self-attention 기술을 차용하여 효율적인 non-recurrent 구조와 함께 성능 개선을 보였다.  

우리는 ActivityNet Captions 및 YouCookII 데이터셋에서 각각 METEOR 점수 10.12 와 6.58을 달성하였다.  

## Introduction
사람들은 정보 습득을 위해 비디오를 점점 더 많이 이용하고 있다.  
비디오 컨텐츠는 높은 수준의 인지 능력을 필요로 하므로 인간이 이해하는 데에 상대적으로 많은 시간이 필요하다.  
비록 시각 정보 그 자체로 속에 담긴 의미를 명확히 알 수 있을 때도 있지만, 비디오 컨텐츠를 더 쉽고 빠르게 이해하는 한 가지 방법은 핵심 의미만 담고 있도록 압축시키는 것이다.  
이는 매일 쏟아져 나오는 비디오 컨텐츠의 양을 보았을 때 매우 중요한 문제이다.  
Video Summarization은 이러한 압축 작업의 한 종류이지만, 언어 요소를 고려하지 않기 때문에 교육형 비디오에는 적합하지 않다.  
Dense Video Captioning은 자연어 설명문 형식으로 비디오 내의 사건을 설명하며, 언어 요소를 보존하면서 비디오 정보를 압축할 수 있다.  

Dense Video Captioning은 두가지 부분으로 나뉜다.  
바로 Event Detection과 Event Description이다.  
현존하는 방법은 이 두가지의 하위 문제를 각각의 모듈(Event Proposal, Captioning)을 이용하여 해결하려는 방법들이다.  
주로 각각의 모듈을 독립적으로 훈련하고 best event proposal에 대한 description을 생성하는 방식이거나, 번갈아 훈련하는 방식(proposal 모듈 훈련 <-> 발생한 event proposal에 대해 captioning 모듈 훈련 및 proposal module fine-tuning)이다.  
그러나 두 방법 모두 언어 정보가 event proposal에 직접적인 영향을 주지 못한다는 단점이 있다.  

직관적으로 비디오의 사건 구성과 언어는 밀접한 연관이 있으며 언어 정보는 비디오 내의 사건을 특정하는 데에 도움을 줄 수 있다.  
이러한 이유로, 우리는 encoder-decoder 기반의 end-to-end 모델을 제안한다.  

encoder는 video frames(features)를 적합한 표현 형식으로 encode한다.  
그런 다음, proposal decoder가 event proposal을 미분가능한 mask로 바꾸어주는 masking network를 통해 proposal specific representation를 생성하고, 이 미분가능한 mask는 proposal decoder, captioning decoder 모두 안정적으로 훈련할 수 있도록 해준다. 즉, proposal module은 생성된 caption의 질에 따라 예측값을 조절할 수 있게 된다. 다르게 말하면, 생성된 caption의 언어정보가 visual model이 더욱 적합한 proposal을 생성할 수 있도록 유도할 수 있다.  

그 동안의 proposal module이 비디오의 내용과 상관 없이 class-agnostic binary classification 문제를 풀도록 훈련된 것과는 달리, 우리의 모델은 propose 되는 비디오 세그먼트의 내용과 caption 속 의미 정보사이의 일관성을 확보하였다.  

Dense Video Captioning의 또 다른 과제는, 이는 넓게는 sequence modeling 분야 전체의 문제이기도 하지만 장거리 정보 의존성 문제를 해결해야한다는 것이다.  
RNN을 사용할 수도 있지만 Self-attention이 더 효율적으로 학습할 수 있으므로 빠른 self-attention 모듈을 장착한 transformer 구조를 채택하였다.  

우리의 기여는 크게 두 가지로 설명할 수 있다.  
첫째로, Dense Video Captioning 분야에 end-to-end 모델을 제안하였다.  
둘째로, self-attention을 사용하였다.  

## 관련 연구
### Image and Video Captioning
이전의 연구들은 Hidden Markov Model과 Ontology를 이용하였으나, 
- Grounded language learning from video described with sentences. 2013.
- A thousand frames in just a few words: Lingual description of videos through latent topics and sparse object stitching. 2013.

최근의 연구들은 대부분 DNN 기반의 방법을 사용한다.
- Show and tell: A neural image caption generator. 2015.
- Show, attend and tell: Neural image caption generation with visual attention. 2015.
- Image captioning with semantic attention. 2016.
- Watch what you just said: Image captioning with text-conditional attention. 2017.
- Boosting image captioning with attributes. 2017.
- Self-critical sequence training for image captioning. 2016.

일반적으로 CNN을 이용하여 video frame을 인코딩하고, 디코더로 LSTM과 같은 recurrent language decoder를 이용하며,
- Very deep convolutional networks for large-scale image recognition. 2014.
- Deep residual learning for image recognition. 2016.

이들 연구의 차이점은 주로 mean-pooling,  
- Translating videos to natural language using deep recurrent neural networks. 2014.
- Semantic compositional networks for visual captioning. 2017.

recurrent 신경망 구조,
- Long-term recurrent convolutional networks for visual
recognition and description. 2015. 
- Sequence to sequence-video to text. 2015.

그리고 attention mechanism 사용여부이다. 
- Describing videos by exploiting temporal structure. 2015.
- Video captioning with transferred semantic attributes. 2017.
- Semantic compositional networks for visual captioning. 2017.

### Temporal Action Proposals (TAP)
TAP는 무편집 영상에서 사건과 관계 없이 proposal의 시간을 특정하는 것을 목표로 한다.  
현존하는 방법들은 TAP를 binary classification 문제로 치환하며, proposal이 어떻게 propose 되는지 또는 어떤 proposal을 탈락시킬 것인지에 따라 연구내용이 달라진다.  

<Temporal action localization in untrimmed videos via multi-stage cnns. (2016)>은 비디오 프레임에 대하여 sliding window 방식을 제안하였는데, 이는 컴퓨팅 리소스가 많이 든다.  
최근에는 object detection의 anchoring 기법에 영감을 받아 두가지 방법이 제안되었다. 
<Turn tap: Temporal unit regression network for temporal action proposals (2017)>와 <Towards automatic learning of procedures from web instructional videos (2018)>는 explicit anchoring을 제안하였으며,  
<Daps: Deep action proposals for action understanding (2016)>와 <Sst: Single-stream temporal action proposals. (2017)>는 implicit anchoring을 제안하였다.  
explicit anchoring의 경우, 각각의 anchor는 해당 구간 내의 video feature이며, action 또는 background 두 가지 중 하나로 분류된다.  
implicit anchor의 경우, RNN이 video sequence를 encode하고 각각의 anchor center에 다양한 크기의 다중 anchor가 제안된다.  
지금까지는 explicit anchoring 방법이 location regression과 함께 사용되었을 때 가장 좋은 성능을 보였다.  
우리 논문의 방법은 <Towards automatic learning of procedures from web instructional videos (2018)>를 기반으로 하며, 이 모델은 행동 보다는 길고 복잡한 사건을 감지하기 위해 고안되었다.  
우리는 이 framework를 temporal convolutional proposal network와 self-attention based context encoding으로 개선하였다.

### Dense Video Captioning
video paragraph captioning이라는 비디오 세부 구간별 captioning 방법론이 <Video paragraph captioning using hierarchical recurrent neural networks (2016)> 논문을 통하여 소개되었으나, 구간이 사람에 의해 미리 정해져 있다는 단점이 있다.  

<A thousand frames in just a few words: Lingual description of videos through latent topics and sparse object stitching (2013)> 논문에서 sparse object stitching을 이용하여 전체 video에 대한 dense caption을 생성하는 방법을 제안하였으나, 이 방법은 top-down ontology에 의존적이며 최근 captioning 방법과 달리 data-driven 방식이 아니다.  

이 연구와 가장 비슷한 선행연구는 <Dense-captioning events in videos. (2017)> 이며, event location과 caption을 생성하는 모델이다. 그러나, 그들은 proposal과 captioning module을 통합하여 합께 훈련하기 때문에 caption이 event proposal의 정보를 이용하지 못한다는 단점이 있다. 