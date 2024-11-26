import shutil
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
import os

from injector import inject

from .di_container import injector
from posture_estimation.services.posture_estimation_service import (
    PostureEstimationService,
)
from posture_estimation.services.video_processing_service import VideoProcessingService

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import logging

logger = logging.getLogger("django")


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome to the Home Page!")  # ホームページ用のメッセージ


@method_decorator(csrf_exempt, name="dispatch")  # CSRFを無効にする
class ProcessVideoView(View):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_service = injector.get(VideoProcessingService)
        self.posture_service = injector.get(PostureEstimationService)

    def post(self, request):
        logger.info("process_videoリクエストを受け取りました")
        try:
            # 入力動画の処理
            logger.info("入力動画の処理を開始")
            video_path = request.FILES["video"].temporary_file_path()
            temp_dir = "temp"
            frames_dir = os.path.join(temp_dir, "frames")
            pose_dir = os.path.join(temp_dir, "pose")
            frames = self.video_service.split_video_to_frames(video_path, frames_dir)

            # 姿勢推定処理
            logger.info("姿勢推定処理を開始")
            for frame in frames:
                pose_output = os.path.join(pose_dir, os.path.basename(frame))
                self.posture_service.estimate_pose(frame, pose_output)

            # 動画再構成
            logger.info("動画再構成を開始")
            output_video = "outputs/output.mp4"
            self.video_service.combine_frames_to_video(pose_dir, output_video)

            # 一時ファイル削除
            logger.info("一時ディレクトリ削除")
            shutil.rmtree(temp_dir)

            # レスポンス
            return JsonResponse({"video_url": output_video, "status_code": 200})

        except Exception as e:
            logger.error(f"エラー: {e}")
            return JsonResponse({"code": 500, "message": str(e)})
