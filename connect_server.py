import pandas as pd

def pickColor(red,green,blue):

 closet = pd.read_csv("./closet.csv", index_col = 0)

#데이터 받아오기

 data_to_insert = {'top_bottom_others' : 0, 'length' : 1, 'color_r' : red, 'color_g' : green, 'color_b' : blue, 'material' : 8}

 closet = closet.append(data_to_insert, ignore_index=True)

 cnt_r = 0
 cnt_g = 0
 cnt_b = 0

 for i in range(0,len(closet)) :
  #빨간색 옷
   if closet['color_r'][i] >= 180 :
    
     if closet['color_g'][i]<=120 and closet['color_b'][i] :
      
       cnt_r += 1
  
  #초록색 옷    
   if closet['color_g'][i] >= 180 :
    
     if closet['color_r'][i]<=120 and closet['color_b'][i] :
      
       cnt_g += 1
  
  #파란색 옷
   if closet['color_b'][i] >= 180 :
    
     if closet['color_r'][i]<=120 and closet['color_g'][i] :
      
       cnt_b += 1

#사용자가 넣은 옷에 따른 발화
 num = len(closet)-1

 clothes = closet[num:num+1]

 if clothes['color_r'][num] > clothes['color_g'][num] :
  
   if clothes['color_r'][num] > clothes['color_b'][num] :
    
     print("빨간 색 옷은 총"+str(cnt_r)+"벌 입니다.")
    
 if clothes['color_g'][num] > clothes['color_b'][num] :
  
   if clothes['color_g'][num] > clothes['color_r'][num] :
    
     print("초록 색 옷은 총"+str(cnt_g)+"벌 입니다.")
    
 if clothes['color_b'][num] > clothes['color_r'][num] :
  
   if clothes['color_b'][num] > clothes['color_g'][num] :
    
     print("파란 색 옷은 총"+str(cnt_r)+"벌 입니다.")         