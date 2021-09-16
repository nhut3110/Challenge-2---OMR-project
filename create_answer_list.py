def createAnswerList(thresh, order):
    ansList = []
    fy = 126
    y = 10
    score = 0
    tmp = order
    boxes = []
    for count in range(6):
        tmpList = []
        copyimg = thresh[y:y + fy, 0:216]
        # cv2.imshow('ttt',copyimg)
        # print('shape cua anh la ',copyimg.shape)
        # cv2.waitKey(0)
        boxes = split_image(copyimg)
        dem = -1
        maxPixels = 0
        location = -1
        question = -1
        # print('len box',len(boxes))
        for j in boxes:
            dem += 1
            pixels = cv2.countNonZero(j)
            # print(pixels,' shape la ',j.shape)
            # cv2.imshow('t',j)
            # cv2.waitKey(0)
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
                order += 1
        y = y + fy + 10
        ansList.append(tmpList)
        # print('y = ',y,' xong 5 cau',)
        boxes = []

    return ansList