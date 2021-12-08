def answerArrangement(list):
          num = len(list)
          
          cnt1 = 0
          cnt2 = 0 
          cnt3 = 0
          
          # 여기서 조금 더 세분화하면 사계절 구분 가능 
          for i in range(0,num):
             if list[i] < 10:     # 겨울 
                print(list[i]);
                cnt1 += 1
             elif list[i] >= 10 and list[i] < 20:
                print(list[i])    # 환절기 
                cnt2 += 1
             else:                # 여름 
                cnt3 += 1
         
          if cnt1 >= num-1:
            answer = "겨울"
          elif cnt2 >= num-1:
            answer = "환절기"
          else:
            answer = "여름"
          return answer;