# Posture Estimation Sports Backend

`posture-estimation-sports-backend`は、スポーツにおける姿勢推定を実行するバックエンドシステムです。TensorFlowとKerasを使用して、`move_net_thunder_fp16`という姿勢推定モデルを活用します。このプロジェクトはDjangoフレームワークを使用して構築されています。

## 目次
- [概要](#概要)
- [セットアップ手順](#セットアップ手順)
- [使い方](#使い方)
- [ディレクトリ構造](#ディレクトリ構造)
- [依存関係](#依存関係)
- [ライセンス](#ライセンス)

## 概要

このプロジェクトでは、リクエストを受け取るとサーバーマシン上の動画を選択し、その動画に姿勢推定を適用します。推定結果を画像として抽出し、動画と画像リストをクライアントに返却します。

- **使用技術**:
  - **Python**: バックエンド開発のプログラミング言語
  - **Django**: Webアプリケーションフレームワーク
  - **TensorFlow**: 姿勢推定のための機械学習ライブラリ
  - **Keras**: TensorFlowの高水準API
  - **OpenCV**: 画像処理ライブラリ

## セットアップ手順

以下の手順に従って、このプロジェクトをセットアップしてください。

### 1. リポジトリのクローン

まず、リポジトリをクローンします。

```bash
git clone https://github.com/yourusername/posture-estimation-sports-backend.git
cd posture-estimation-sports-backend
```

### 2. 仮想環境の作成

次に、Pythonの仮想環境を作成し、必要な依存関係をインストールします。

#### 2.1: 仮想環境の作成

```bash
python -m venv venv
```

#### 2.2: 仮想環境の有効化

- **Windows**の場合:

```bash
venv\Scripts\activate
```

- **Mac/Linux**の場合:

```bash
source venv/bin/activate
```

### 3. 依存関係のインストール

プロジェクトに必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

### 4. データベースのマイグレーション

Djangoのデータベース設定を反映させるために、マイグレーションを実行します。

```bash
python manage.py migrate
```

### 5. 開発サーバーの起動

サーバーを起動し、プロジェクトが正しく動作するかを確認します。

```bash
python manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/` にアクセスして、Djangoのウェルカムページが表示されれば、セットアップが成功しています。

## 使い方

### 姿勢推定APIのエンドポイント

プロジェクトのバックエンドは、姿勢推定を実行するAPIエンドポイントを提供します。

- **エンドポイント**: `POST /api/posture-estimate/`
- **リクエストボディ**: 動画ファイル（MP4形式）
- **レスポンス**:
  - 姿勢推定結果が適用された動画
  - 各フレームの画像リスト

### 使い方の例

1. 動画をアップロードするリクエストを送信します。

```bash
curl -X POST -F "video=@your_video.mp4" http://127.0.0.1:8000/api/posture-estimate/
```

2. レスポンスとして、姿勢推定を適用した動画とそのコマ送り画像リストが返却されます。

### 注意点

- 動画のサイズが大きい場合、処理に時間がかかることがあります。タイムアウト設定などを考慮することをおすすめします。
- 姿勢推定の精度は使用するモデル（`move_net_thunder_fp16`）に依存します。適切なデバイスやリソースを用意してください。

## ディレクトリ構造

```
posture-estimation-sports-backend/
│
├── posture_estimation/        # Djangoアプリケーション
│   ├── migrations/            # マイグレーションファイル
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── services.py           # 姿勢推定処理を行うサービス
│
├── posture_estimation_sports_backend/  # プロジェクト設定ディレクトリ
│   ├── __init__.py
│   ├── settings.py            # プロジェクト設定
│   ├── urls.py                # URL設定
│   ├── asgi.py                # ASGI設定
│   ├── wsgi.py                # WSGI設定
│
├── requirements.txt           # 依存ライブラリリスト
├── manage.py                  # Django管理コマンド
└── .gitignore                 # Git管理に無視するファイル
```

## 依存関係

以下のライブラリがこのプロジェクトに必要です:

- `Django==5.0`
- `tensorflow==2.17.1`
- `keras==3.5.0`
- `numpy==1.26.4`
- `pandas==2.2.2`
- `opencv-python==4.7.0.72`
