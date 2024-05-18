#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import os
import pandas as pd
import tempfile
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    with wandb.init(job_type="basic_cleaning") as run:
        run.config.update(args)

        logger.info("Downloading data set {args.input_artifact}")
        artifact_local_path = run.use_artifact(args.input_artifact).file()
        df = pd.read_csv(
            artifact_local_path,
            index_col="id",
            parse_dates=["last_review"]
        ).convert_dtypes()

        logger.info("Cleaning data set")
        df_cleaned = df[df.price.between(args.min_price, args.max_price)].copy()
        with tempfile.TemporaryDirectory() as tmp_dir:
            clean_path = os.path.join(tmp_dir, args.output_artifact)
            df_cleaned.to_csv(clean_path)

            logger.info("Uploading data set {args.output_artifact} to Wandb")
            artifact = wandb.Artifact(
                args.output_artifact,
                type=args.output_type,
                description=args.output_description,
            )
            artifact.add_file(clean_path)
            run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the data set to download",
        required=True,
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the cleaned data set",
        required=True,
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the cleaned data set. This will be used to categorize the artifact in the W&B",
        required=True,
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="A brief description of the output artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price below which rows are considered outliers and dropped out",
        required=True,
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price above which rows are considered outliers and dropped out",
        required=True,
    )


    args = parser.parse_args()

    go(args)
