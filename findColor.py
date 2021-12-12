
# 매개변수로 받은 RGB 값을 기반으로 정형화된 색상 도출 



def pickColor(red,green,blue):

   print(red,green,blue);
  #빨간색 옷
   if red >= 160 :
     
    ## if green >= 190 and blue >= 190 : 
     ##  return "흰색"
     
   ##  if green >= 190 and blue <= 70 : 
   ##    return "노란색"
     
   ##  if green <= 70 and blue <= 70 : 
   ##    return "바이올렛색"
    
     if green<=120 and blue <= 120 :
      
       return "빨간색"
     
     
  
  #초록색 옷    
   elif green >= 160 :
    
     if red<=120 and blue <= 120 :
      
       return "초록색"
     
  ##   if red<=120 and blue >= 180 : 
  ##     return "민트색"
  
  #파란색 옷
   elif blue >= 170 :
    
     if red<=120 and green <= 120 :
      
       return "파란색"
     
  ## elif red <= 50 : 
  ##   if blue<=50 and green <= 40 :
  ##     return "검정색"
