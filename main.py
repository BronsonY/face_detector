import cv2

# Load the pre-trained Haar Cascade face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Open a connection to the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Get the height and width of the frame
    height, width = frame.shape[:2]

    # Set the desired width for the window
    desired_width = 800

    # Calculate the corresponding height to maintain the aspect ratio
    desired_height = int((desired_width / width) * height)

    # Resize the frame
    frame = cv2.resize(frame, (desired_width, desired_height))

    # Display the frame in a window named 'img'
    cv2.imshow('img', frame)

    # Check for the 'Esc' key to exit the loop
    if cv2.waitKey(1) == 27:  # 27 is the ASCII code for the 'Esc' key
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()