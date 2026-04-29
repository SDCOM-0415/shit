# get_ip.sh

これはtermuxでローカルIPアドレスを迅速に取得するためのスクリプトです。`termux`でテストされています。現在のバージョン <Badge type="tip" text="v0.1" />。

## 機能

- すべてのネットワークインターフェースのIPv4アドレスを取得
- ネットワークインターフェース名と対応するIPアドレスを明確な形式で表示
- ifconfigコマンドが利用可能かどうかを自動的にチェック

## 使用方法

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/get_ip.sh && sudo chmod +x ./get_ip.sh && sudo ./get_ip.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/get_ip.sh && sudo chmod +x ./get_ip.sh && sudo ./get_ip.sh
```

実行後、スクリプトはIPv4アドレスを持つすべてのネットワークインターフェースとそのIPアドレスを表示します。形式: `インターフェース名：IPアドレス`

## 依存関係

- `net-tools`パッケージ（`ifconfig`コマンドを提供）

## 注意事項

- システムに`ifconfig`コマンドがインストールされていない場合、スクリプトは`net-tools`パッケージのインストールを促します
- スクリプトはIPv4アドレスを持つインターフェースのみを表示します。IPアドレスのないインターフェースは表示されません
- このスクリプトは主にtermux環境用に設計されていますが、他のLinuxシステムでも使用できます

## プロジェクトリポジトリ
CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/get_ip.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/get_ip.sh

## © 作者
SDCOM