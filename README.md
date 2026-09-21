# Python の if 文で Jev を使う

TypeSafe の Jev を使い、自然言語の質問に対する判定で分岐する小さな部品です。
Python の構文を変更するマクロではなく、通常の `if` に渡せる関数として実装しています。

```python
from jev_if import jev

sample_messages = [
    "同じ商品が二重に請求されています。余分に払った分を返してください。",
    "届いた商品に傷がありました。交換をお願いできますか？",
    "注文した商品はいつ発送されますか？",
    "商品の使い方が分からないので、説明書を送ってください。",
]
message = sample_messages[0]  # 0〜3を変更すると別の例を試せます

if jev("顧客は返金を求めていますか？", state={"message": message}, threshold=0.8):
    print("返金希望")
else:
    print("判定基準未満")
```

`jev_if.py` を自分のプログラムと同じフォルダに置くと利用できます。
質問は「はい／いいえ」で答えられる形にし、判断に必要なデータを `state` に渡します。
`state` は辞書・リスト・文字列など、JSON にできる値を指定してください。

## セットアップ（Windows PowerShell、Python 3.10 以上）

まず [TypeSafe Console](https://console.typesafe.ai/) にログインまたはアカウントを作成し、API キーを発行・コピーしてください。

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:TYPESAFE_API_KEY = "取得したAPIキー"
& .\.venv\Scripts\python.exe example.py
```

`TypeSafeClient` は `TYPESAFE_API_KEY` 環境変数から API キーを読み込みます。上の `$env:` での設定は現在の PowerShell セッションだけに有効なので、PowerShell を開き直した場合は再設定してください。

次回以降も使えるように Windows ユーザー環境変数として保存する場合は、次のコマンドを使います。設定後は新しい PowerShell を開いてください。

```powershell
[Environment]::SetEnvironmentVariable(
    "TYPESAFE_API_KEY",
    "取得したAPIキー",
    "User"
)
```

API キー本体はソースコード、README、`.env`、Git にコミットしないでください。サンプルの実行には API キーが必要ですが、テストはモックを使用するため API キーなしで実行できます。
このフォルダでは `.venv` と依存パッケージを準備済みです。

## 判定の仕組み

- Jev の Noul が返す「はい」の確率（0〜1）を、`threshold` と比較します。
- `確率 >= threshold` なら `True`。省略時のしきい値は `0.5` です。
- たとえば `threshold=0.8` の場合、`0.8` は `True`、`0.79` は `False` です。
- `False` は基準未満という意味で、確実に「いいえ」と分かったとは限りません。しきい値は実例で調整してください。
- 通信・認証などのエラーは例外になります。判定結果の `False` と区別できます。
- 呼ぶたびに外部 API へ質問と `state` を送信するため、通信時間と API 利用料が発生します。
- 標準モデルは `jev-latest`。`model=` で変更できます。

確率を見て、曖昧な場合を別の分岐にしたいときは次のように書けます。

```python
from jev_if import jev_probability

p = jev_probability("顧客は返金を求めていますか？", state={"message": message})
if p >= 0.8:
    print("返金希望")
elif p <= 0.2:
    print("返金希望ではない")
else:
    print("要確認")
```

数値の大小比較や一致判定など、Python で正確に決められる条件は通常の `if` が適しています。
この関数は文章の意味などを判定する用途に使います。

## ローカル検証

```powershell
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

テストは API 応答を模擬し、しきい値の境界、引数の受け渡し、エラーの扱いを検証します。
実際の Jev の回答品質や API 接続は、キーを設定して別途確認してください。

参照: [公式 Python SDK](https://docs.typesafe.ai/sdk/python)、[Noul の仕様](https://docs.typesafe.ai/primitives/noul)。
