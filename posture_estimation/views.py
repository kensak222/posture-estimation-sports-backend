from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
import os

from injector import inject

from posture_estimation_sports_backend import settings

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
            logger.info("動画保存を開始")
            video_file = request.FILES.get("video")
            video_path = os.path.join(settings.TEMP_DIR, video_file.name)
            save_uploaded_file(video_file, video_path)
            logger.info("入力動画の処理を開始")
            frames_dir = os.path.join(settings.TEMP_DIR, "frames")
            pose_dir = os.path.join(settings.TEMP_DIR, "pose")
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

            # レスポンス
            output_path = "http://127.0.0.1:8000/outputs/output.mp4"
            logger.info(f"レスポンスを返却します output_path : ${output_path}")
            return JsonResponse({"video_url": output_path, "status_code": 200})

        except Exception as e:
            logger.error(f"エラー: {e}")
            return JsonResponse({"code": 500, "message": str(e)})


def save_uploaded_file(uploaded_file, destination_path):
    try:
        with open(destination_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        print(f"File saved at: {destination_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        raise
