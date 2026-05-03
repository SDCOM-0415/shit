# download_cbz_interactive.py

これは cloudme.one から漫画のチャプターをダウンロードし、CBZファイルにまとめるPythonスクリプトです。Windows / macOS / Linux に対応しています。現在のバージョン <Badge type="tip" text="v1.0" />。

## 機能

`download_cbz_interactive.py` は cloudme.one の漫画チャプターダウンロードツールです。APIを通じて漫画情報を取得し、チャプターの画像をダウンロードして、各種コミックリーダーで使用できるCBZ形式に自動的にパッケージ化します。

## 特徴

- インタラクティブにダウンロードするチャプター範囲を選択
- APIを通じて漫画・チャプター情報を自動取得
- img.cloudme.oneプロキシ経由で高画質画像をダウンロード（cf_clearanceが必要）
- CDN直結フォールバックダウンロード（Cookie不要、ただし画質は低い）
- CBZファイルに自動パッケージ化（ZIP形式、コミックリーダー対応）
- コマンドラインでダウンロードディレクトリを指定可能
- 不足している依存関係を自動検出・インストール
- クロスプラットフォーム対応（Windows / macOS / Linux）
- ターミナルUnicode自動対応（未対応端末ではASCII記号にフォールバック）
- ダウンロード進捗バー表示
- 既存のCBZファイルを自動スキップ

## 依存関係

- Python 3.6+
- curl_cffi

```bash
pip install curl_cffi
```

スクリプトの初回実行時に依存関係を自動検出し、不足している場合はインストールを案内します。

## 使用方法

### スクリプトのダウンロード

CNB:
```bash
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/download_cbz_interactive.py
```

Github:
```bash
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/download_cbz_interactive.py
```

### インタラクティブモード

スクリプトを直接実行するとインタラクティブモードになります：

```bash
python download_cbz_interactive.py
```

### ダウンロードディレクトリの指定

コマンドライン引数でCBZファイルの保存ディレクトリを指定できます：

```bash
# Windows
python download_cbz_interactive.py -o D:\Comics

# macOS / Linux
python download_cbz_interactive.py -o ~/Comics

# 長いオプションも使用可能
python download_cbz_interactive.py --output ./comics
```

デフォルトのダウンロードディレクトリはスクリプトがあるディレクトリです。

## コマンドライン引数

| パラメータ | 短縮 | 説明 |
|-----------|------|------|
| `--output` | `-o` | CBZファイルの保存ディレクトリを指定（デフォルト: スクリプトディレクトリ） |

## 実行フロー

1. **ダウンロードディレクトリの確認**: 現在のダウンロードディレクトリを表示し、新しいパスを入力して変更するかEnterで確認
2. **漫画IDの入力**: cloudme.oneサイトの漫画IDを入力（URL内の数字、例：`cloudme.one/refs/10` の `10`）
3. **漫画情報の取得**: APIを通じて漫画タイトルと全チャプターリストを自動取得
4. **プレフィックス処理（オプション）**: チャプタータイトルに `_` 区切り文字が含まれている場合、プレフィックスを削除するかどうかを確認
5. **Cloudflare Cookieの設定（オプション）**: `cf_clearance` Cookieを提供すると高画質画像をダウンロード可能。スキップするとCDN直結で低画質画像をダウンロード
6. **チャプターの選択**: ダウンロードするチャプター範囲を入力。以下の形式に対応：
   - 単一チャプター: `101`
   - 範囲: `101-120`
   - 複数: `101,103,105`
   - 混合: `101-105,108,110-112`
   - 全部: `all`
7. **確認とダウンロード**: 情報を確認してダウンロード開始。進捗と結果サマリーを表示

## cf_clearanceの取得方法

高画質画像はCloudflare保護されたプロキシ経由でダウンロードするため、`cf_clearance` Cookieが必要です：

1. ブラウザで `cloudme.one` を開く
2. `F12` を押して開発者ツールを開く
3. `Application` タブに切り替える
4. 左側で `Cookies` → `https://cloudme.one` を見つける
5. `cf_clearance` フィールドを見つけてその値をコピーする

::: tip
`cf_clearance` を提供しなくてもスクリプトは動作しますが、CDN直結で低画質画像をダウンロードすることになります。
:::

## 注意事項

- Python 3.6以上が必要です
- `curl_cffi` はCloudflare保護をバイパスするためのコア依存関係です
- 大量のチャプターをダウンロードする際、スクリプトはチャプター間に自動的に間隔を追加し、リクエスト過多を防ぎます
- 既存のCBZファイルは自動的にスキップされ、再ダウンロードされません
- Windowsユーザーでターミナルの文字化けが発生する場合、スクリプトがUTF-8サポートを自動的に有効にします

## プロジェクトリポジトリ

CNB: https://cnb.cool/SDCOM/shit/-/blob/main/script/download_cbz_interactive.py

Github: https://github.com/SDCOM-0415/shit/blob/main/script/download_cbz_interactive.py

## © 作者

SDCOM
