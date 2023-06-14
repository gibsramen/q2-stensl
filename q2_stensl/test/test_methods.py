from importlib_resources import files as resource

import biom
import numpy as np
import pandas as pd

from qiime2.plugins import stensl
import q2_stensl._methods as methods
from qiime2 import Artifact, Metadata


def test_stensl():
    tbl_file = resource("q2_stensl") / "test/test_data/otu_example_stensl.biom"
    md_file = resource("q2_stensl") / "test/test_data/metadata_example_stensl.tsv"

    tbl = biom.load_table(tbl_file)
    md = pd.read_table(md_file, sep="\t")
    md.index = md.SampleID

    props = methods._track(tbl, md, em_iterations=5, lambda_vals=[0.01, 0.1])
    exp_dim = (1, 51)
    assert props.shape == exp_dim

    src_sum = props.sum(axis=1).item()
    np.testing.assert_almost_equal(src_sum, 1.0)


def test_q2_stensl():
    tbl_file = resource("q2_stensl") / "test/test_data/otu_example_stensl.qza"
    md_file = resource("q2_stensl") / "test/test_data/metadata_example_stensl.tsv"

    tbl = Artifact.load(tbl_file)
    md = Metadata.load(md_file)

    props, = stensl.methods.track(tbl, md, em_iterations=5,
                                  lambda_vals=[0.01, 0.1])
    props = props.view(pd.DataFrame)
    exp_dim = (1, 51)
    assert props.shape == exp_dim

    src_sum = props.sum(axis=1).item()
    np.testing.assert_almost_equal(src_sum, 1.0)
