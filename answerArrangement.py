def answerArrangement(list):
          num = len(list)
          
          cnt1 = 0
          cnt2 = 0 
          
          # 여기서 조금 더 세분화하면 사계절 구분 가능 
          for i in range(0,num):
             if list[i] < 5:
                print(list[i]);
                cnt1 += 1
             else:
                cnt2 += 1
         
          if cnt1 >= num-1:
            answer = "겨울"
          elif cnt2 >= num-1:
            answer = "여름"
          else:
            answer = "환절기입니다. 여러 종류의 옷을 구비해 두시는게 좋을 것 같네요. 그래도 옷장을 정리하시겠습니까?"
          return answer;