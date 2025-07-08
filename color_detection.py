import cv2
import numpy as np


# فتح الكاميرا
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # تحويل الصورة من BGR إلى HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # تحديد مدى اللون الأحمر
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    # تطبيق الماسك على الصورة الأصلية
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # العثور على الكنتورز
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "Red", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()