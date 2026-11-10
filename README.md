# Agent Working Framework（AWF）

AIエージェントが許可範囲内で自律的に働き、人間が目的・権限・根拠・現在地を把握するための、軽量な作業フレームワークです。開発、調査、文書作成、運用で同じCoreを使います。

本リポジトリは **AWF-SPEC-001 / 0.1.0-draft** の参照実装です。Markdownを読める環境だけで利用できます。独自ランタイム、専用CLI、必須のGit・TDD・状態管理サービスはありません。

## すぐに使う

1. [Coreの5契約](core/contract.md)と[ライフサイクル](core/lifecycle.md)を対象環境から参照できるようにします。
2. 依頼文や既存Issueに、目的・成果・完了条件・許可範囲を示します。不明点は仮定または未確定と記します。
3. [入口テンプレート](templates/AGENTS.md)を使って接続します。Codexの場合は[導入手順](adapters/codex/README.md)に従います。
4. 必要な[Practice](practices/README.md)だけを選びます。選択なしでもCoreは使えます。
5. 小さな作業は会話で結果と根拠を報告します。長時間作業や引き継ぎには[状態テンプレート](templates/task-status.md)を必要に応じて使います。

依頼の例：

> トークンが期限と同時刻でも有効になる不具合を修正してください。完了条件は期限の前・同時・後の検証成功です。ローカルの編集とテストを許可します。本番変更は対象外です。実装方法は任せます。

テンプレート全欄の記入や、同じ情報の別ファイルへの転記は不要です。人間が必要な情報を確認できれば、Issue、会話、文書などを状態の正本にできます。

## 構成

| 場所 | 内容 |
| --- | --- |
| [SPEC.md](SPEC.md) | 適合条件を含む仕様の正本 |
| [core/](core/contract.md) | 5契約と共通ループ |
| [practices/](practices/README.md) | security、evidence、tdd、pre-commit、context-management |
| [adapters/codex/](adapters/codex/README.md) | AGENTS.mdによる接続、手動運用と未対応機能 |
| [templates/](templates/README.md) | 導入用入口と状態表示 |
| [開発例](examples/software-development/README.md) | 失敗の再現、修正、再検証、承認境界 |
| [調査例](examples/research/README.md) | 一次資料の比較、事実と提案の区別、未検証点 |
| [検証記録](docs/conformance.md) | 要件対応表、6シナリオの評価、検証の限界 |
| [運用方針](docs/maintenance.md) | 仕様の未決事項への実装判断、更新・互換性 |

提供された[原仕様書](agent-working-framework-spec.md)は入力資料として保持します。初版の `SPEC.md` は原文と同一です。今後の仕様変更は `SPEC.md` を正本とし、変更理由と互換性への影響を残します。

## この実装の検証

リポジトリルートで、Python 3.9以上の標準ライブラリだけを使って実行できます。これはAWFの利用者に必須のツールではありません。

```sh
python3 scripts/verify.py
python3 -m unittest discover -s examples/software-development -p 'test_*.py' -v
python3 -m unittest discover -s tests -v
python3 scripts/check_secrets.py
```

最初のコマンドは配布物・リンク・導入配置・状態の整合性を検査します。2番目は開発例の実動作を検証します。6つの振る舞いは[シナリオ記録](docs/scenarios.md)で入出力と判断をレビューします。静的チェックだけでエージェントの遵守や実行環境の安全性を保証するものではありません。

3番目はコマンド注入・パス逸脱等の回帰テスト、4番目は公開対象の限定的な秘密情報パターン検査です。検査値は表示しません。[セキュリティレビュー](docs/security-review.md)に対策・検証範囲・残る制約を記載しています。

## 責任と境界

AIは実行・検証・報告・問題提起、人間は目的・許容リスク・権限・必要な承認・最終受容を担います。許可済みの範囲内では実行方法をAIが選択します。Markdownは実行権限を制御しないため、利用環境の権限・サンドボックス・Secrets管理を組み合わせます。

ライセンス：[MIT](LICENSE)。
