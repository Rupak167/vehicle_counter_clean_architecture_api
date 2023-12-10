import cv2
from ultralytics import YOLO
import subprocess
import torch
import os
from PIL import Image, ImageDraw
import random

class ProcessVideoFile:

    def __init__(self, media_root):
        self.media_root = media_root
        self.count = 0

    def _different_elements(self, tensor1, tensor2):
        set1 = set(tensor1.tolist())
        set2 = set(tensor2.tolist())

        difference = set1 - set2

        return list(difference)
    
    def _toh264(self, input_file, output_file):
        cmd = [
            'ffmpeg',       # The FFmpeg executable
            '-i', input_file,   # Input file
            '-c:v', 'libx264',  # Video codec (H.264)
            '-preset', 'veryfast',  # Encoding preset
            '-crf', '18',       # Constant Rate Factor (adjust for quality)
            '-c:a', 'aac',     # Audio codec (AAC)
            '-strict', 'experimental',  # Enable experimental audio codec
            '-b:a', '192k',    # Audio bitrate
            output_file
        ]

        subprocess.run(cmd)
    def line_split_using_double_backslash(self, line):
        


    def invoke(self, model_weights_path, video_file_path, processed_file_root, processed_file_name):
        class_map = {
            0: 'bus',
            1: 'car',
            2: 'motorbike',
            3: 'truck'
        }

        counter = {
            'bus':0,
            'car':0,
            'motorbike':0,
            'truck':0
        }

        model = YOLO(model_weights_path)
        cap = cv2.VideoCapture(video_file_path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        processed_file_path = os.path.join(self.media_root, processed_file_root)
        os.makedirs(processed_file_path, exist_ok=True)
        processed_file_full_path = os.path.join(processed_file_path, processed_file_name)
        intermediate__processed_file_full_path = os.path.join(processed_file_path, 'i_' + processed_file_name)

        #image save
        processed_file_root_image = processed_file_root + "images"
        images_save_path_root = os.path.join(self.media_root, processed_file_root_image)
        os.makedirs(images_save_path_root, exist_ok=True)
        images_save_path_root = os.path.join(images_save_path_root, processed_file_name.split('.')[0])

        output_video = None

        prev_boxes = None

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()
            if output_video is None:
                output_video = cv2.VideoWriter(intermediate__processed_file_full_path, fourcc, cap.get(cv2.CAP_PROP_FPS) / 3, (frame.shape[1], frame.shape[0]))

            self.count += 1

            if self.count % 3 != 0:
                continue

            if success:
                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = model.track(frame, persist=True)

                boxes = results[0].boxes
                if prev_boxes is not None and boxes.id is not None and prev_boxes.id is not None:
                    different_elemetns_list = self._different_elements(prev_boxes.id, boxes.id)
                    if len(different_elemetns_list) > 0:
                        for x in different_elemetns_list:
                            indices = torch.where(prev_boxes.id == x)
                            index = indices[0].item() if indices[0].numel() > 0 else -1
                            counter[class_map[prev_boxes.cls[index].item()]] += 1

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                output_video.write(annotated_frame)

                if self.count % 5 != 0:
                    save_path = images_save_path_root  + str(random.randint(10000, 99999))+".png"
                    image = Image.fromarray(annotated_frame)
                    image.save(save_path)



                # Display the annotated frame
                # cv2.imshow("YOLOv8 Tracking", annotated_frame)

                prev_boxes = boxes


                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break
            
        output_video.release()
        cv2.destroyAllWindows()

        print("Here:")
        print(intermediate__processed_file_full_path)
        print(processed_file_full_path)

        intermediate__processed_file_full_path_slash = intermediate__processed_file_full_path.replace('\\', '\\\\')
        processed_file_full_path_slash = processed_file_full_path.replace('\\', '\\\\')
        
        print("Here:")
        print(intermediate__processed_file_full_path_slash)
        print(processed_file_full_path_slash)


        self._toh264(intermediate__processed_file_full_path_slash, processed_file_full_path_slash)
        os.remove(intermediate__processed_file_full_path_slash)
        
        return True, processed_file_full_path_slash, counter