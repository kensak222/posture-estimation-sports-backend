from injector import Binder, Injector, Module, provider, singleton
from posture_estimation.services.file_service import FileService
from posture_estimation.services.video_processing_service import VideoProcessingService
from posture_estimation.services.posture_estimation_service import (
    PostureEstimationService,
)
from posture_estimation.repositories.file_repository import FileRepository


class AppModule(Module):
    ### services
    @singleton
    @provider
    def provide_video_processing_service(self) -> VideoProcessingService:
        return VideoProcessingService()

    @singleton
    @provider
    def provide_posture_estimation_service(self) -> PostureEstimationService:
        return PostureEstimationService()

    @singleton
    @provider
    def provide_file_service(self, file_repository: FileRepository) -> FileService:
        """FileService に FileRepository を注入してインスタンスを提供"""
        return FileService(file_repository)

    ### repositories
    @singleton
    @provider
    def provide_file_repository(self) -> FileRepository:
        """FileRepository のインスタンスを提供"""
        return FileRepository()


# Injectorをアプリケーション全体で共有
injector = Injector([AppModule])
