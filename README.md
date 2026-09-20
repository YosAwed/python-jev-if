# Python の if 文で Jev を使う

TypeSafe の Jev を使い、自然言語の質問に対する判定で分岐する小さな部品です。
Python の構文を変更するマクロではなく、通常の `if` に渡せる関数として実装しています。

```python
from jev_if import jev

message = "余分に払った分を返してください。"

if jev("顧客は返金を求めていますか？", state={"message": message}, threshold=0.8):
    print("返金希望")
else:
    print("判定基準未満")
```

`jev_if.py` を自分のプログラムと同じフォルダに置くと利用できます。
質問は「はい／いいえ」で答えられる形にし、判断に必要なデータを `state` に渡します。
`state` は辞書・リスト・文字列など、JSON にできる値を指定してください。

## セットアップ（Windows PowerShell、Python 3.10 以上）

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:TYPESAFE_API_KEY = "自分のAPIキー"
& .\.venv\Scripts\python.exe example.py
```

API キーは [TypeSafe Console](https://console.typesafe.ai) で取得します。
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
