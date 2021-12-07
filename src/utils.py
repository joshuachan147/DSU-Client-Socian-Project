from google.cloud import vision
import cv2

def bounding_box(capture, vision_object):
    vid_w = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    vid_h = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    vtx = vision_object.bounding_poly.normalized_vertices
    s, e = vtx[0], vtx[2]

    return tuple(map(
        int, (s.x * vid_w, s.y * vid_h, e.x * vid_w, e.y * vid_h)))

def intersection(b1, b2):
    sx1, sy1, ex1, ey1 = b1
    sx2, sy2, ex2, ey2 = b2

    b0 = sx0, sy0, ex0, ey0 = (
        max(sx1, sx2),
        max(sy1, sy2),
        min(ex1, ex2),
        min(ey1, ey2)
    )
    
    return 0 if min(ex0 - sx0, ey0 - sy0) <= 0 else area(b0)

def area(b):
    sx, sy, ex, ey = b
    return (ex - sx) * (ey - sy)

def frame_to_image(frame):
    frame_content = cv2.imencode('.jpg', frame)[1].tobytes()
    return vision.Image(content=frame_content)

def create_label(frame, box, text = '', scale = 1, thickness = 1, color = (0,0,0)):
    sx, sy = box[:2]
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, scale, thickness)

    cv2.rectangle(frame, (sx - 2, sy - h - 15), (sx + w + 5, sy), color[::-1], -1)
    cv2.putText(frame, text, (sx, sy - 5),
    cv2.FONT_HERSHEY_DUPLEX, scale, (255,255,255), thickness)