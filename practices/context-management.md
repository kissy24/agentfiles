# Context Management

- id: context-management
- name: Context Management
- version: 0.1.0
- core_compatibility: AWF-SPEC-001 / 0.1.0-draft
- purpose: 長時間作業で目的や根拠を失わず、不要な文脈を減らす
- applies_to: 長時間作業、中断・引き継ぎ、複数資料を使う作業
- preconditions: 人間と次の担当者が参照できる状態の置き場所がある
- overrides: system-policy、runtime-controls、awf-core、domain-policy、repository-policy

## Rules

1. 入口は短く保ち、Coreと現在の作業に関係するPractice・資料だけを読む。
2. 状態の正本を1つ決め、重要判断・根拠・未解決事項・次の行動を節目で更新する。重複する状態は参照に置き換える。
3. 中断・引き継ぎ時は目的、成果物の場所、最終検証、残課題、許可範囲、再開条件を圧縮して残す。内部推論全文は残さない。
4. 再開時にファイル・実行結果・権限を再確認する。古いサマリーと現状が違えば現状を検証して状態を修正する。
5. タスクに応じ時間・試行・費用の上限を設定する。進展がなければ方針を変えるか相談・中断する。トークン消費量そのものを最大化しない。

## Verification

状態だけから目的・判断・根拠・残課題・次の一手を説明できるか確認する。参照先が利用可能か確認し、実測なしに費用削減を断定しない。

負担と評価：重要な節目に絞り、再開に必要な時間と読み込む資料の量を振り返る。
