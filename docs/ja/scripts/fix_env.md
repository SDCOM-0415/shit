# fix_env.sh

これは環境変数をシェル設定ファイルに永続的に固定するためのスクリプトです。`Bash` `Zsh`でテストされています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

環境変数をユーザーのシェル設定ファイルに永続的に固定し、セッション終了後に環境変数が失われるのを防ぎます。.bashrc、.zshrc、または.profileへの自動検出と書き込みをサポートします。

## 使用方法

### スクリプトのダウンロード

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/fix_env.sh && sudo chmod +x ./fix_env.sh
```

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/fix_env.sh && sudo chmod +x ./fix_env.sh
```

### スクリプトの実行

```bash
# スクリプトを実行
./fix_env.sh

# 環境変数名と内容を入力してください
```

## 対話フロー

1. 環境変数名を入力（例: `API_KEY`、`PATH` など）
2. 環境変数の内容を入力（例: `/usr/local/bin` または `abc123`）
3. スクリプトは現在使用しているシェル（bash/zsh）を自動検出
4. 環境変数を対応する設定ファイルに書き込む

## 環境変数名のルール

- 文字、数字、アンダースコアのみを許可
- 数字で始めることはできません
- 最初の文字は文字またはアンダースコアでなければなりません

## サポートされているシェル設定ファイル

- **Bash**: `~/.bashrc`
- **Zsh**: `~/.zshrc`
- **その他**: `~/.profile`

## 設定を有効にする

スクリプト実行後、以下のコマンドを実行して設定を有効にします：

```bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc

# またはターミナルウィンドウを再開
```

## 注意事項

- 環境変数が既に存在する場合、スクリプトはその値を更新します
- 設定ファイルが存在しない場合は自動的に作成されます
- 設定を有効にするには設定ファイルを再読み込みするかターミナルを再起動する必要があります

## 作者

SDCOM

## プロジェクトURL

- CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/fix_env.sh
- GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/fix_env.sh