import tensorflow as tf
import cv2
import numpy as np
from pathlib import Path

import logging

logger = logging.getLogger("django")


class PoseEstimator:
    """
    PoseEstimator is a utility class for performing pose estimation on video files.

    Attributes:
        infer: The TensorFlow model's inference function loaded from the given path.
    """

    def __init__(self, model_path):
        """
        Initializes the PoseEstimator with a given TensorFlow SavedModel path.

        Args:
            model_path (str): The file path to the saved model directory.
        """
        loaded_model = tf.saved_model.load(model_path)
        self.infer = loaded_model.signatures["serving_default"]

    def process_frame(self, frame):
        """
        Processes a single video frame for pose estimation.

        Args:
            frame (numpy.ndarray): The input video frame as a NumPy array.

        Returns:
            numpy.ndarray: Keypoints extracted from the frame, including [x, y, confidence].
        """

        # 入力データをリサイズ
        input_image = tf.image.resize(frame, (256, 256))  # モデル入力サイズにリサイズ
        input_image = tf.cast(input_image, dtype=tf.int32)  # データ型を tf.int32 に変更
        input_image = tf.expand_dims(input_image, axis=0)  # バッチ次元を追加

        # 推論実行
        outputs = self.infer(input=tf.constant(input_image))  # 'input' 名で渡す
        keypoints = outputs["output_0"]  # 出力を取得

        return keypoints.numpy()

    def process_video(self, video_path, output_dir):
        """
        Processes a video file for pose estimation and outputs the processed frames.

        Args:
            video_path (str): The path to the input video file.
            output_dir (str): The directory where processed frames will be saved.

        Returns:
            tuple: A tuple containing:
                - output_video_path (str): Path to the saved processed video.
                - frame_list (list): List of file paths to the processed frame images.
        """

        logger.info("動画への姿勢推定を開始します")

        # 動画の読み込み
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)  # 動画のフレームレートを取得
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 動画処理後の出力ファイルパス
        output_video_path = output_dir / "output.mp4"

        # 動画のエンコーダ設定
        frame_list = []
        frame_index = 0
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(
            str(output_video_path), fourcc, fps, (int(cap.get(3)), int(cap.get(4)))
        )

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 姿勢推定を行う
            keypoints = self.process_frame(frame)
            overlay = self.draw_keypoints(frame, keypoints)

            # 処理したフレームを動画に書き込む
            video_writer.write(overlay)

            frame_index += 1

            cap.release()
            video_writer.release()
            logger.info(f"姿勢推定をかけた動画を {output_video_path} に保存しました")

        # output.mp4 を秒間1枚ずつコマ送りで画像を取得
        logger.info("output.mp4 から1秒ごとのフレームを抽出します")
        cap = cv2.VideoCapture(str(output_video_path))
        frame_list = []
        frame_index = 0

        duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / fps
        while frame_index < duration:
            cap.set(
                cv2.CAP_PROP_POS_FRAMES, frame_index * fps
            )  # 秒単位でフレーム位置を設定
            ret, frame = cap.read()
            if not ret:
                break

            frame_output_path = output_dir / f"frame_{frame_index:04d}.png"
            cv2.imwrite(str(frame_output_path), frame)
            frame_list.append(str(frame_output_path))

            frame_index += 1

        cap.release()
        logger.info("cap.release()")

        return str(output_video_path), frame_list

    def generate_video(self, frames, output_path):
        frame = cv2.imread(frames[0])
        height, width, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(output_path, fourcc, 1, (width, height))

        for frame_path in frames:
            frame = cv2.imread(frame_path)
            video_writer.write(frame)

        video_writer.release()

    def draw_keypoints(self, frame, keypoints):
        """
        Draws keypoints on a video frame.

        Args:
            frame (numpy.ndarray): The input video frame as a NumPy array.
            keypoints (numpy.ndarray): Keypoints with [x, y, confidence].

        Returns:
            numpy.ndarray: The video frame with keypoints overlaid.
        """
        # 最初の次元（バッチサイズ）を削除
        keypoints = keypoints[0]  # shape: (6, 56)

        for i, keypoint in enumerate(keypoints):  # 関節数分ループ
            logger.info(f"Keypoint {i}: {keypoint}")
            # keypoint[0:2] は [x, y] 座標、keypoint[2] は信頼度
            if len(keypoint) >= 3:
                x, y, confidence = keypoint[0], keypoint[1], keypoint[2]
                # 信頼度が十分高い場合のみ描画
                if confidence > 0.4:
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
            else:
                logger.warning(f"Keypoint {i} has insufficient data: {keypoint}")

        return frame
