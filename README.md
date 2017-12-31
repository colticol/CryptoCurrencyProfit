# 概要
各通貨の購入額総平均と売却額総平均を算出し、手数料を差し引いて利益を算出します。

# 対応取引所
- Bitflyer
- Zaif
- Bitfinex
- cryptopia

# 使い方
- data/に取引履歴(trade.csv)と送金履歴(withdraw.csv)を配置します。
    - 取引履歴は、購入総平均と売却総平均の計算、および手数料の差し引きに利用されます。
    - 送金履歴は送金手数料の差し引きに利用されます。
    - 送金履歴を利用しない場合、src/total_average.pyのwithdraw.csvの引数を削除してください。
- src/total_average.pyのholdsに保有している通貨を入力してください。
- src/で以下のコマンドを実行してください。
`
python3 total_average.py
`

# 環境
- python3 (https://www.python.org/downloads/)
- pandas (https://pandas.pydata.org/)

