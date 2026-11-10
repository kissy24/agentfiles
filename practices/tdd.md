# Test-Driven Development

- id: tdd
- name: Test-Driven Development
- version: 0.1.0
- core_compatibility: AWF-SPEC-001 / 0.1.0-draft
- purpose: 振る舞いの変更を段階的に検証する
- applies_to: software-development
- preconditions: 対象コードに実行可能なテスト環境がある
- overrides: system-policy、runtime-controls、awf-core、domain-policy、repository-policy

## Rules

1. 振る舞いを示す失敗するテストを先に作り、想定した理由で失敗することを確認するのを推奨する。既存テストが適切なら再利用する。
2. 目的の振る舞いを満たす変更を行い、関連テストを実行する。テスト自体の誤りや環境不足を、製品の不具合再現と混同しない。
3. 必要ならリファクタリングし、影響範囲を再検証する。実装の内部をそのまま写すテストは避ける。
4. 失敗は完了にせず、原因を調べる。同じ失敗で進展がなければ方針変更・中断・相談する。
5. テスト環境がなければ制約と代替検証を示す。このPracticeのためだけに無関係な業務へテスト環境を強制しない。

## Verification

対象の振る舞い、修正前後の結果、再現コマンドを参照できるようにする。テスト成功だけで未実施の統合・本番検証まで成功としない。

負担と評価：変更する振る舞いと影響範囲に絞り、再発防止の有効性と実行コストを評価する。
