# tweet
트위터 고객 대응 모델

## 역할분담

|구성원|역할|
|---|---|
|김한슬|조장 & 머신러닝 활용 데이터분석|
|김태우|데이터 처리 & 활용| 
|유현택|백엔드 & 대응 api|
|정강민 멘토님|전체 프로젝트 멘토링|
|조혜창 멘토님|전체 프로젝트 멘토링|

# Tweet - Music Recommendation Based on Tweet Sentiment Analysis
<img width="655" alt="image" src="https://github.com/sw-twitter/tweet/assets/117340073/e3f53651-2f71-4480-acf0-1fdef72be4ee">


## 프로젝트 개요
Tweet는 사용자의 트윗을 분석하여 감정을 파악하고, 이를 바탕으로 개인화된 노래를 추천하는 인공지능 프로젝트입니다. 이 프로젝트는 React, Material UI, Python 및 OpenAI의 ChatGPT를 사용하여 구현되었습니다.

## 아키텍처 개요
이 프로젝트는 크게 두 부분, 즉 Front-end와 Back-end, 인공지능 모델로 나뉩니다.

### Front-end
- **기술 스택**: React를 사용하여 구축하였으며, 사용자 인터페이스는 Material UI로 디자인되었습니다.
- **주요 기능**:
  - 사용자는 웹 인터페이스를 통해 자신의 Twitter 핸들을 입력할 수 있습니다.
  - 감정 분석 결과와 음악 추천 목록이 사용자에게 표시됩니다.

### Back-end
- **기술 스택**: Python을 주 언어로 사용하여 서버와 로직을 구현하였습니다.
- **데이터 수집**: kaggle 데이터를 사용하여 사용자의 최근 트윗을 수집합니다.
- **감정 분석**: 수집된 트윗에서 감정을 분석합니다. 이 때, 다양한 감정 상태를 인식할 수 있도록 모델이 튜닝되어 있습니다.
- **음악 추천 로직**: 감정 분석 결과에 따라 다양한 장르와 스타일의 음악을 추천하기 위해 Openai API를 사용합니다.

## 전체 흐름
1. **사용자 인터페이스**: 사용자가 웹 페이지에 접속하여 Twitter 핸들을 입력합니다.
2. **데이터 수집 및 전송**: Front-end는 이 정보를 Back-end로 전송합니다.
3. **Back-end 처리**: 트윗을 수집하고, 감정 분석을 수행한 뒤, 적절한 음악을 추천합니다.
4. **결과 전달**: 추천된 음악 목록이 Front-end를 통해 사용자에게 표시됩니다.

## 감정분석 코딩 데이터 참고자료
from google.colab import drive
drive.mount('/content/drive')
!pip install --upgrade openai
!pip install tqdm requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import openai
import requests
from tqdm import tqdm
import time
openai.api_key = "INPUT YOUR API KEY"
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
df =  pd.read_table('/content/drive/MyDrive/Colab_Notebooks/bab2min_corpus_master_sentiment_naver_shopping.txt', names=['Rating', 'Review Text'])
df = df.iloc[0:200]
df['Rating'].value_counts(normalize=True).sort_index()
def analyze_review(review):

  try:
    messages = [
            {"role": "system", "content": "너는 제품 리뷰에 담긴 고객 감정을 분석하고 탐지하는 AI 언어모델이야"},
            {"role": "user", "content": f"다음 제품 리뷰를 분석해 고객 감정이 긍정인지 부정인지 판단해 알려줘. 대답은 다른 추가적인 설명없이 '긍정' 또는 '부정'  둘 중 하나의 단어로 대답해야 해: {review}"}
        ]

    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=3,
            n=1,
            stop=None,
            temperature=0
        )

    response= completion.choices[0].message.content
    print(response)
    return response

  except openai.error.RateLimitError as e:
    retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
    print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
    time.sleep(retry_time)
    return analyze_review(review)

  except openai.error.ServiceUnavailableError as e:
    retry_time = 10  # Adjust the retry time as needed
    print(f"Service is unavailable. Retrying in {retry_time} seconds...")
    time.sleep(retry_time)
    return analyze_review(review)

  except openai.error.APIError as e:
    retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
    print(f"API error occurred. Retrying in {retry_time} seconds...")
    time.sleep(retry_time)
    return analyze_review(review)

sentiments = []

for review in tqdm(df["Review Text"]):
    sentiment = analyze_review(review)
    sentiments.append(sentiment)

df["Sentiment"] = sentiments

df.to_excel('/content/drive/MyDrive/Colab_Notebooks/reviews_analyzed_sentiment.xlsx', index=False)
