import numpy as np
import cv2

cap = cv2.VideoCapture(0)

echoes = []
num_echoes = 8

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frame = np.array(frame)
	
	echoes.append(frame)
	if len(echoes) >= num_echoes:
		echoes = echoes[1:]

	# Our operations on the frame come here
	echoes_np = np.array(echoes)
	maximum = np.min(echoes_np, axis=0)

	# Display the resulting frame
	cv2.imshow('frame',maximum)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()