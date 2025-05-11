import cv2
import datetime

cap = cv2.VideoCapture(0)
first_frame = None

while True:
    ret, frame = cap.read()
    text = "No Motion"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        text = "Motion Detected"
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.putText(frame, f"Status: {text}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    cv2.imshow("Security Feed", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
