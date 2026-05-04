# download_cbz_interactive.py

これは cloudme.one から漫画のチャプターをダウンロードし、CBZファイルにまとめるPythonスクリプトです。Windows / macOS / Linux に対応しています。現在のバージョン <Badge type="tip" text="v1.1" />。

## 機能

`download_cbz_interactive.py` は cloudme.one の漫画チャプターダウンロードツールです。APIを通じて漫画情報を取得し、チャプターの画像をダウンロードして、各種コミックリーダーで使用できるCBZ形式に自動的にパッケージ化します。

## 特徴

- インタラクティブまたはコマンドラインでダウンロードするチャプター範囲を選択
- APIを通じて漫画・チャプター情報を自動取得
- img.cloudme.oneプロキシ経由で高画質画像をダウンロード（cf_clearanceが必要）
- CDN直結フォールバックダウンロード（Cookie不要、ただし画質は低い）
- マルチスレッド画像ダウンロード、マルチタスク並列チャプターダウンロード
- CBZファイルに自動パッケージ化（ZIP形式、コミックリーダー対応）
- HTTP/SOCKS5プロキシ対応
- 画像ダウンロードスレッド数（1-32）と並列チャプター数（1-5）を設定可能
- コマンドラインで cf_clearance を渡して、インタラクティブ入力が不要
- 確認をスキップして直接ダウンロード開始（`-y`/`--yes`）
- 不足している依存関係を自動検出・インストール
- クロスプラットフォーム対応（Windows / macOS / Linux）
- ターミナルUnicode自動対応（未対応端末ではASCII記号にフォールバック）
- ダウンロード進捗バー表示
- 既存のCBZファイルを自動スキップ

## 依存関係

