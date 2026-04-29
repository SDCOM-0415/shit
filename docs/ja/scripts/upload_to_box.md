# upload_to_box.sh

これはファイルをファイルクーリアにアップロードするためのスクリプトです。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

`upload_to_box.sh` はファイルをファイルクーリアにアップロードするためのスクリプトです。ユーザーはコマンドラインからファイルを迅速にアップロードし、受け取りコードとダウンロードURLを取得することができます。

## 特徴

- カスタムサーバーアドレスをサポート
- Tokenはオプションで、必要に応じて入力するかどうかを選択できます
- 実行時にユーザーに設定情報を入力するよう求め、永続的なストレージは必要ありません
- アップロードプロセスを自動的に処理し、アップロードタスクの初期化とファイルコンテンツの正式なアップロードを含みます
- アップロード成功後に受け取りコードとダウンロードURLを表示します

## 使用方法

### スクリプトのダウンロード

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/upload_to_box.sh && sudo chmod +x ./upload_to_box.sh
```

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/upload_to_box.sh && sudo chmod +x ./upload_to_box.sh
```

### スクリプトの実行

```bash
# スクリプトを実行してファイルをアップロード
./upload_to_box.sh <ファイルパス>
```

### 例

```bash
# カレントディレクトリのtest.txtをアップロード
./upload_to_box.sh test.txt

# 指定したパスのファイルをアップロード
./upload_to_box.sh /path/to/file.zip
```

## 注意事項

- サーバーのBase URLが正しいことを確認してください。形式は `https://filebox.example.com` のようにしてください
- Tokenはオプションです。サーバーが認証を要求する場合、有効なTokenを入力する必要があります
- アップロードするファイルのサイズはサーバーの制限に従う必要があります
- アップロードに失敗した場合、スクリプトはサーバーが返したエラー情報を表示します

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/upload_to_box.sh

Github: https://github.com/SDCOM-0415/shit/blob/main/script/upload_to_box.sh

## © 作者

SDCOM