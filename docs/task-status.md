# AWF構築の状態

- objective: AWF-SPEC-001に基づき、共通Core・Practices・Adapter・テンプレート・適用例を構築する
- status: completed
- current_focus: 参照実装の構築と仕様に対する受入検証を完了
- decisions: Markdownによる参照実装を採用。最小導入は入口とCoreの3ファイル。5Practiceは選択制で、状態は手動またはエージェントが更新する
- evidence: [要件対応と受入評価](conformance.md)、[6シナリオ](scenarios.md)、[実行ログ](verification.txt)。原仕様との一致、導入配置と既存入口保全、リンク・状態項目、開発例の失敗再現と修正後3件成功、調査レポートの出典照合を確認
- remaining: 本仕様の参照実装として残課題なし。独立したCodexセッションの実運用試験・他製品Adapter・自動同期・運用効果測定は未実施／未提供であり、対応範囲に含めない
- next_action: READMEの導入手順から利用可能。対象環境へ導入する際はAdapter記載の接続確認を行う
- updated_at: 2026-11-10T21:46:20+09:00
