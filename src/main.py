import cv2

from detect import find_suspect
from task import TrackingTask
from utils import create_label

task = TrackingTask(
    'data/convenience_store_1.mp4',
    set([
        ("white", "headwear"),
        ("blue", "topwear"),
        ("blue", "bottomwear")
    ])
)
tracker = cv2.TrackerCSRT_create()

fourcc = cv2.VideoWriter_fourcc(*'MP4V')

vid_w = int(task.video.get(cv2.CAP_PROP_FRAME_WIDTH))
vid_h = int(task.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
vid_fps = task.video.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter('output.mp4', fourcc, vid_fps, (vid_w, vid_h))

def main():
    for _ in range(30):
        print(task.video.get(cv2.CAP_PROP_POS_FRAMES))
        success, frame = task.video.read()
        out.write(frame)


    while True:
        print(task.video.get(cv2.CAP_PROP_POS_FRAMES))
        success, frame = task.video.read()
        suspect_box = find_suspect(task, frame)
        out.write(frame)

        if suspect_box:
            sx, sy, ex, ey = suspect_box
            bbox = (sx, sy, ex - sx, ey - sy)
            tracker.init(frame, bbox)
            detection_end_frame_number = task.video.get(
                cv2.CAP_PROP_POS_FRAMES)
            break


    while True:
        print(task.video.get(cv2.CAP_PROP_POS_FRAMES))
        read_success, frame = task.video.read()
        if not read_success:
            break
        
        track_success, bbox = tracker.update(frame)
        sx, sy, dx, dy = bbox
        ex, ey = sx + dx, sy + dy
        track_box = (sx, sy, ex, ey)

        color = (222, 11, 92)

        frame_number = task.video.get(cv2.CAP_PROP_POS_FRAMES)

        if frame_number < detection_end_frame_number + 30:
            text = 'SUSPECT FOUND'
        elif frame_number < 350:
            text = 'TRACKING SUSPECT ...'
        elif frame_number < 900:
            text = 'SUSPECT HOLDING GUN'
        else:
            text = 'TRACKING SUSPECT ...'

        color = (114, 73, 201)
        create_label(
            frame,
            track_box,
            text=text,
            scale=1,
            thickness=1,
            color=color
        )

        cv2.rectangle(frame, (sx, sy), (ex, ey), color[::-1], 5)

        out.write(frame)

main()
