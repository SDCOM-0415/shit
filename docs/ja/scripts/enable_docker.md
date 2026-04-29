# enable_docker.sh

これはDockerを再び有効化するためのスクリプトです。`Debian 12` `Ubuntu 22.04`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

`disable_docker.sh`によって設定されたすべての制限を解除し、Dockerをインストールします。

## 使用方法

```bash
# sudoまたはrootユーザーで実行する必要があります
sudo ./enable_docker.sh
```

## 注意事項

- このスクリプトはroot権限が必要です
- 以前のバックアップファイル（`/root/docker-backup-*`内）は手動で復元する必要がある場合があります
- ログは `/var/log/docker-enable.log` に保存されます

## 作者

SDCOM

## プロジェクトURL

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/enable_docker.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/enable_docker.sh