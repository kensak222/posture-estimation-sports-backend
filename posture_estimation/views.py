from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.core.files.storage import FileSystemStorage
import os


class ProcessVideoView(View):
    def post(self, request, *args, **kwargs):
        # 動画ファイルの取得
        video_file = request.FILES.get("file")
        if not video_file:
            return JsonResponse({"error": "No file uploaded."}, status=400)

        # ファイルを保存
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        file_url = fs.url(filename)

        # ここに姿勢推定処理を追加（例: 動画の処理、画像生成など）
        # 生成した画像と動画を返す処理をここに追加

        # 仮のレスポンス
        response_data = {
            "message": "Video processing started.",
            "video_file": file_url,
        }
        return JsonResponse(response_data)
