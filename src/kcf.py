import cv2

tracker = cv2.TrackerCSRT_create()
video = cv2.VideoCapture('data/convenience_store_2.mp4')
resize_precentage = 100
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

while True:
    timer = cv2.getTickCount()
    success,frame = video.read()
    frame = rescale_frame(frame, percent = resize_precentage)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    fps = round(fps)
    cv2.putText(frame, str(fps), (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.imshow("Tracking",frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
bbox = cv2.selectROI(frame, False)
print(bbox)
sucess = tracker.init(frame, bbox)
cv2.destroyWindow("ROI selector")

while True:
    timer = cv2.getTickCount()
    sucess, frame = video.read()
    frame = rescale_frame(frame, percent = resize_precentage )
    sucess, bbox = tracker.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    fps = round(fps)
    cv2.putText(frame, str(fps), (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    if sucess:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]),
              int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,0,255), 2, 2)
        cv2.putText(frame, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,225,0), 2)
    else:
        cv2.putText(frame, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    
    cv2.imshow("Tracking", frame)
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

    