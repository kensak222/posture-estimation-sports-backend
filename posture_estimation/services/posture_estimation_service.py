import tensorflow as tf
import cv2
import numpy as np
from pathlib import Path


class PostureEstimatorService:
    def __init__(self, model_path):
        self.model = tf.saved_model.load(model_path)

    def process_frame(self, frame):
        input_image = tf.image.resize(frame, (256, 256))  # モデル入力サイズにリサイズ
        input_image = tf.cast(input_image, dtype=tf.float32) / 255.0
        input_image = tf.expand_dims(input_image, axis=0)

        keypoints = self.model(input_image)
        return keypoints.numpy()

    def process_video(self, video_path, output_dir):
        cap = cv2.VideoCapture(video_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        frame_list = []
        frame_index = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            keypoints = self.process_frame(frame)
            overlay = self.draw_keypoints(frame, keypoints)

            frame_output_path = output_dir / f"frame_{frame_index:04d}.png"
            cv2.imwrite(str(frame_output_path), overlay)
            frame_list.append(str(frame_output_path))
            frame_index += 1

        cap.release()
        return str(output_dir), frame_list

    def draw_keypoints(self, frame, keypoints):
        for keypoint in keypoints[0][0]:  # 顔や関節をループ処理
            x, y, confidence = keypoint
            if confidence > 0.5:
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
        return frame
