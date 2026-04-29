# port_forward.sh

これはLinuxシステム上でiptablesポート転送ルールを管理するためのVPNポート転送管理ツール（Proバージョン）です。`Debian 12` `Ubuntu 22.04`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

- クラウドサーバーのパブリックネットワークインターフェースを自動検出
- TCP、UDPプロトコルおよび全プロトコル転送をサポート
- 単一ポート、複数ポートおよびポート範囲転送をサポート
- スマートポートマッピング（1:1マッピングまたはカスタムターゲットポート）
- VPNサブネットトラフィックループバックを自動的に構成（MASQUERADE）
- 有効な転送ルールを視覚的に表示および削除
- ユーザーフレンドリーなメニューインターフェース

## 使用方法

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/port_forward.sh && sudo chmod +x ./port_forward.sh && sudo ./port_forward.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/port_forward.sh && sudo chmod +x ./port_forward.sh && sudo ./port_forward.sh
```

スクリプトを実行した後、メニューのプロンプトに従って操作してください：
- `1` を選択して新しいポート転送ルールを追加
- `2` を選択して既存の転送ルールを表示および削除
- `3` を選択してスクリプトを終了

## 注意事項

- スクリプトはroot権限が必要です
- 転送ルールはシステムの再起動後に失われます。永続化するにはiptables-saveを使用してください
- NATルールを削除した後も、FORWARDチェインのエントリは残りますが使用に影響はありません
- デフォルトのVPNサブネットは `192.168.42.0/24` です。変更が必要な場合はスクリプト内のサブネット設定を調整してください
- ターゲットVPNクライアントがサーバーに正常にアクセスできることを確認してください

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/port_forward.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/port_forward.sh

## © 作者

SDCOM