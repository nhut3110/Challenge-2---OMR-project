##### Import các thư viện và biến cần thiết
import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import time

questionsF = 5
answersF = 5
correct_ans_col1 = []
correct_ans_col2 = []
difficult = [0 for i in range(62)]
ansAll = []
pathData = "C:/Users/ASUS/Desktop/challenge 2/Data/"
pathCSV = "C:/Users/ASUS/Desktop/challenge 2/CSV Result/"

##### Hàm tính thời gian
class Timer(object):
    def __init__(self):
        self.times = []
        self.start()

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.times.append(time.time() - self.start_time)
        return self.times[-1]

##### Hàm để cắt nhỏ ảnh ra thành các ô tô đáp án
def split_image(image):
    r = len(image) // questionsF * questionsF 
    c = len(image[0]) // answersF * answersF
    image = image[:r, :c]
    rows = np.vsplit(image, questionsF)
    boxes = []
    for row in rows:
        cols = np.hsplit(row, answersF)
        for box in cols:
            boxes.append(box)
    return boxes

##### Hàm để tô những câu đúng sai nhưng chưa hoàn thiện
def drawAns(check, img_original, colnum, socau, ansOfStudent, correct_ans, locationF, locationS):
	red = (0, 0, 255)
	green = (0, 255, 0)
	radius = 5
	h = 25
	w = 43
	if colnum == 1: x = 130
	else: x = 490
	d1 = ( x + w*(ansOfStudent), 150 + locationF + (socau%5-1 if socau%5 != 0 else 4)*h)
	#d2 = ( x + w*(ansOfStudent) + w, 150 + locationF + (socau%5-1)*h)
	#d3 = ( x + w*(ansOfStudent), 150 + locationF + (socau%5-1)*h + h)
	d4 = ( x + w*(ansOfStudent) + w, 150 + locationF + (socau%5-1 if socau%5 != 0 else 4)*h + h)
	center = ((d1[0]+d4[0])//2, (d1[1]+d4[1])//2)
	#img_original = cv2.cỉrcle(img_original, center, radius, green, -1)

	return center

##### Hàm tính toán và chấm điểm đúng sai cho từng bài làm
def calc(thresh, correct_ans, socau, numberQues, colNum, img_original):
	if numberQues <= 0:
		return 0
	ansOfStudent = []
	fy = 126
	y = 10
	score = 0
	tmp = socau
	boxes = []
	center = []
	rangeNum = numberQues//5 if numberQues%5 == 0 else (numberQues//5)+1
	for count in range(rangeNum):
		copyimg = thresh[y:y+fy,0:216]
		#cv2.imshow('ttt',copyimg)
		#print('shape cua anh la ',copyimg.shape)
		#cv2.waitKey(0)
		correct_answer = correct_ans[count]
		boxes = split_image(copyimg)
		dem = -1
		maxPixels = 0
		location = -1
		question = -1
		#print('len box',len(boxes))
		for j in boxes:
			dem+=1
			pixels = cv2.countNonZero(j)
			#print(pixels,' shape la ',j.shape)
			#cv2.imshow('t',j)
			#cv2.waitKey(0)
			if pixels > maxPixels:
				maxPixels = pixels
				location = dem
			if dem == 4:
				ans = location
				question += 1
				if ans == correct_answer[question] and socau < tmp + numberQues:
					score +=1	
					center.append(drawAns(True, img_original, colNum, socau+1, ans, correct_answer[question], y, y+fy))
				else:
					difficult[socau] += 1
					center.append(drawAns(True, img_original, colNum, socau+1, ans, correct_answer[question], y, y+fy))
				dem = -1
				maxPixels = 0
				location = -1
				socau += 1
				if ans == 0: f_ans = 'A'
				if ans == 1: f_ans = 'B'
				if ans == 2: f_ans = 'C'
				if ans == 3: f_ans = 'D'
				if ans == 4: f_ans = 'E'
				ansOfStudent.append(f_ans)
				#print(j.shape)
				locationOfQuestion = str(socau) if socau >=10 else '0'+str(socau)
				#if socau <= tmp + numberQues:
				#	print('cau', locationOfQuestion, 'dap an duoc chon la',f_ans)
		y = y +fy +10
		#print('y = ',y,' xong 5 cau',)
		boxes = []	
	return score,ansOfStudent,center

##### Hàm này giúp đọc vào đáp án từ mã đề cho sẵn và lưu vào list
def createAnswerList(thresh, socau):
	ansList = []
	fy = 126
	y = 10
	score = 0
	tmp = socau
	boxes = []
	for count in range(6):
		tmpList = []
		copyimg = thresh[y:y+fy,0:216]
		#cv2.imshow('ttt',copyimg)
		#print('shape cua anh la ',copyimg.shape)
		#cv2.waitKey(0)
		boxes = split_image(copyimg)
		dem = -1
		maxPixels = 0
		location = -1
		question = -1
		#print('len box',len(boxes))
		for j in boxes:
			dem+=1
			pixels = cv2.countNonZero(j)
			#print(pixels,' shape la ',j.shape)
			#cv2.imshow('t',j)
			#cv2.waitKey(0)
			if pixels > maxPixels:
				maxPixels = pixels
				location = dem
			if dem == 4:
				ans = location
				question += 1
				tmpList.append(ans)	
				dem = -1
				maxPixels = 0
				location = -1
				socau += 1
		y = y +fy +10
		ansList.append(tmpList)
		#print('y = ',y,' xong 5 cau',)
		boxes = []
		
	return ansList
	
##### Hàm nãy để xử lý chung ảnh đề mẫu đọc vào
def readAnswerModule(imgName):
	img_original = cv2.imread(imgName)
	socau = 0 
	global correct_ans_col1
	global correct_ans_col2

	img = img_original[150:970,130:350]
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur_img = cv2. GaussianBlur(gray_img, (5, 5), 0)
	_, thresh = cv2. threshold(blur_img, 170, 255, cv2.THRESH_BINARY_INV)
	correct_ans_col1 = createAnswerList(thresh,socau)

	socau = 30
	img = img_original[150:970,490:710]
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur_img = cv2. GaussianBlur(gray_img, (5, 5), 0)
	_, thresh = cv2. threshold(blur_img, 170, 255, cv2.THRESH_BINARY_INV)
	correct_ans_col2 = createAnswerList(thresh,socau)
	#print(correct_ans_col1)
	#print(correct_ans_col2)

##### Phần chính của cả challenge 2, giúp xử lý từng bài làm của học sinh và chấm điểm chúng
def mainProcessGrading(imgName, numberOfQuestions, correct_ans_col1, correct_ans_col2):
	img_original = cv2.imread(imgName)
	score = 0
	socau = 0 
	center = []
	global ansAll
	mylist = []
	tmpL = []
	tmpN = 0
	tmpC = []
	if numberOfQuestions > 30:
		num1 = 30
		num2 = numberOfQuestions -30
	else:
		num1 = numberOfQuestions
		num2 = 0
	img = img_original[150:970,130:350]
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur_img = cv2. GaussianBlur(gray_img, (5, 5), 0)
	_, thresh = cv2. threshold(blur_img, 170, 255, cv2.THRESH_BINARY_INV)
	tmpN,tmpL,tmpC = calc(thresh,correct_ans_col1,socau,num1,1,img_original)
	score += tmpN
	mylist += tmpL
	center += tmpC

	socau = 30
	img = img_original[150:970,490:710]
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur_img = cv2. GaussianBlur(gray_img, (5, 5), 0)
	_, thresh = cv2. threshold(blur_img, 170, 255, cv2.THRESH_BINARY_INV)
	tmpN,tmpL,tmpC = calc(thresh,correct_ans_col2,socau,num2,2,img_original)
	score += tmpN
	mylist += tmpL
	center += tmpC

	print(str(score)+'/'+str(numberOfQuestions))
	ansAll.append(mylist)
	#for i in center:
	#	img_original = cv2.circle(img_original, i, 10, (0, 0, 255), 2)
	#	print(i)
	#	cv2.imshow('test',img_original)
	#	cv2.waitKey(0)
	return score

################## Đây là mục xử lý chính của file

##### Đọc đáp án từ mã đề cho sẵn
timer = Timer()
timer.start()
readAnswerModule('C:/Users/ASUS/Desktop/challenge 2/Answer/3A.png')

##### Đọc filename và lưu thông tin và tạo DataFrame Student
filenames = os.listdir(pathData)
df = pd.DataFrame()
df['filenames'] = filenames
df1 = df['filenames'].str.split('_', expand=True)
student = pd.DataFrame()
student['Student ID'] = df1[0]
df2 = pd.DataFrame()
df2 = df1[2].str.split('.', expand=True)
studentNames = df1[1].values.tolist()
lastNames = []
surNames = []
firstNames = []
for name in studentNames:
	turn = 0
	count = len(name) - 1
	tmpSurName = ''
	tmpFirstName = name[count]
	
	while not name[count].isupper():
		count -= 1
		tmpFirstName = name[count] + tmpFirstName
		name = name[:-1]
	name = name[:-1]
	count = 1
	tmp = name[0]
	while count <= len(name) -1 :
		if not name[count].isupper():
			tmp += name[count]
			count +=1
		else:
			tmpSurName = tmpSurName + tmp + ' '
			tmp = name[count]
			count += 1

	tmpSurName += tmp
	surNames.append(tmpSurName)
	firstNames.append(tmpFirstName)
student['Sur Name'] = surNames
student['First Name'] = firstNames
student['Code'] = df2[0]
index = 0
grades = []
result = []
print('file student la','\n',student,'\n')

##### Xử lý và chấm từng bài làm
for file in filenames:
	pathNew = pathData + file
	print('\ndiem cua',student['Sur Name'][index] + ' ' + student['First Name'][index],'la ',end='')
	score = mainProcessGrading(pathNew, 60, correct_ans_col1, correct_ans_col2)
	grades.append(score)
	if score > 30:
		result.append('Pass')
	else:
		result.append('Fail')
	print('5 cau dau tien la',ansAll[index][0:5])
	print('toan bo dap an da to la',ansAll[index])
	index += 1

##### Lưu điểm sau khi chấm vào DataFrame
grading = pd.DataFrame()
grading['Student ID'] = student['Student ID']
grading['Grading'] = grades
grading['Final result'] = result
print('\n\n file grading la','\n',grading)

##### So sánh và tìm 3 câu khó nhất
dif = pd.DataFrame()
dif['difficulty'] = difficult[0:60]
dif = dif.sort_values('difficulty', ascending=False)
#print(dif['difficulty'])
threeDifficultQuestions = list(dif['difficulty'][0:3].index)
threeDifficultQuestions.sort(reverse=False)
print('\nba cau kho nhat la',threeDifficultQuestions)
print('Time to exec %.5f sec' % timer.stop())

##### Xuất ra file CSV như yêu cầu
pathStudent = pathCSV + 'student.csv'
pathGrading = pathCSV + 'grading.csv'
student.to_csv(pathStudent)
grading.to_csv(pathGrading)
print('\nDa xuat ra file CSV la student.csv va grading.csv\n')