# Makefile for posture-estimation-sports-backend project

# プロジェクトのルートディレクトリ
PROJECT_DIR := $(shell pwd)

# Python環境設定
PYTHON := python
PIP := pip

# 仮想環境ディレクトリ
VENV_DIR := myenv

# インストールに使用する依存関係
REQUIREMENTS := requirements.txt

# サーバー関連
DJANGO_MANAGE := $(PROJECT_DIR)/manage.py

# 出力ディレクトリ
OUTPUT_DIR := $(PROJECT_DIR)/outputs

# 仮想環境を作成
myenv:
	python -m venv myenv

# Djangoサーバーを起動
runserver:
	python manage.py runserver

# マイグレーションを実行
migrate:
	python manage.py migrate

# 新しい依存関係をインストール
update_requirements:
	pip install -r requirements.txt

# サーバーのテスト
test:
	python manage.py test

# 動画処理を実行するAPIエンドポイントをテスト (例: curlを使用してリクエスト送信)
test_video_processing:
	@echo "Testing video processing API..."
	curl -X POST http://localhost:8000/process-video/ -F "file=@input.mp4"
	@echo "Video processing test complete."

# フォルダや出力ファイルをクリーンアップ
clean:
	@echo "Cleaning up outputs..."
	rm -rf $(OUTPUT_DIR)
	@echo "Outputs cleaned."

# フォルダやファイルの確認 (ディレクトリやファイルを手動で管理したい場合)
list:
	@echo "Listing project files..."
	ls -R $(PROJECT_DIR)

# 仮想環境を削除
destroy-venv:
	@echo "Destroying virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Virtual environment destroyed."
