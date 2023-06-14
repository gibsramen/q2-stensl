from importlib_resources import files as resource
import pathlib
from subprocess import run
from tempfile import TemporaryDirectory

import biom
import pandas as pd
from qiime2 import Metadata

SCRIPT = resource("q2_stensl") / "stensl.R"


def track(
    table: biom.Table,
    metadata: Metadata,
    em_iterations: int = 1000,
    lambda_vals: list = None
) -> pd.DataFrame:
    lambda_vals = lambda_vals or [0.01, 1, 10, 100]
    metadata = metadata.to_dataframe()
    return _track(table, metadata, em_iterations, lambda_vals)


def _track(
    table: biom.Table,
    metadata: pd.DataFrame,
    em_iterations: int,
    lambda_vals: list
):
    with TemporaryDirectory() as tmpdir:
        tmpdir = pathlib.Path(tmpdir)
        tbl_fp = str(tmpdir / "table.biom")
        md_fp = str(tmpdir / "md.tsv")

        with biom.util.biom_open(tbl_fp, "w") as f:
            table.to_hdf5(f, "save")
        metadata.to_csv(md_fp, sep="\t", index=True)

        out_fp = str(tmpdir / "proportions.tsv")

        args = [
            "Rscript",
            str(SCRIPT),
            tbl_fp,
            md_fp,
            str(em_iterations),
            ",".join(map(str, lambda_vals)),
            out_fp
        ]
        run(args)

        props = pd.read_table(out_fp, sep="\t", index_col=0)
        props.index.name = "sampleid"

    return props
