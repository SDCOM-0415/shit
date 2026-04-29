# linux_limit.sh

これはLinuxディレクトリのサイズを制限するためのスクリプトです。`Debian 12`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

- 対話モードとコマンドライン引数の両方をサポート
- fallocateメソッドを使用して固定サイズのイメージファイルを作成
- 元のディレクトリデータを自動的にバックアップ
- 複数のサイズ単位をサポート（B/KB/MB/GB/TB）

## 使用方法

### 対話モード

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh
```

スクリプトを実行した後、プロンプトに従って入力してください：
1. 制限する元のディレクトリパス
2. 制限サイズ（B/KB/MB/GB/TBなどの単位をサポート）
3. イメージ保存パス（デフォルト: ./limit.img）

### コマンドラインモード

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh <元のディレクトリ> <サイズ> <イメージパス>
```
Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh <元のディレクトリ> <サイズ> <イメージパス>
```

例:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/linux_limit.sh && sudo chmod +x ./linux_limit.sh && sudo ./linux_limit.sh /path/to/directory 10GB /path/to/limit.img
```

## 注意事項

- root権限が必要です（mount操作が含まれるため）
- 元のデータは自動的にバックアップされます。バックアップディレクトリ名の形式: `元のディレクトリ名_backup_タイムスタンプ`
- イメージファイルを保存するのに十分なスペースがシステムにあることを確認してください
- 操作前に重要なデータをバックアップすることをお勧めします

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/linux_limit.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/linux_limit.sh

## © 作者

SDCOM