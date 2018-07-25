# 概要
各通貨の購入額総平均と売却額総平均を算出し、手数料を差し引いてJPYで利益を算出します。

# 対応取引所
- Bitflyer
- Zaif
- Bitfinex
- cryptopia

# 使い方
- data/に取引履歴(trade.csv)を配置します。
    - 取引履歴は、購入総平均と売却総平均の計算に利用されます。
- src/total_average.pyの以下の項目を埋めてください。
    - last_holds : 1月1日に保有していた通貨の枚数を入力してください。
    - last_price : 1月1日に保有していた通貨の購入総平均を入力してください。
        - last_hogeは元金および購入総平均の算出に利用されます。
    - jpy_deposit : 今年の日本円の入金額を入力してください。元金に加算されます。
    - jpy_withdrow : 今年のの日本円の出金額を入力してください。利益に加算されます。
    - assets : 現在保有している通貨の枚数を入力してください。利益に加算されます。
- src/で以下のコマンドを実行してください。
`
python3 total_average.py
`

# 環境
- python3 (https://www.python.org/downloads/)
- pandas (https://pandas.pydata.org/)

