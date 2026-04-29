---
layout: home

hero:
  name: Shell Scripts Collection
  text: 便利なShellスクリプトコレクション
  tagline: 実際には私が書いた💩のコレクションですが、少しは実用的です
  actions:
    - theme: brand
      text: スクリプトドキュメントを表示
      link: /ja/scripts/
    - theme: alt
      text: CNB
      link: https://cnb.cool/SDCOM/shit
    - theme: alt
      text: GitHub
      link: https://github.com/SDCOM-0415/shit
---

# Shell Scripts Collection

これは私が書いた💩のコレクションですが、少しは実用的です。

## Webビルドステータス
[![Netlify Status](https://api.netlify.com/api/v1/badges/237be5bf-d8e3-4c5f-afcc-ff571562bc52/deploy-status)](https://app.netlify.com/projects/shit-sdcom/deploys)

## プロジェクト紹介

このプロジェクトは **VitePress** で構築された静的ドキュメントサイトです。さまざまな便利なShellスクリプトを展示および管理するために設計されています。サイトは多言語切り替え（中国語、英語、日本語）をサポートし、明確なドキュメント構造と使いやすいユーザーインターフェースを提供します。

### 技術的特徴

- **レスポンシブデザイン**: デスクトップおよびモバイルデバイスに完全に適応
- **多言語サポート**: 中国語、英語、日本語に対応
- **コードハイライト**: Shellスクリプトの構文ハイライト表示
- **言語切り替え**: 言語を切り替えるときに現在のページ位置を保持
- **サイトマップ**: searchエンジンインデックス作成のためにsitemap.xmlを自動生成

### ドキュメント構造

サイトは明確なディレクトリ構造を使用しています：

```
docs/
├── index.md                    # ホームページ
├── scripts/                    # スクリプトドキュメント
│   ├── index.md                # スクリプト概要
│   └── *.md                    # 各スクリプトの詳細ドキュメント
├── en/                         # 英語ドキュメント
│   ├── index.md
│   └── scripts/
└── ja/                         # 日本語ドキュメント
    ├── index.md
    └── scripts/
```

### アクセス方法

このサイトは複数のアドレスでアクセス可能です：

- **メインドメイン**: https://shit.sdcom.top/
- **セカンダリドメイン**: https://shit.sdcom.asia/
- **Netlify**: https://shit-sdcom.netlify.app/

## 使用方法

### ドキュメントの閲覧

1. 上部のナビゲーションバーを使用してホームページとスクリプトドキュメントを切り替え
2. 左側のサイドバーを使用して特定のスクリプトのドキュメントに素早く移動
3. 上部の言語セレクターを使用して表示言語を切り替え
4. ドキュメント内のコードブロックをクリックしてスクリプトの完全な内容を表示

### スクリプトの取得

各スクリプトドキュメントページには、CNBおよびGitHubからスクリプトを取得する方法が記載されています：

```bash
# CNBから取得
wget https://cnb.cool/SDCOM/shit/-/git/raw/main/script/script_name.sh

# GitHubから取得
wget https://github.com/SDCOM-0415/shit/raw/refs/heads/main/script/script_name.sh
```

## 主なスクリプト

- **kill_app.sh**: Linuxシステムプログラムを迅速に終了するスクリプト
- **linux_limit.sh**: ディレクトリサイズ制限関連のスクリプト（対話モードと非対話モードあり）
- **get_ip.sh**: termuxでローカルIPアドレスを取得するスクリプト
- **uninstall_docker.sh**: Dockerアンインストールスクリプト
- **disable_docker.sh**: Dockerを完全に無効化して再インストールを防止
- **enable_docker.sh**: Dockerを再び有効化
- **fix_env.sh**: 環境変数をシェル設定ファイルに永続的に固定
- **upload_to_box.sh**: ファイルをファイルクーリアにアップロードするスクリプト
- **port_forward.sh**: IPsec VPNポート転送管理ツール

## プロジェクトリポジトリ

- **CNB**: https://cnb.cool/SDCOM/shit/
- **GitHub**: https://github.com/SDCOM-0415/shit/

## © 作者

SDCOM