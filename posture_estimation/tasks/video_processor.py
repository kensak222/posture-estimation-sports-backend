import os
from pathlib import Path
import cv2

from posture_estimation.tasks.pose_estimator import (
    PoseEstimator,
)

import logging

logger = logging.getLogger("django")


class VideoProcessor:
    def __init__(self, model_path):
        self.pose_estimator = PoseEstimator(model_path)

    def process(self, video_path, output_dir):
        logger.info("動画処理を開始します")

        # ステップ 1: フレーム抽出
        frame_list = self.extract_frames(video_path, output_dir)

        # ステップ 2: 姿勢推定適用
        processed_dir = "outputs/processed"
        processed_frames = [
            self.pose_estimator.apply_pose_estimation(frame, processed_dir)
            for frame in frame_list
        ]

        # ステップ 3: 動画生成
        final_video_path = "outputs/output.mp4"
        self.pose_estimator.create_video_from_frames(processed_dir, final_video_path)

        return final_video_path, processed_frames

    def extract_frames(video_path, output_dir, frame_rate=1):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(str(Path(video_path)), 0)
        count = 0
        success, frame = cap.read()
        while success:
            if (
                int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                % (cap.get(cv2.CAP_PROP_FPS) // frame_rate)
                == 0
            ):
                output_path = os.path.join(output_dir, f"frame_{count:04d}.png")
                cv2.imwrite(output_path, frame)
                count += 1
            success, frame = cap.read()
        cap.release()
        return [os.path.join(output_dir, f) for f in sorted(os.listdir(output_dir))]
