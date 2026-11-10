# AWF repository

[Core契約](core/contract.md)と[ライフサイクル](core/lifecycle.md)を適用する。
このリポジトリの目的は、[仕様](SPEC.md)に基づく軽量で業務非依存のAWFを提供すること。

- Coreへ特定のツール・業務手順を追加しない。Practicesは任意、製品固有事項はAdaptersに置く。
- 変更に関係する文書だけ読み、検証は `python3 scripts/verify.py`。開発例のコード変更時はREADME記載の単体テストも実行する。
- 仕様入力 `agent-working-framework-spec.md` を保持する。仕様の正本は `SPEC.md`。
- 実施していない検証やランタイム制御を対応済みと記載しない。
- 本構築作業の状態は[docs/task-status.md](docs/task-status.md)。以後の独立した作業は会話・Issue等で状態の場所を決める。
