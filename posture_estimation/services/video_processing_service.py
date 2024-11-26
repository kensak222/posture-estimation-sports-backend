import os
import cv2
import logging
from pathlib import Path

import ffmpeg

logger = logging.getLogger("django")


class VideoProcessingService:
    def split_video_to_frames(self, video_path, output_dir):
        """動画をコマ送りして画像リストを生成する"""
        logger.info("動画を画像に分割開始")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        video = cv2.VideoCapture(video_path)
        success, image = video.read()
        count = 0
        while success:
            frame_path = os.path.join(output_dir, f"frame_{count:04d}.png")
            cv2.imwrite(frame_path, image)
            success, image = video.read()
            count += 1
        video.release()
        logger.info("動画を画像に分割完了")
        return [os.path.join(output_dir, f"frame_{i:04d}.png") for i in range(count)]

    def combine_frames_to_video(self, frame_dir, output_video):
        """画像リストを動画に変換"""
        logger.info("画像を動画に変換開始")
        frame_pattern = os.path.join(frame_dir, "frame_%04d.png")
        ffmpeg.input(frame_pattern, framerate=30).output(output_video).run()
        logger.info("画像を動画に変換完了")
