import argparse
import json
import pandas as pd

from prometheus.utils.data import create_dataset, create_dataframe, \
    prepare_dataset_labeling, separate_tags


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--in-csv", 
        type=str, default=None)
    parser.add_argument(
        "--in-dirs", 
        type=str, default=None)
    
    parser.add_argument(
        "--out-dataset", 
        type=str, default=None)
    parser.add_argument(
        "--out-labeling", 
        type=str, default=None, required=True)

    parser.add_argument(
        "--tag-column",
        type=str, default=None, required=True)
    parser.add_argument(
        "--tag-delim",
        type=str, default=None)

    args = parser.parse_args()
    return args


def prepare_df_from_dirs(dirs, class_column_name):
    dataset = create_dataset(dirs)
    df = create_dataframe(dataset, columns=[class_column_name, "filepath"])
    return df


def main(args):
    if args.in_csv is not None:
        df = pd.read_csv(args.in_csv)
    elif args.in_dirs is not None:
        df = prepare_df_from_dirs(args.in_dirs, args.class_column)
    else:
        raise Exception
    
    if args.tag_delim is not None:
        df = separate_tags(
            df, 
            tag_column=args.tag_column,
            tag_delim=args.tag_delim)
    
    tag2lbl = prepare_dataset_labeling(df, args.tag_column)
    print("Num classes: ", len(tag2lbl))

    with open(args.out_labeling, "w") as fout:
        json.dump(tag2lbl, fout)

    if args.out_dataset is not None:
        df.to_csv(args.out_dataset, index=False)


if __name__ == "__main__":
    args = parse_args()
    main(args)
