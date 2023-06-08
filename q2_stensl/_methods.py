from importlib_resources import files as resource
import pathlib
from subprocess import run
from tempfile import TemporaryDirectory

import biom
import pandas as pd

SCRIPT = resource("q2_stensl") / "stensl.R"


def track(
    table: biom.Table,
    metadata: pd.DataFrame,
    em_iterations: int = 1000,
):
    with TemporaryDirectory(dir="boop") as tmpdir:
        tmpdir = pathlib.Path(tmpdir)
        tbl_fp = str(tmpdir / "table.biom")
        md_fp = str(tmpdir / "md.tsv")

        with biom.util.biom_open(tbl_fp, "w") as f:
            table.to_hdf5(f, "save")
        metadata.to_csv(md_fp, sep="\t", index=False)

        out_fp = str(tmpdir / "proportions.tsv")

        args = [
            "Rscript",
            str(SCRIPT),
            tbl_fp,
            md_fp,
            str(em_iterations),
            out_fp
        ]
        run(args)

        props = pd.read_table(out_fp, sep="\t", index_col=0)

    return props
