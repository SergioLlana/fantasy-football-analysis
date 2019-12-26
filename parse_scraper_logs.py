from utils import parse_parser_args, read
import pandas as pd
import ast


def _parse_purchase(purchases_str):
    values = []
    for purchase in purchases_str:
        if purchase:
            value_str = purchase.split("€")[1]
            values.append(int(value_str.replace(",", "")))
        else:
            values.append(0)
    return values


def _parse_value(value_str):
    return int(value_str[1:].replace(",", ""))


def parse(args):
    log = read("data/{0}.log".format(args["log_type"]))
    df = pd.DataFrame([ast.literal_eval(row) for row in log.split("\n")
                       if row and row[0] == "{"])

    if args["log_type"] == "market":
        df = df.drop_duplicates(subset='name', keep="last")
        df["value"] = df.value.str.replace(',', '').astype(int)
    elif args["log_type"] == "transfers":
        df["value"] = df.money.apply(lambda x: x.replace(",", "")[1:]).astype(int)
    elif args["log_type"] == "players":
        df = df.drop_duplicates(subset='name', keep="last")
    else:
        df["purchase_info"] = df.purchase_info.apply(_parse_purchase)
        df["increments"] = df.increments.apply(_parse_purchase)
        df["team_value"] = df.value.apply(_parse_value)

    df.to_csv("data/{0}.csv".format(args["output_file"]))


if __name__ == "__main__":
    args = parse_parser_args()
    parse(args)
