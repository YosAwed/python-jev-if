"""Run after setting the TYPESAFE_API_KEY environment variable."""

from jev_if import jev


def main() -> None:
    message = "同じ商品が二重に請求されています。余分に払った分を返してください。"

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
