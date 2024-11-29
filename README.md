# Posture Estimation Sports Backend

`posture-estimation-sports-backend`は、スポーツにおける姿勢推定を実行するバックエンドシステムです。TensorFlowとKerasを使用して、`move_net_thunder_fp16`という姿勢推定モデルを活用します。このプロジェクトはDjangoフレームワークを使用して構築されています。

## 目次
- [概要](#概要)
- [セットアップ手順](#セットアップ手順)
- [使い方](#使い方)
- [ディレクトリ構造](#ディレクトリ構造)
- [依存関係](#依存関係)

## 概要

このプロジェクトでは、リクエストを受け取るとサーバーマシン上の動画を選択し、その動画に姿勢推定を適用します。推定結果のPATHをクライアントに返却します。

- **主な使用技術**:
  - **Python 3.10.11**: バックエンド開発のプログラミング言語
  - **Django**: Webアプリケーションフレームワーク
  - **TensorFlow**: 姿勢推定のための機械学習ライブラリ
  - **Keras**: TensorFlowの高水準API
  - **OpenCV**: 画像処理ライブラリ

## セットアップ手順

<details>

<summary>クリックしてセットアップ手順を確認してください。</summary>

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
make myenv
```

#### 2.2: 仮想環境の有効化

- **Windows**の場合:

```bash
myenv\Scripts\activate
```

- **Mac/Linux**の場合:

```bash
source myenv/bin/activate
```

### 3. 依存関係のインストール

プロジェクトに必要なライブラリをインストールします。

```bash
make update_requirements
```

### 4. ffmpeg をインストールし、PATHを通す

1. [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) から Get packages & executable files > Widowsアイコン > Windows builds by BtbN > ffmpeg-master-latest-win64-gpl.zip をタップして、インストールする
  - Mac や Linux では、よしなにインストールする
2. zipを解答し、`C:\FFmpeg\bin`のようにPATHを通す

### 5. データベースのマイグレーション

Djangoのデータベース設定を反映させるために、マイグレーションを実行します。

```bash
make migrate
```

### 6. 開発サーバーの起動

サーバーを起動し、プロジェクトが正しく動作するかを確認します。

```bash
make runserver
```

ブラウザで `http://127.0.0.1:8000/` にアクセスして、Djangoのウェルカムページが表示されれば、セットアップが成功しています。

</details>

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

2. レスポンスとして、姿勢推定を適用した動画のPATHが返却されます。

3. 以下のようにして、姿勢推定された動画をGETします、ブラウザから確認するとより分かりやすいです。

```bash
curl `http://127.0.0.1:8000/[返却されたPATH]`
```

### 注意点

- 動画のサイズが大きい場合、処理に時間がかかることがあります。タイムアウト設定などを考慮することをおすすめします。
- 姿勢推定の精度は使用するモデル（`move_net_thunder_fp16`）に依存します。適切なデバイスやリソースを用意してください。

### サンプル

動画は[https://www.pexels.com/](https://www.pexels.com/) より拝借しました。  

https://github.com/user-attachments/assets/2dd9cb78-96f7-4557-8468-aee460441972
