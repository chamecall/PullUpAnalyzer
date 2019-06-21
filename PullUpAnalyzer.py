import cv2
import sys
import Utils
import os
from PoseProcessor import PoseProcessor
from VideoProcessor import VideoProcessor

pose_processor = PoseProcessor(30, 30, 5, 1 / 2)
input_source = '/home/algernon/samba/video_queue/input/Sandel/Sandel.mp4'
json_dir = '/home/algernon/samba/video_queue/input/Sandel/Sandel_json'
output_dir = '/home/algernon/samba/video_queue/output/'

cap = cv2.VideoCapture(input_source)
filename = os.path.basename(input_source).split('.')[0]
cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_video = os.path.join(output_dir, f'{filename}_out.avi')

video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"XVID"), 24,
                               (cap_width, cap_height))
required_points = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4, "LShoulder": 5, "LElbow": 6,
                 "LWrist": 7, "MidHip": 8, "RHip": 9, "RKnee": 10, "RAnkle": 11, "LHip": 12, "LKnee": 13, "LAnkle": 14}
required_pairs = (['Neck', 'RShoulder'], ['Neck', 'LShoulder'], ['RShoulder', 'RElbow'], ['LShoulder', 'LElbow'],
                  ['RElbow', 'RWrist'], ['LElbow', 'LWrist'], ['LWrist', 'RWrist'], ['Nose', 'Neck'], ['Neck', 'MidHip'],
                  ['MidHip', 'LHip'], ['MidHip', 'RHip'], ['RHip', 'RKnee'], ['LHip', 'LKnee'], ['LKnee', 'LAnkle'], ['RKnee', 'RAnkle'])

video_processor = VideoProcessor(pose_processor, required_points, required_pairs)
video_processor.enable_debug()

for processed_frame in video_processor.process_video_with_raw_data(cap, json_dir):
    cv2.imshow('Processed frame', processed_frame)
    video_writer.write(processed_frame)
    if cv2.waitKey(1) > 0:
        break

video_writer.release()
