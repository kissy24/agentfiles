# 失敗時の状態例

修正前コードに対する実行結果を使った、過去時点の表示例。現在の正本は [task-status.md](task-status.md)。

- objective: 期限の前・同時・後で正しく期限切れを判定する
- status: working
- current_focus: 同時刻のテスト失敗の原因を調べる
- decisions: 完了にしない。期限と等しい場合だけ誤るため、比較境界を調べる
- evidence: [修正前コード](before/expiry.py)と[検証ログ](../../docs/verification.txt)のRED。3件中test_at_expiryが失敗
- remaining: 同時刻の判定修正、修正後の3条件の再検証
- next_action: 比較境界を修正して同じ3テストを再実行する
- updated_at: 2026-11-10T21:46:20+09:00
