from injector import Injector, Module, singleton, provider
from pathlib import Path

from posture_estimation.services.posture_estimation_service import (
    PostureEstimationService,
)
from .tasks.video_processor import VideoProcessor


class AppModule(Module):
    @singleton
    @provider
    def provide_video_processor(self) -> VideoProcessor:
        model_path = (
            Path(__file__).resolve().parent.parent
            / "ai_model"
            / "move_net_thunder_fp16"
        )
        return VideoProcessor(str(model_path))

    @singleton
    @provider
    def provide_posture_estimation_service(
        self, video_processor: VideoProcessor
    ) -> PostureEstimationService:
        return PostureEstimationService(video_processor)


# Injectorをアプリケーション全体で共有
injector = Injector([AppModule])
