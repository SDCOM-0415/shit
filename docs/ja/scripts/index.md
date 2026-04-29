# スクリプトドキュメント

ここにはすべてのスクリプトの詳細なドキュメントが含まれています。目的、使用方法、例が記載されています。

## 使用可能なスクリプト

- [kill_app.sh](./kill_app.md) - Linuxシステムプログラムを迅速に終了するスクリプト
- [linux_limit.sh](./linux_limit.md) - ディレクトリサイズ制限関連のスクリプト
- [get_ip.sh](./get_ip.md) - termuxでローカルIPアドレスを取得するスクリプト
- [uninstall_docker.sh](./uninstall_docker.md) - Dockerアンインストールスクリプト
- [disable_docker.sh](./disable_docker.md) - Dockerを完全に無効化して再インストールを防止
- [enable_docker.sh](./enable_docker.md) - Dockerを再び有効化
- [fix_env.sh](./fix_env.md) - 環境変数をシェル設定ファイルに永続的に固定
- [upload_to_box.sh](./upload_to_box.sh) - ファイルをファイルクーリアにアップロードするスクリプト
- [port_forward.sh](./port_forward.md) - IPsec VPNポート転送管理ツール

## これらのスクリプトの使い方

ほとんどのスクリプトは次の方法で実行できます：

```bash
# CNB
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/script_name.sh && sudo chmod +x ./script_name.sh && sudo ./script_name.sh

# Github
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/script_name.sh && sudo chmod +x ./script_name.sh && sudo ./script_name.sh
```

特定の使用方法とパラメータについては、各スクリプトの詳細なドキュメントを参照してください。

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/

Github: https://github.com/SDCOM-0415/shit/

## © 作者

SDCOM