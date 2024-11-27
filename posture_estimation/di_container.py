from injector import Injector, Module, provider, singleton
from posture_estimation.services.video_processing_service import VideoProcessingService
from posture_estimation.services.posture_estimation_service import (
    PostureEstimationService,
)
from posture_estimation.repositories.file_repository import FileRepository


class AppModule(Module):
    @singleton
    @provider
    def provide_video_processing_service(self) -> VideoProcessingService:
        return VideoProcessingService()

    @singleton
    @provider
    def provide_posture_estimation_service(self) -> PostureEstimationService:
        return PostureEstimationService()


# Injectorをアプリケーション全体で共有
injector = Injector([AppModule])
