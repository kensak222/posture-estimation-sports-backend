from pathlib import Path
import cv2

from posture_estimation.services.posture_estimation_service import (
    PostureEstimatorService,
)


class VideoProcessorService:
    def __init__(self, model_path):
        self.pose_estimator = PostureEstimatorService(model_path)

    def process(self, video_path, output_dir):
        output_video_path = Path(output_dir) / "output_video.mp4"
        frame_output_dir, frame_list = self.pose_estimator.process_video(
            video_path, output_dir
        )

        self.generate_video(frame_list, str(output_video_path))
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
