from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from pathlib import Path
import os
import os

from posture_estimation.services.posture_estimation_service import (
    PostureEstimationService,
)

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import logging

from .dependencies import injector
from posture_estimation.tasks.video_processor import VideoProcessor

logger = logging.getLogger("django")


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome to the Home Page!")  # ホームページ用のメッセージ


@method_decorator(csrf_exempt, name="dispatch")  # CSRFを無効にする
class ProcessVideoView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # サービスインスタンスをDIコンテナから取得
        self.service = injector.get(PostureEstimationService)

    def post(self, request, *args, **kwargs):
        logger.info("process-video リクエストの処理を開始します")
        try:
            # 動画のパス（デフォルトのinput.mp4）
            video_file = request.FILES.get("video")
            if not video_file:
                return JsonResponse(
                    {
                        "error": "No video file provided in request.",
                        "response_code": 400,
                    }
                )

            output_dir = Path(settings.BASE_DIR) / "posture_estimation" / "outputs"
            output_dir.mkdir(parents=True, exist_ok=True)

            # アップロードされたファイルを保存
            logger.info("ファイル保存を開始します")
            video_path = output_dir / video_file.name
            with open(video_path, "wb") as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            output_video, frame_list = self.service.process_video(
                video_path, output_dir
            )

            return JsonResponse(
                {
                    "output_video": output_video,
                    "frame_list": frame_list,
                    "response_code": 200,
                }
            )

        except Exception as e:
            logger.error(e)
            return JsonResponse(
                {
                    "error": str(e),
                    "response_code": 500,
                }
            )
