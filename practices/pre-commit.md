# Pre-commit

- id: pre-commit
- name: Early Change Checks
- version: 0.1.0
- core_compatibility: AWF-SPEC-001 / 0.1.0-draft
- purpose: 変更の基本的な問題を早期に検出する
- applies_to: Gitを使うソフトウェア・文書開発
- preconditions: Gitと対象プロジェクトの検査コマンドが利用できる
- overrides: system-policy、runtime-controls、awf-core、domain-policy、repository-policy

## Rules

1. 既存のフォーマット・Lint・型・秘密情報検査等から、今回の変更に適したものを選ぶ。特定のhook管理製品は必須ではない。
2. 既存hookがあればその設定と副作用を確認する。hook導入や設定変更は作業の許可範囲で行う。
3. コミット前に関連チェックと差分を確認する。実行できない検査は理由を示す。失敗を隠すための無断スキップはしない。
4. 自動修正後は差分を再確認する。無関係な変更を巻き込まず、許可されていないコミット・push・マージは行わない。

## Verification

実行コマンド、結果、差分レビューの対象を記録または参照する。hookの成功を全受入条件の達成とはみなさない。

負担と評価：既存チェックを再利用し、検出した問題と待ち時間を見て検査を調整する。
