import cv2
from enum import Enum
from google.cloud import vision, storage
from google.cloud.vision_v1.types.image_annotator import GcsDestination, OutputConfig
from color import nearest_color
from task import TrackingTask
from utils import bounding_box, frame_to_image, intersection, area, create_label


class Annotate(Enum):
    ALL = 0
    RELEVANT = 1
    NONE = 2


def find_suspect(task: TrackingTask, frame, annotation_level=Annotate.RELEVANT):

    frame_vision_image = frame_to_image(frame)

    vision_objects = task.vision_client.object_localization(
        image=frame_vision_image).localized_object_annotations

    for obj in vision_objects:
        obj.name = obj.name.lower()

    vision_objects.sort(key=lambda obj: -1 * task.object_priority(obj))

    batch_color_request = vision.BatchAnnotateImagesRequest()

    for obj in vision_objects:
        sx, sy, ex, ey = bounding_box(task.video, obj)
        obj_image = frame_to_image(frame[sy:ey, sx:ex])

        batch_color_request.requests.append(
            vision.AnnotateImageRequest(
                image=obj_image,
                features=[
                    vision.Feature(
                        type_=vision.Feature.Type.IMAGE_PROPERTIES
                    )
                ]
            )
        )

    vision_object_properties = task.vision_client.batch_annotate_images(
        request=batch_color_request).responses

    vision_objects_color_label = []
    for i, prop in enumerate(vision_object_properties):
        colors = prop.image_properties_annotation.dominant_colors.colors
        def color_to_rgb(c): return (c.red, c.green, c.blue)
        top_scoring_color = color_to_rgb(
            max(colors, key=lambda c: c.score).color)
        vision_objects_color_label.append(nearest_color(top_scoring_color))

    vision_results = list(zip(vision_objects, vision_objects_color_label))

    for i, (obj, color_label) in enumerate(vision_results):

        obj_box = sx, sy, ex, ey = bounding_box(task.video, obj)
        task.vision_client.batch_annotate_images()

        if obj.name == 'person':
            person_identifiers = set()

            for obj1, color_label1 in vision_results:
                name1 = obj1.name
                if name1 not in task.categorizer:
                    continue

                obj1_box = bounding_box(task.video, obj1)

                if intersection(obj_box, obj1_box) / area(obj1_box) < .75:
                    continue

                person_identifiers.add(
                    (color_label1, task.categorizer[name1]))

            if len(task.description - person_identifiers) == 0:
                color = (114, 73, 201)
                create_label(
                    frame,
                    obj_box,
                    text='SUSPECT FOUND',
                    scale=1,
                    thickness=1,
                    color=color
                )

                cv2.rectangle(frame, (sx, sy), (ex, ey), color[::-1], 5)
                return obj_box

        elif obj.name in task.categorizer:
            if (color_label, task.categorizer[obj.name]) in task.description:
                color = (222, 11, 92)
                create_label(
                    frame,
                    obj_box,
                    text=f'{color_label} {task.categorizer[obj.name]} FOUND'.upper(
                    ),
                    scale=.6,
                    thickness=1,
                    color=color
                )

                cv2.rectangle(frame, (sx, sy), (ex, ey), color[::-1], 5)
                continue

        cv2.rectangle(frame, (sx, sy), (ex, ey), (2, 184, 219)[::-1], 2)
        cv2.putText(frame, f'{i}', (sx, sy + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

    return None