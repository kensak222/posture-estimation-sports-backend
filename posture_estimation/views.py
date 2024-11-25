from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from pathlib import Path
import os
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import logging

from posture_estimation.services.video_processor_service import VideoProcessorService

logger = logging.getLogger("django")


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome to the Home Page!")  # ホームページ用のメッセージ


@method_decorator(csrf_exempt, name="dispatch")  # CSRFを無効にする
class ProcessVideoView(View):
    def post(self, request, *args, **kwargs):
        logger.info("process-video リクエストの処理を開始します")
        try:
            # 動画のパス（デフォルトのinput.mp4）
            video_file = request.FILES["video"]
            output_dir = Path(settings.BASE_DIR) / "posture_estimation" / "outputs"

            video_path = output_dir / video_file.name
            with open(video_path, "wb") as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            model_path = Path(settings.BASE_DIR) / "ai_model" / "move_net_thunder_fp16"
            processor = VideoProcessorService(model_path)
            output_video, frame_list = processor.process(video_path, output_dir)

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
