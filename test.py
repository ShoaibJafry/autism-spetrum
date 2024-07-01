import cv2

def detect_human(image_path):
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Could not read the image.")
        return False

    # Convert the image to grayscale for the classifier
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if any faces are detected
    if len(faces) > 0:
        print("Human detected!")
        return True
    else:
        print("No human detected.")
        return False

# Example usage
# Uncomment the following line and replace 'path_to_image.jpg' with your image file path
#detect_human('image.jpg')
