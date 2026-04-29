# uninstall_docker.sh

これはDockerを完全にアンインストールするためのスクリプトです。`Debian 12`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

- すべてのDockerサービスを停止
- すべてのDocker関連パッケージをアンインストール
- Dockerデータディレクトリと設定ファイルを削除
- システム内のDocker残留ファイルをクリーンアップ
- aptキャッシュを更新

## 使用方法

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/uninstall_docker.sh && sudo chmod +x ./uninstall_docker.sh && sudo ./uninstall_docker.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/uninstall_docker.sh && sudo chmod +x ./uninstall_docker.sh && sudo ./uninstall_docker.sh
```

注意: このスクリプトはシステムレベルの操作を実行するため、sudo権限が必要です。

## 注意事項

- このスクリプトはDocker関連のすべてのデータと設定を**完全に削除**します。含まれるもの:
  - すべてのDockerコンテナ
  - すべてのDockerイメージ
  - すべてのDockerボリューム
  - すべてのDockerネットワーク
  - すべてのDocker設定
- このスクリプトを実行する前に、重要なDockerデータをバックアップしてください
- スクリプトは`|| true`構文を使用して、一部のコマンドが失敗してもスクリプト全体が続行されるようにします
- このスクリプトは主に公式の方法でインストールされたDockerを対象としています。他の方法でインストールした場合、追加のクリーンアップステップが必要になる場合があります

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/uninstall_docker.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/uninstall_docker.sh
## © 作者

SDCOM