| 依存関係 | 用途 | インストール |
|---------|------|-------------|
| Python 3.6+ | 実行環境 | — |
| [curl_cffi](https://pypi.org/project/curl-cffi) | Cloudflare保護をバイパスして画像をダウンロード | `pip install curl_cffi` |

> スクリプトの初回実行時に依存関係を自動検出し、不足している場合はインストールを案内します。

## 使用方法

### スクリプトのダウンロード

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/download_cbz_interactive.py
```

GitHub:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/download_cbz_interactive.py
```

### インタラクティブモード

スクリプトを直接実行するとインタラクティブモードになります：

```bash
python download_cbz_interactive.py
```

### 非インタラクティブモード

コマンドライン引数ですべての必要情報を提供すると、スクリプトは対話入力をスキップして直接ダウンロードを開始します：

```bash
# 101-120話をダウンロード、プロキシ使用、16スレッド、3チャプター並列
python download_cbz_interactive.py \
  -o ~/Comics \
  -m 10 \
  -c 101-120 \
  --cf xxxxxxxx \
  -p http://127.0.0.1:7890 \
  -t 16 \
  -j 3 \
  --strip-prefix \
  -y
```

> `-m`、`-c`、`-o` がすべて提供されると、スクリプトは自動的に非インタラクティブモードに入ります。
> 提供されていない引数はインタラクティブモードで入力を求められます。

### ダウンロードディレクトリの指定

コマンドライン引数でCBZファイルの保存ディレクトリを指定できます：

```bash
# Windows
python download_cbz_interactive.py -o D:\Comics

# macOS / Linux
python download_cbz_interactive.py -o ~/Comics

# 他の引数と組み合わせ可能
python download_cbz_interactive.py -o ~/Comics -m 10 -c all -y
```

デフォルトのダウンロードディレクトリはスクリプトがあるディレクトリです。

## コマンドライン引数

| パラメータ | 短縮 | 説明 |
|-----------|------|------|
| `--output DIR` | `-o` | CBZファイルの保存ディレクトリを指定（デフォルト: スクリプトディレクトリ） |
| `--mid ID` | `-m` | 漫画ID（例: cloudme.one/refs/10 の `10`） |
| `--chapters RANGE` | `-c` | チャプター範囲、`101-120`、`101,103,105`、`all` に対応 |
| `--cf TOKEN` | | cf_clearance cookie 値（高画質画像ダウンロード用） |
| `--proxy URL` | `-p` | HTTP/SOCKS5プロキシアドレス（例: `http://127.0.0.1:7890`） |
| `--threads N` | `-t` | 画像ダウンロードスレッド数（1-32、デフォルト 8） |
| `--jobs N` | `-j` | 並列ダウンロードチャプター数（1-5、デフォルト 5） |
| `--strip-prefix` | | タイトル中の `_` 前のプレフィックスを削除（例: `SomeManga_Chapter101` → `Chapter101`） |
| `--yes` | `-y` | 確認プロンプトをスキップして直接ダウンロード開始 |

## 実行フロー

### インタラクティブモードの流れ

1. **ダウンロードディレクトリの確認**: 現在のダウンロードディレクトリを表示し、新しいパスを入力して変更するかEnterで確認
2. **（オプション）プロキシ設定**: HTTP/SOCKS5プロキシアドレスを入力、またはEnterでスキップ
3. **（オプション）スレッド数設定**: 画像ダウンロードスレッド数（1-32）を設定、Enterでデフォルト8を使用
4. **（オプション）並列タスク数設定**: 同時ダウンロードするチャプター数（1-5）を設定、Enterでデフォルト5を使用
5. **漫画IDの入力**: cloudme.oneサイトの漫画IDを入力（URL内の数字、例: `cloudme.one/refs/10` の `10`）
6. **漫画情報の取得**: APIを通じて漫画タイトルと全チャプターリストを自動取得
7. **プレフィックス処理（オプション）**: チャプタータイトルに `_` 区切り文字が含まれている場合、プレフィックスを削除するかどうかを確認
8. **Cloudflare Cookieの設定（オプション）**: `cf_clearance` Cookieを提供すると高画質画像をダウンロード可能。スキップするとCDN直結で低画質画像をダウンロード
9. **チャプターの選択**: ダウンロードするチャプター範囲を入力。以下の形式に対応：
   - 単一チャプター: `101`
   - 範囲: `101-120`
   - 複数: `101,103,105`
   - 混合: `101-105,108,110-112`
   - 全部: `all`
10. **確認とダウンロード**: 情報を確認してダウンロード開始。進捗と結果サマリーを表示

### 非インタラクティブモード

`-o`、`-m`、`-c` がすべて提供されると、スクリプトはすべてのインタラクティブプロンプトをスキップして直接ダウンロードを開始します。その他の引数（`-p`、`-t`、`-j`、`--cf`、`--strip-prefix`、`-y`）は必要に応じて指定できます。

## cf_clearanceの取得方法

高画質画像はCloudflare保護されたプロキシ経由でダウンロードするため、`cf_clearance` Cookieが必要です：

1. ブラウザで `cloudme.one` を開く
2. `F12` を押して開発者ツールを開く
3. `Application` タブに切り替える
4. 左側で `Cookies` → `https://cloudme.one` を見つける
5. `cf_clearance` フィールドを見つけてその値をコピーする

::: tip
`cf_clearance` を提供しなくてもスクリプトは動作しますが、CDN直結で低画質画像をダウンロードすることになります。
コマンドライン引数 `--cf` で直接渡すこともできます。インタラクティブモードで手動で貼り付ける必要はありません。
:::

## 注意事項

- Python 3.6以上が必要です
- `curl_cffi` はCloudflare保護をバイパスするためのコア依存関係です
- 大量のチャプターをダウンロードする際、スクリプトはチャプター間に自動的に間隔を追加し、リクエスト過多を防ぎます
- 既存のCBZファイルは自動的にスキップされ、再ダウンロードされません
- Windowsユーザーでターミナルの文字化けが発生する場合、スクリプトがUTF-8サポートを自動的に有効にします
- 画像ダウンロードスレッド数（`-t`）は32以下、並列チャプター数（`-j`）は5以下にすることをお勧めします。レート制限を回避するためです

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/download_cbz_interactive.py

GitHub: https://github.com/SDCOM-0415/shit/blob/main/script/download_cbz_interactive.py

## © 作者

SDCOM
