import os
import cv2
import tensorflow as tf
from pathlib import Path

import logging

logger = logging.getLogger("django")


class PoseEstimator:
    """
    PoseEstimator handles pose estimation on a given video, processing it frame by frame.
    """

    def __init__(self, model_path):
        """
        Initialize the PoseEstimator with a TensorFlow model.
        """
        loaded_model = tf.saved_model.load(model_path)
        self.infer = loaded_model.signatures["serving_default"]

    def apply_pose_estimation(self, image_path, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        image = cv2.imread(image_path)
        input_tensor = tf.convert_to_tensor(
            [tf.image.resize(image, (256, 256))], dtype=tf.float32
        )
        outputs = self.model.signatures["serving_default"](input_tensor)
        keypoints = outputs["output_0"].numpy().reshape(-1, 3)

        # 可視化 (例: 人間の姿勢をラインで描画)
        for x, y, _ in keypoints:
            cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)

        output_path = os.path.join(output_dir, os.path.basename(image_path))
        cv2.imwrite(output_path, image)
        return output_path

    def create_video_from_frames(frame_dir, output_path, fps=30):
        images = sorted(
            [
                os.path.join(frame_dir, f)
                for f in os.listdir(frame_dir)
                if f.endswith(".png")
            ]
        )
        frame = cv2.imread(images[0])
        height, width, layers = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for image in images:
            video.write(cv2.imread(image))
        video.release()

    def process_frame(self, frame):
        """
        Processes a single video frame for pose estimation.

        Args:
            frame (numpy.ndarray): The input video frame.

        Returns:
            numpy.ndarray: Keypoints extracted from the frame, including [x, y, confidence].
        """
        input_image = tf.image.resize(frame, (256, 256))
        input_image = tf.cast(input_image, dtype=tf.int32)
        input_image = tf.expand_dims(input_image, axis=0)

        outputs = self.infer(input=tf.constant(input_image))
        # Output is a [1, 1, 17, 3] tensor.
        keypoints = outputs["output_0"]

        return keypoints.numpy()

    def draw_keypoints(self, frame, keypoints):
        """
        Draws keypoints on a video frame.

        Args:
            frame (numpy.ndarray): The input video frame.
            keypoints (numpy.ndarray): Keypoints with [x, y, confidence].

        Returns:
            numpy.ndarray: The video frame with keypoints overlaid.
        """
        logger.info("キーポイントを描画します")
        logger.info(f"Keypoints structure: {keypoints.shape}")
        logger.info(f"Keypoints content: {keypoints}")

        # keypoints の形状を確認し、適切にループ処理を行います
        for i in range(keypoints.shape[1]):  # 6つの関節部位
            keypoint = keypoints[0, i, :]
            logger.info(f"Keypoint: {keypoint}")

            # 最初の3つの値 (x, y, confidence) を抽出
            if len(keypoint) >= 3:  # 3つの要素が存在する場合
                x, y, confidence = keypoint[:3]
            else:
                logger.warning(f"Unexpected keypoint format: {keypoint}")
                continue  # この keypoint は無視

            if confidence > 0.2:
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)

        return frame

    def process_video(self, video_path, output_dir):
        """
        Processes a video, applies pose estimation to each frame, and saves the resulting video as output.mp4.

        Args:
            video_path (str): Path to the input video file.
            output_dir (str): Directory to save the processed output video.

        Returns:
            str: Path to the saved output video (output.mp4).
        """
        logger.info("動画への姿勢推定を開始します")
        cap = cv2.VideoCapture(str(Path(video_path)), 0)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the input video
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_video_path = output_dir / "output.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(
            str(output_video_path), fourcc, fps, (int(cap.get(3)), int(cap.get(4)))
        )  # VideoWriter

        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Apply pose estimation to the frame
            keypoints = self.process_frame(frame)
            # Draw keypoints on the frame
            overlay = self.draw_keypoints(frame, keypoints)

            # Write the processed frame to the output video
            video_writer.write(overlay)
            frame_index += 1

        # Release the video objects
        cap.release()
        video_writer.release()
        logger.info(f"姿勢推定をかけた動画を {output_video_path} に保存しました")

        return str(output_video_path)
