import os
import cv2
import logging
from pathlib import Path

import ffmpeg
from subprocess import CalledProcessError

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
        logger.info("動画の分割が完了")
        return [os.path.join(output_dir, f"frame_{i:04d}.png") for i in range(count)]

    def combine_frames_to_video(self, frame_dir, output_video):
        """画像リストを動画に変換"""
        logger.info("画像を動画に変換開始")
        frame_pattern = os.path.join(frame_dir, "frame_%04d.png")
        logger.info(
            f"frame_pattern = {frame_pattern}, frame_dir = {frame_dir}, output_video = {output_video}"
        )
        logger.info(f"{dir(ffmpeg)}")
        try:
            # ffmpeg-python を使用して動画を作成
            (
                ffmpeg.input(frame_pattern, framerate=30)
                .output(output_video, vcodec="libx264", pix_fmt="yuv420p")
                .run(capture_stdout=True, capture_stderr=True)
            )
            logger.info("画像を動画に変換完了")
        except CalledProcessError as e:
            logger.error(f"ffmpeg error: {e.stderr.decode()}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
