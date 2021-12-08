
# 매개변수로 받은 RGB 값을 기반으로 정형화된 색상 도출 
def pickColor(red,green,blue):

  #빨간색 옷
   if red >= 180 :
    
     if green<=120 and blue <= 120 :
      
       return "빨간색"
  
  #초록색 옷    
   elif green >= 180 :
    
     if red<=120 and blue <= 120 :
      
       return "초록색"
  
  #파란색 옷
   elif blue >= 180 :
    
     if red<=120 and green <= 120 :
      
       return "파란색"

