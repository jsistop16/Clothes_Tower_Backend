import pytz
import requests 
from datetime import  datetime, timedelta
import os


def answerWeather():
      tz = pytz.timezone('Asia/Seoul')
      
      
      now = datetime.now(tz)
      print(now.hour);
      print("지금 시간은 " + now.strftime("%H%M"));
      # 오늘
      # today = datetime.today(tz) # 현재 지역 날짜 반환
      today_date = now.strftime("%Y%m%d") # 오늘의 날짜 (연도/월/일 반환)
      print('오늘의 날짜는', today_date)

      # 어제
      yesterday = now - timedelta(days=1)
      yesterday_date=yesterday.strftime('%Y%m%d')
      print('어제의 날짜는', yesterday_date)

      # 1일 총 8번 데이터가 업데이트 된다.(0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
      # 현재 api를 가져오려는 시점의 이전 시각에 업데이트된 데이터를 base_time, base_date로 설정
      if now.hour<2 or (now.hour==2 and now.minute<=10): # 0시~2시 10분 사이
        base_date=yesterday_date # 구하고자 하는 날짜가 어제의 날짜
        base_time="2300"
      elif now.hour<5 or (now.hour==5 and now.minute<=10): # 2시 11분~5시 10분 사이
        base_date=today_date
        base_time="0200"
      elif now.hour<8 or (now.hour==8 and now.minute<=10): # 5시 11분~8시 10분 사이
        base_date=today_date
        base_time="0500"
      elif now.hour<=11 or (now.minute<=11 and now.minute<=10): # 8시 11분~11시 10분 사이
        base_date=today_date
        base_time="0800"
      elif now.hour<14 or (now.hour==14 and now.minute<=10): # 11시 11분~14시 10분 사이
        base_date=today_date
        base_time="1100"
      elif now.hour<17 or (now.hour==17 and now.minute<=10): # 14시 11분~17시 10분 사이
        base_date=today_date
        base_time="1400"
      elif now.hour<20 or (now.hour==20 and now.minute<=10): # 17시 11분~20시 10분 사이
        base_date=today_date
        base_time="1700" 
      elif now.hour<23 or (now.hour==23 and now.minute<=10): # 20시 11분~23시 10분 사이
        base_date=today_date
        base_time="2000"
      else: # 23시 11분~23시 59분
        base_date=today_date
        base_time="2300"
      
      print("현재 시각 : " +base_time);
      # 실제로 공공데이터 api에서 데이터를 가지고 오는 로직 
      url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
      params ={'serviceKey' : os.environ.get("WEATHER_KEY"),
               'pageNo' : '1', 'numOfRows' : '1',
               'dataType' : 'JSON', 'base_date' : base_date,
               'base_time' :  base_time, 'nx' : '60', 'ny' : '127' }
      response = requests.get(url, params=params).json();
      
      response2 = response['response']['body']['items']['item'][0]['fcstValue'];
      
      if(int(response2) <= 15):
         answer = "현재 시각, 기온는 "+ response2 + "도 입니다. 긴 옷을 추천드립니다. CLOTHES TOWER를 실행할까요?"
      elif(int(response2) > 15 and int(response2) <= 20):
         answer =  "현재 시각, 기온는 "+ response2 + "도 입니다. 환절기이니 외투를 챙기세요. CLOTHES TOWER를 실행할까요?"
      elif(int(response2) > 20):
         answer =  "현재 시각, 기온는 "+ response2 + "도 입니다. 시원한 옷을 추천드립니다. CLOTHES TOWER를 실행할까요?" 
      else:
         answer = "현재 시각, 기온는 " + response2 + "도 입니다."
      return {"answer" : answer, "response"  :response2 }