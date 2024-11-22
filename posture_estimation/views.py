from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
import os
from .services.posture_estimation_service import PostureEstimationService
from pathlib import Path


# APIリクエストを受け取り、動画を処理して返す
class ProcessVideoView(View):
    def post(self, request, *args, **kwargs):
        video_path = os.path.join(
            Path(__file__).resolve().parent.parent.parent, "input.mp4"
        )

        output_dir = os.path.join(
            Path(__file__).resolve().parent.parent.parent, "outputs"
        )
        os.makedirs(output_dir, exist_ok=True)

        model_path = os.path.join(
            Path(__file__).resolve().parent.parent.parent,
            "ai_model",
            "move_net_thunder_fp16",
        )
        posture_service = PostureEstimationService(model_path)

        # 姿勢推定をかけた画像リストの生成
        images = posture_service.process_video(video_path, output_dir)

        # 姿勢推定をかけた動画の生成
        output_video_path = os.path.join(output_dir, "output_video.mp4")
        posture_service.generate_video_with_pose(video_path, output_video_path)

        return JsonResponse(
            {"status": "success", "output_video": output_video_path, "images": images}
        )
