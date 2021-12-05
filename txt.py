# # nugu speaker로 다시 전송할 데이터 
      
      # weather
      
      # list1.append(weather)
      
      # if len(list1)%5 == 0:
         
      #    num = len(list1)
         
      #    cnt1 = 0
      #    cnt2 = 0
            
      #       for i in range(num, num-5) :
               
      #          if list1[i] > 10 : # 온도 체크 로직 
                  
      #             cnt1 += 1
                  
      #       for i in range(num, num-5) :
               
      #          if list1[i] < 0 :   # 온도 체크 로직 
                  
      #             cnt2 += 1
            
      #       #더울 때      
      #       if cnt1 == 5 :
               
      #          print
      
      #       #추울 때      
      #       if cnt2 == 5 :
               
      #          print
         
      #    if(temp > 20)
           
      #    else if (temp < 20)
         
         
         
      
      
      # list1.append(num)
      
      
      
      
      
      
      
      # if len(list1) > 5 :
         
      #    for i in list1  :
         
      #       cnt = 0
         
      #       if i > 10 :
            
      #          cnt += 1
            
      #       if cnt >5 :
            
      #          print



  # today02am = cur_time.replace(hour=2, minute=0);
      # today05am = cur_time.replace(hour=5, minute=0);
      # today08am = cur_time.replace(hour=8, minute=0);w
      # today11am = cur_time.replace(hour=11, minute=0);
      # today14pm = cur_time.replace(hour=14, minute=0);
      # today17pm = cur_time.replace(hour=17, minute=0);
      # today20pm = cur_time.replace(hour=20, minute=0);
      # today23pm = cur_time.replace(hour=23, minute=0);
      
      
      # if cur_time >= today02am and cur_time < today05am : 
      #    cur_time = today02am;
      
      # if cur_time >= today05am and cur_time < today08am : 
      #    cur_time = today05am;
      
      # if cur_time >= today08am and cur_time < today11am : 
      #    cur_time = today08am;
      
      # if cur_time >= today11am and cur_time < today14pm : 
      #    cur_time = today11am;
      
      # if cur_time >= today14pm and cur_time < today17pm : 
      #    cur_time = today14pm;
         
      # if cur_time >= today17pm and cur_time < today20pm : 
      #    cur_time = today17pm;
         
      # if cur_time >= today20pm and cur_time < today23pm : 
      #    cur_time = today20pm;
         
      # if cur_time >= today23pm or cur_time < today02am :
      #    cur_time = today23pm;
    #    print(cur_time);


     #장소에 대한 parameter를 nugu 스피커에서 post 요청으로 받아온 후 파싱
      # global todo2;
      # todo2 = request2.json;
      # location = todo2.get("action").get("parameters").get("location").get("value");


      # ================================== Google Image Vision을 통한 옷 이미지 인식 기능 =================================        
        
# def rgb_to_hex(r, g, b):
#     r, g, b = int(r), int(g), int(b)
#     return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
# def run_vision(file_name):
#   client = vision.ImageAnnotatorClient()
#   os.environ.get("GOOGLE_APPLICATION_CREDENTIALS");


#   with io.open(file_name, 'rb') as image_file: 
#     content = image_file.read()

#   image = vision.Image()
#   image.content = content;

#   response = client.image_properties(image = image)
  
#   labels = response.image_properties_annotation;
#   print(labels)
#   for color in labels.dominant_colors.colors:
#     print("color = " + rgb_to_hex(int(color.color.red),int(color.color.green),int(color.color.blue)) + " percentage : " +str(int(color.score * 100))+"%")
   
#   return labels;        
# @api.route("/vision")
# class Vision(Resource):
    
#   def get(self):
#     print("google vision api start...!")
#     result = run_vision("./image/cloth.png");
#     return "success";



# =======================================================

# def closest_colour(requested_colour):
#     min_colours = {}
#     for key, name in webcolors.css3_hex_to_names.items():
#         r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#         rd = (r_c - requested_colour[0]) ** 2
#         gd = (g_c - requested_colour[1]) ** 2
#         bd = (b_c - requested_colour[2]) ** 2
#         min_colours[(rd + gd + bd)] = name
#     return min_colours[min(min_colours.keys())]

# def get_colour_name(requested_colour):
#     try:
#         closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
#     except ValueError:
#         closest_name = closest_colour(requested_colour)
#         actual_name = None
#     return actual_name, closest_name

# requested_colour = (119, 172, 152)
# actual_name, closest_name = get_colour_name(requested_colour)


# 
# print "Actual colour name:", actual_name, ", closest colour name:", closest_name    
#==================================================================       