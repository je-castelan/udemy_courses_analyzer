import argparse
import logging
import os
import pandas as pd
import hashlib


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_dataframe(folder):
    df = pd.DataFrame([], columns=[
        'category',
        'name',
        'prize',
        'rank',
        'url',
        'origin',
        ])
    for file in os.listdir(folder):
        newdf = pd.read_csv("{}/{}".format(folder, file))
        newdf['origin'] = file

        # UID Generator
        uids = (
            newdf.apply(
                lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1
                )
            .apply(lambda hash_object: hash_object.hexdigest())
        )
        newdf['uid'] = uids
        newdf.set_index('uid', inplace=True)
        df = pd.concat([df, newdf])
    return df


if __name__ == "__main__":
    """
    Main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder",
        help="Give the folder with the files to analyze",
        type=str)
    args = parser.parse_args()
    folder = args.folder
    if not folder:
        logger.error("Folder is not defined. Finishing")
        print("It's mandatory to assign a folder to analyze")
    else:
        if not os.path.exists(folder):
            logger.error("Folder is not valid. Finishing")
            print("It's mandatory to assign a valid folder")
        else:
            df = create_dataframe(folder)
            print(df)
