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

    def process_frame(self, frame):
        """
        Processes a single video frame for pose estimation.

        Args:
            frame (numpy.ndarray): The input video frame.

        Returns:
            numpy.ndarray: Keypoints extracted from the frame, including [x, y, confidence].
        """
        input_image = tf.image.resize(frame, (256, 256))  # Resize to model input size
        input_image = tf.cast(input_image, dtype=tf.int32)  # Change dtype to tf.int32
        input_image = tf.expand_dims(input_image, axis=0)  # Add batch dimension

        outputs = self.infer(input=tf.constant(input_image))  # Perform inference
        keypoints = outputs["output_0"]  # Get keypoints output

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
        for i in range(keypoints.shape[1]):  # 例: 6つの関節部位を想定
            keypoint = keypoints[0, i, :]
            x, y, confidence = keypoint

            # Confidenceが大きい場合に描画
            if confidence > 0.2:
                logger.info(
                    f"信頼度が高いためキーポイントを描画します Keypoints structure: {keypoints.shape}"
                )
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
        cap = cv2.VideoCapture(video_path)
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
