import cv2
import os
import sys

# Usage : python src/capture.py malak A
person, letter = sys.argv[1], sys.argv[2].upper()
out_dir = os.path.join("data", "real", person, letter)
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
count = len(os.listdir(out_dir))
print("ESPACE = prendre une photo, Q = quitter")

while True:
    ok, frame = cap.read()
    if not ok:
        break
    h, w = frame.shape[:2]
    s = min(h, w)
    x0, y0 = (w - s) // 2, (h - s) // 2
    view = frame.copy()
    cv2.rectangle(view, (x0, y0), (x0 + s, y0 + s), (0, 255, 0), 2)
    cv2.putText(view, f"{person} - {letter} ({count})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Capture (place la main dans le carre)", view)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(" "):
        path = os.path.join(out_dir, f"{count:02d}.jpg")
        cv2.imwrite(path, frame)
        count += 1
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()