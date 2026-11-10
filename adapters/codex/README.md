# Codex Adapter

AWF 0.1.0-draft / Adapter 0.1.0。プロジェクトの `AGENTS.md` を入口に、同一のCore文書を読み込ませる構成です。Coreの再定義、グローバル設定の変更、Hooksや独自ランタイムは不要です。

## 配置

```text
target-project/
├── AGENTS.md
└── .awf/
    ├── core/
    │   ├── contract.md
    │   └── lifecycle.md
    └── practices/             # 選択したものだけ。なくてもよい
```

初回はこのAWFリポジトリを開き、対象プロジェクトへ `core/` を `.awf/core/` としてコピーし、[入口](../../templates/AGENTS.md)をルートへ配置します。Core内の相互リンクはコピー後も解決します。対象に `AGENTS.md` がある場合は上書きせず、AWF入口の節を統合して既存ルールと整合させます。

新規導入用の例です。AWFリポジトリルートから実行し、`awf_target` を実在する導入先に変更します。既存のAWFまたは入口があれば停止します。

```sh
awf_target='/absolute/path/to/target-project'
(
  set -euC
  awf_source=$(pwd -P)
  test -d "$awf_target"
  test ! -L core
  test ! -L templates
  for awf_file in core/contract.md core/lifecycle.md templates/AGENTS.md; do
    test -f "$awf_file"
    test ! -L "$awf_file"
  done
  cd "$awf_target"
  for awf_entry in .awf AGENTS.md AGENTS.override.md; do
    if test -e "$awf_entry" || test -L "$awf_entry"; then
      echo "Existing entry; merge manually: $awf_entry" >&2
      exit 1
    fi
  done
  mkdir .awf
  mkdir .awf/core
  cat "$awf_source/core/contract.md" > .awf/core/contract.md
  cat "$awf_source/core/lifecycle.md" > .awf/core/lifecycle.md
  cat "$awf_source/templates/AGENTS.md" > AGENTS.md
)
```

更新は自動上書きせず、現在の版と新版の差分を確認して適用します。Coreの版は各文書に記載されています。

導入元・導入先は信頼できる、自分が管理するディレクトリを使ってください。コピー元のシンボリックリンクを拒否し、`noclobber` により書込時にも既存ファイルの上書きを拒否します。第三者が同時にディレクトリを差し替えられる環境に対する防御や、失敗時の自動ロールバックは提供しません。途中で失敗した場合は作成済みファイルを確認し、既存データと区別してから手動で復旧します。

Practiceを使う場合だけ `.awf/practices/` を作り、例えば `practices/evidence.md` をコピーします。入口の「選択なし」を「選択：evidence。`.awf/practices/evidence.md` を必要時に読む」に置き換えます。ファイルをコピーしただけでは選択扱いにしません。調査ではTDDやGitを追加する必要はありません。

状態ファイルが必要なら[テンプレート](../../templates/task-status.md)を任意の場所へコピーし、入口に場所を示します。作業依頼には完了条件・許可範囲を示し、承認が必要なら担当者と判断対象も明確にします。

## 接続の確認

対象プロジェクトで新しいCodexセッションを開き、次を依頼します。

> 有効な指示ファイルとAWF Coreを読んで、目的・許可範囲・完了条件・状態の置き場所を簡潔に示してください。設定やファイルは変更しないでください。

入口と2つのCoreが参照され、選択したPracticeだけが対象となることを確認します。リンク先は自動展開を仮定せず、入口で読むよう明示しています。

公式資料では、プロジェクトルートから作業ディレクトリまでの指示を読み、各階層では `AGENTS.override.md` が `AGENTS.md` より優先されます。適用範囲・上書き・サイズ制限によって入口が効かない場合があるため、新しいセッションで有効な指示を確認してください。[OpenAI公式：Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)（確認日：2026-11-10）。

## 対応範囲

| 契約・機能 | 提供方法 | 制約 |
| --- | --- | --- |
| Intent | 入口からCoreと依頼を参照 | 目的・完了条件は人間またはエージェントが整理 |
| Boundary | Coreと環境の許可範囲を確認 | 文書による指示。権限制御・承認UIは利用環境の責務 |
| Evidence | 作業に合う検証と根拠の参照 | テスト自動実行・出典自動判定は未提供 |
| Visibility | 会話・Issue・状態ファイル | 手動またはエージェント更新。リアルタイム同期は未提供 |
| Accountability | 人間とAIの責任を明記 | 承認者の本人確認や受容の自動判定は未提供 |
| ライフサイクル | 指示として4機能と停止・再開条件を提供 | ループ制御・イベント監視は未提供 |

本Adapterは文書による接続を提供します。モデルが常に指示に従うことを保証せず、技術的制御の試験は対象環境で行います。新しい外部操作の承認は、その操作・対象・影響に対する有効な許可と実行環境制御で判断します。

検証の範囲：[適合性記録](../../docs/conformance.md)。他製品向けの自動接続は本版では未提供ですが、同じCoreをその製品の入口から参照できます。
