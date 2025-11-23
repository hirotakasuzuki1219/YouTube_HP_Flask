# Git Push トラブルシューティング

## エラー: `Could not resolve host: github.com`

このエラーは、ネットワーク接続の問題を示しています。

## 解決方法

### 方法1: ネットワーク接続の確認

1. **インターネット接続を確認**
   - ブラウザでGitHubにアクセスできるか確認
   - 他のWebサイトにアクセスできるか確認

2. **DNS設定の確認**
   - DNSサーバーが正しく設定されているか確認
   - 一時的にGoogle DNS（8.8.8.8）を使用

### 方法2: プロキシ設定の確認

会社や学校のネットワークを使用している場合、プロキシ設定が必要な場合があります。

```bash
# プロキシ設定を確認
git config --global --get http.proxy
git config --global --get https.proxy

# プロキシを設定する場合（例）
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# プロキシを無効にする場合
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 方法3: SSH接続に変更（推奨）

HTTPSの代わりにSSH接続を使用：

```bash
# 現在のリモートURLを確認
git remote -v

# SSH接続に変更
git remote set-url origin git@github.com:hirotakasuzuki1219/YouTube_HP_Flask.git

# 確認
git remote -v
```

**注意**: SSH接続を使用するには、SSHキーを設定する必要があります。

### 方法4: 一時的な解決策

1. **VPNを使用**（利用可能な場合）
2. **別のネットワークに接続**（モバイルホットスポットなど）
3. **時間をおいて再試行**

### 方法5: ブランチ名の確認

現在のブランチが`master`ですが、GitHubのデフォルトブランチが`main`の場合：

```bash
# 現在のブランチを確認
git branch

# mainブランチに切り替え（存在する場合）
git checkout main

# または、masterブランチをmainにリネーム
git branch -m master main
```

## 推奨される手順

### 1. ネットワーク接続を確認

```bash
# GitHubに接続できるか確認
ping github.com

# または
curl -I https://github.com
```

### 2. ブラウザでGitHubにアクセス

- https://github.com にアクセスできるか確認
- ログインできるか確認

### 3. 接続方法を変更

**SSH接続に変更（推奨）:**

```bash
# SSHキーが設定されているか確認
ls ~/.ssh/id_rsa.pub

# SSHキーがない場合、生成
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# GitHubにSSHキーを追加（生成された公開鍵をコピー）
cat ~/.ssh/id_rsa.pub

# リモートURLをSSHに変更
git remote set-url origin git@github.com:hirotakasuzuki1219/YouTube_HP_Flask.git
```

**または、HTTPS接続を再試行:**

```bash
# キャッシュをクリア
git config --global --unset http.proxy
git config --global --unset https.proxy

# 再試行
git push origin master
```

## 一時的な解決策

ネットワークの問題が解決しない場合：

1. **別のネットワークに接続**（モバイルホットスポットなど）
2. **VPNを使用**
3. **時間をおいて再試行**

## 確認事項

- [ ] インターネット接続が正常か
- [ ] ブラウザでGitHubにアクセスできるか
- [ ] プロキシ設定が必要か
- [ ] SSH接続に変更できるか
- [ ] ブランチ名が正しいか（master vs main）

