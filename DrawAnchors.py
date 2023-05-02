import cv2

def show_labels_img(imgname):
    img = cv2.imread(DATASET_PATH + imgname + ".jpg")
    h, w = img.shape[:2]
    # print(w,h)
    label = []
    with open("../YOLOv8/imgs/test/"+imgname+".txt",'r') as flabel:
        for label in flabel:
            label = label.split(' ')
            label = [float(x.strip()) for x in label]
            print(CLASSES[int(label[0])])
            pt1 = (int(label[1] * w-label[3] * w/2), int(label[2] * h-label[4] * h/2))
            pt2 = (int(label[1] * w+label[3] * w/2), int(label[2] * h+label[4] * h/2))
            # cv2.putText(img, CLASSES[int(label[0])], pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            cv2.putText(img, None, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))   # 不加类别标签
            cv2.rectangle(img, pt1, pt2, (0,0,255,2))

    cv2.imwrite("../YOLOv8/imgs/testDrawAnchor/%s.jpg"%(imgname),img)
if __name__ == '__main__':
    CLASSES=['pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor']   #这里是类型
    DATASET_PATH="../YOLOv8/imgs/testDrawAnchor/"
    image_ids = open('../YOLOv8/imgs/train.txt').read().strip().split()  # 读取图片名称
    for image_id in image_ids:
        show_labels_img(image_id)

