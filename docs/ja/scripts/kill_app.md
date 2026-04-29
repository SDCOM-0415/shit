# kill_app.sh
このスクリプトはLinuxおよびmacOSシステムで実行中のプログラムを迅速に終了するために使用されます。`FydeOS Linux Subsystem`、`macOS 10.15.7`、`Debian 12`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />

## 機能

- ユーザーがプロセス名を入力し、そのプロセスを見つけて終了することができます
- 完全一致するプロセスが見つからない場合、関連する可能性のあるプロセスを表示します
- PIDで直接プロセスを終了することをサポートします

## 使用方法
CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/kill_app.sh && sudo chmod +x ./kill_app.sh && sudo ./kill_app.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/kill_app.sh && sudo chmod +x ./kill_app.sh && sudo ./kill_app.sh
```

スクリプトを実行した後、終了するプロセス名を入力してください。完全一致するプロセスが見つからない場合、スクリプトは関連する可能性のあるプロセスをリストし、特定のプロセスを終了するためにPIDを入力することができます。

## 注意事項

- このスクリプトは`kill -9`コマンドを使用してプロセスを強制終了します。これによりデータ損失またはその他の問題が発生する可能性があります
- 重要なプロセスを終了する前に、すべての作業を保存してください
- Linuxシステムでこのスクリプトを使用する場合、一部のシステムプロセスを終了するにはroot権限が必要になる場合があります

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/kill_app.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/kill_app.sh

## © 作者

SDCOM