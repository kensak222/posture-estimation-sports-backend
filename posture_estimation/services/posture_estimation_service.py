import cv2
import tensorflow as tf
import numpy as np
import os
from pathlib import Path


# 姿勢推定を行うためのロジックを実装
class PostureEstimationService:
    def __init__(self, model_path: str):
        self.model = tf.saved_model.load(model_path)
        self.model_fn = self.model.signatures["serving_default"]

    def infer(self, frame: np.ndarray):
        # モデルに入力するための前処理
        input_tensor = tf.convert_to_tensor(frame)
        input_tensor = input_tensor[tf.newaxis, ...]

        # 姿勢推定を行う
        output = self.model_fn(input_tensor)

        return output

    def process_video(self, video_path: str, output_dir: str) -> list:
        cap = cv2.VideoCapture(video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        frame_count = 0
        images = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % int(frame_rate) == 0:  # 1秒ごとにフレームを処理
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 姿勢推定をかける
                output = self.infer(frame_rgb)

                # 結果を画像として保存
                frame_output_path = os.path.join(output_dir, f"frame_{frame_count}.png")
                cv2.imwrite(frame_output_path, frame)

                images.append(frame_output_path)

        cap.release()
        return images

    def generate_video_with_pose(self, video_path: str, output_video_path: str):
        cap = cv2.VideoCapture(video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 姿勢推定をかけて結果を描画する
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = self.infer(frame_rgb)

            # 姿勢推定の結果を元の画像に描画
            frame_with_pose = self.draw_pose(frame, output)

            frames.append(frame_with_pose)
            frame_count += 1

        cap.release()

        # 動画保存
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            output_video_path, fourcc, frame_rate, (frame.shape[1], frame.shape[0])
        )

        for frame in frames:
            out.write(frame)

        out.release()

    def draw_pose(self, frame, output):
        # 結果をフレームに描画するロジック
        # 姿勢推定結果の関節座標を描画する部分
        return frame  # この部分を実装する
