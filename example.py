"""Run after setting the TYPESAFE_API_KEY environment variable."""

from jev_if import jev

SAMPLE_MESSAGES = (
    "同じ商品が二重に請求されています。余分に払った分を返してください。",
    "届いた商品に傷がありました。交換をお願いできますか？",
    "注文した商品はいつ発送されますか？",
    "商品の使い方が分からないので、説明書を送ってください。",
)


def main() -> None:
    # 0〜3を変更すると、別のサンプルを試せます。
    message = SAMPLE_MESSAGES[0]

    if jev(
        "顧客は返金を求めていますか？",
        state={"message": message},
        threshold=0.8,
    ):
        print("返金希望として振り分けます。")
    else:
        print("返金希望の判定基準に達しませんでした。")


if __name__ == "__main__":
    main()
