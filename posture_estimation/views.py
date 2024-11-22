from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os

from posture_estimation.services.posture_estimation_service import (
    PostureEstimationService,
)


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome to the Home Page!")  # ホームページ用のメッセージ


def session_test_view(request):
    session_id = request.session.session_key  # セッションIDを取得
    if not session_id:
        # セッションが無い場合、強制的に新しいセッションを作成
        request.session.create()

    # セッションIDを返す
    return HttpResponse(f"Session ID: {session_id}")


class ProcessVideoView(View):
    # CSRFを無効化する
    # @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # 動画ファイルの取得
        video_file = request.FILES.get("file")
        if not video_file:
            return JsonResponse({"error": "No file uploaded."}, status=400)

        # ファイルを保存
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        file_url = fs.url(filename)

        video_path = os.path.join(
            Path(__file__).resolve().parent.parent.parent, "input.mp4"
        )

        output_dir = os.path.join(
            Path(__file__).resolve().parent.parent.parent, "outputs"
        )
        os.makedirs(output_dir, exist_ok=True)

        images, output_video_path = self.process_video_and_generate_output(
            video_path, output_dir
        )

        # 画像リストと生成した動画パスを返す
        response_data = {
            "message": "Video processing completed.",
            "images": images,  # 画像リスト
            "video": output_video_path,  # 生成した動画のパス
        }
        return JsonResponse(response_data)

    # 動画に対して姿勢推定をかけ、画像リストと動画を生成する処理を行う
    def process_video_and_generate_output(self, video_path, output_dir):
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

        return images, output_video_path
