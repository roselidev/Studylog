# Multi-modal Dense Video Captioning

[IEEE/CVPR 2020]
[codebase](https://github.com/v-iashin/MDVC)

## Abstract
Dence video captioning은 무편집 비디오에서 흥미로운 event를 특정하고 text description (caption) 을 생성하는 작업이다.  
대부분의 이전 연구들은 주로 visual information에만 집중하고 audio track은 완전히 무시하였다.  
그러나, audio, 특히 speech는 사람이 환경을 이해하는 중요한 힌트를 제공한다.  
본고에서 우리는 새로운 video captioning 접근방식을 보여 event description을 생성하는 데에 modality의 수에 제한이 없음을 보일 것이다.  
구체적으로, 우리는 audio와 speech modality가 dense video captioning 모델을 개선할 수 있음을 보일 것이다.  
우리는 automatic speech recognition(ASR) 시스템을 적용하여 시간 정보로 배열된 speech의 텍스트 정보(subtitle)를 얻어, 이를 비디오 프레임, 상응하는 오디오 트랙과 함께 독립적인 하나의 입력으로 취하였다.  
우리는 captioning task를 machine translation task로 상정하였으며, 최근 제안된 Transformer 아키텍처를 이용하여 multi-modal input을 text 설명으로 변환하였다.  
우리는 ActivityNet Captions Dataset에 대하여 성능 실험을 하였다.  

## Introduction
무료 영상 자료가 늘어남에 따라 핵심 내용을 요약하고 압축적으로 표현하려는 수요가 함께 증가하고 있다.  
한 가지 접근 방법은 video summarization task로 중요한 비디오 부분을 편집하는 것이다.  
또는, 비디오 컨텐츠를 자연어 문장을 이용하여 표현할 수 있다.  
이 접근방식은 매우 압축적이고 직관적인 비디오 표현 형식이며 video captioning이라고 불린다.  
그러나, 길고 제한 사항이 불분명한 비디오 전체를 한 문장으로 압축하는 것은 현실성이 없다.  
따라서, dense video captioning 분야는 먼저, events를 특정하고, 각각의 event에 대해 text description을 생성하는 것을 목표로 한다.  

대부분의 기존 연구들은 captioning 문제를 machine translation task로 상정하며, 이는 video feature를 입력으로 하고 자연어를 출력으로 하는 모델이다. 따라서, captioning 기법은 Transformer와 같은 machine translation 분야의 기존 모델을 레버리징할 수 있다.  

기존 연구의 대부분은 caption을 전적으로 시각 정보에 기반하여 생성하였다.  
그러나, 거의 대부분의 비디오는 오디오 정보를 담고 있으며, 이는 video understanding의 중요한 단서가 된다.  
특히, 비디오 속의 사람이 무슨 말을 하고 있는지는 내용 설명에 큰 영향을 끼친다.  
예를 들어, 누군가가 문 뒤에서 노크를 한다면, 우리의 시각정보에는 닫힌 문 밖에 없지만 청각정보가 누군가 문 뒤에 있다는 정보를 제공한다.  
따라서, 기존 방식의 모델들은 유용한 caption을 생성할 수 없다.  

반면, 우리의 모델은 video frame, raw audio signal, speech content를 모두 사용하여 caption 생성을 수행한다.  
이를 위해, 우리는 ASR 시스템을 도입하여 시간별 발화정보 (자막과 비슷함)를 추출하였으며, 이를 비디오, 오디오트랙과 함께 transformer 모델에 사용하였다.  

제안한 모델은 ActivityNetCaption Dataset으로 검증하였으며, 현재 SOTA 성능을 달성하였다.  


## 관련 연구
### Video Captioning
video captioning 의 모든 연구들은 규칙기반 모델을 적하여, 일련의 비디오를 이용하여 미리 정의된 template을 채워 sentence를 생성한다.  
이후에는 captioning problem을 machine translation task로 상정하므로 sentence template은 없어도 된다.  
번역 시스템에서 신경망 모델이 성과를 내면서, video captioning에도 그러한 방법들이 유명해졌다.  
이러한 접근방식의 기본 논리는 encoder-decoder 양식으로 2개의 RNN.을 훈련하는 것이다.  
구체적으로, encoder는 video feature을 입력으로 받아 hidden state에 적층하고, 이는 decoder로 전해져 caption 생성에 사용된다.  
captioning model의 성능을 더욱 높이기 위하여 몇가지 방법이 제안되었다.  
<>와 <>는 visual 및 textual domain 사이에 shared memory 를 포함하는 방식을 제안하였다.  
또한, <>와 <>는 문장 대신 문단을 제공하는 방식을 제안하였다.  

### Dense Video Captioning
dense image captioning 분야에 영감을 받아, ActivityNet Captions라는 데이터셋이 공개되었다.  
<Bidirectional attentive fusion with context gating for dense video captioning. 2018.>