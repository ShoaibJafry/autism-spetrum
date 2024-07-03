import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_human_dnn(image_path):
    # Load the pre-trained MobileNet SSD model and the class names
    prototxt_path = 'deploy.prototxt'
    model_path = 'mobilenet_iter_73000.caffemodel'
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    
    classNames = {0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
                  5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair', 10: 'cow', 11: 'diningtable',
                  12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person', 16: 'pottedplant',
                  17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Could not read the image.")
        return False

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Iterate over the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # confidence threshold
            idx = int(detections[0, 0, i, 1])
            if classNames[idx] == 'person':
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 2)
                print("Human detected!")
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.axis('off')
                plt.show()
                return True
    
    print("No human detected.")
    return False

# Test with the provided image
#image_path = 'human.jpeg'
#detect_human_dnn(image_path)
