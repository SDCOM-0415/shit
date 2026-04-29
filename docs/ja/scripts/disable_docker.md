# disable_docker.sh

これはDockerを完全に無効化して再インストールを防止するためのスクリプトです。`Debian 12` `Ubuntu 22.04`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

Dockerを完全に無効化して再インストールを防止します。このスクリプトは:

1. すべてのDocker関連サービスを停止および無効化
2. Docker関連プロセスを終了
3. Dockerパッケージをアンインストール
4. Dockerファイルとディレクトリをクリーンアップ
5. Docker関連パッケージをロック
6. APTブロックポリシーを作成
7. 関連するカーネルモジュールを無効化
8. 再インストールを防止する監視スクリプトを作成
9. 監査ルールを作成

## 使用方法

```bash
# sudoまたはrootユーザーで実行する必要があります
sudo ./disable_docker.sh
```

## 注意事項

- このスクリプトはroot権限が必要です
- 操作は不可逆です。重要なデータをバックアップしてください
- 監視スクリプトは10分ごとに実行され、Dockerの再インストールを防止します
- ログは `/var/log/docker-disable.log` と `/var/log/docker-monitor.log` に保存されます

## 作者

SDCOM

## プロジェクトURL

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/disable_docker.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/disable_docker.sh