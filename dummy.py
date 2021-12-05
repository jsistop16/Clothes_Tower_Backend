import pandas as pd

data = {
#0 = top, 1 = bottom, 2 = others
"top_bottom_others" : [0,0,0,0,0,0,0,0],
#0 = short, 1 = long
"length" : [0,1,0,0,1,1,0,0],
"color_r" : [234,210,50,84,70,63],
"color_g" : [80,90,240,221,93,40],
"color_b" : [73,87,59,45,209,222],
    #기모 = 1, 나일론 = 2, 데님 = 3, 면 = 4, 스웨이드 = 5, 폴리 = 6
    #린넨 = 7, 울 = 8, 아크릴 = 9, 캐시미어 = 10, 기타 = 11
"material" : [1,2,3,5,6,7,10,8]
}

df = pd.DataFrame(data)

df.to_csv("./closet.csv")
# C:\\Users\\jemin\\OneDrive\\바탕 화면\\2학년 2학기\\인공지능및응용\\closet.csv