from pathlib import Path
from posture_estimation.tasks.video_processor import VideoProcessor
import logging

logger = logging.getLogger("django")


class PostureEstimationService:
    def __init__(self, video_processor: VideoProcessor):
        self.video_processor = video_processor

    def process_video(self, video_path: Path, output_dir: Path):
        logger.info("動画処理を呼び出します")
        output_video, frame_list = self.video_processor.process(video_path, output_dir)
        return output_video, frame_list
