
# import the necessary packages
import cv2 as cv

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

def pedestrainDetector(input_image):
# initialize the HOG descriptor/person detector


        # load the image and resize it to (1) reduce detection time
        # and (2) improve detection accuracy

    image = cv.resize(input_image,(int(240),int(180)))
    # image = imutils.resize(image, width=min(200, image.shape[1]))
    orig = image.copy()

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image)


    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        pad_w, pad_h = int(0.1*w), int(0.1*h)
        cv.rectangle(image, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), 2)

    cv.imshow("RESULT", image)

    return rects

image = "p5.jpg"
input_image = cv.imread(image)

result=pedestrainDetector(input_image=input_image)

if len(result) > 0:
    result = True
else:
    result = False

print (result)

cv.waitKey(0)

