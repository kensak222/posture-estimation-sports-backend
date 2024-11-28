from posture_estimation.repositories.file_repository import FileRepository


class FileService:
    """ファイル操作のサービス層"""

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    def save_uploaded_file(self, uploaded_file, destination_path):
        self.file_repository.save_uploaded_file(uploaded_file, destination_path)

    def clean_directories(self, directories):
        """指定されたディレクトリ内のすべてのファイルを削除"""
        for directory in directories:
            self.file_repository.delete_files_in_directory(directory)
