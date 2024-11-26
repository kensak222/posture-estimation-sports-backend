import os
import shutil
from pathlib import Path


class FileRepository:
    def delete_temp(self, path="temp"):
        """
        一時ディレクトリを削除する。
        """
        if os.path.exists(path):
            shutil.rmtree(path)
