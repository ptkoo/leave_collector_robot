import cv2

cap = cv2.VideoCapture(0)

_, img = cap.read()

if _:
	img = cv2.cvtColor(cv2.resize(img, (640, 640)), cv2.COLOR_BGR2RGB)
	cv2.imshow("test",img)

	cv2.waitKey()

	cap.release()
	cv2.destroyAllWindows()
