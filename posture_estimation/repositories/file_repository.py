import os
import shutil
import logging

logger = logging.getLogger("django")


class FileRepository:
    """ファイル操作を担当するリポジトリ"""

    def save_uploaded_file(self, uploaded_file, destination_path):
        try:
            with open(destination_path, "wb+") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            print(f"File saved at: {destination_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
            raise

    def delete_files_in_directory(self, directory_path):
        if os.path.exists(directory_path):
            logger.info(f"temp内の不必要なファイルを削除します: {directory_path}")
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # ファイルやリンクの削除
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # ディレクトリの削除
                except Exception as e:
                    logger.error(f"ファイル削除処理に失敗しました {file_path}: {e}")
