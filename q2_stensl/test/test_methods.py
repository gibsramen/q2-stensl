from importlib_resources import files as resource

import biom
import numpy as np
import pandas as pd

import q2_stensl._methods as methods


def test_stensl():
    tbl_file = resource("q2_stensl") / "test/test_data/otu_example_stensl.biom"
    md_file = resource("q2_stensl") / "test/test_data/metadata_example_stensl.txt"

    tbl = biom.load_table(tbl_file)
    md = pd.read_table(md_file, sep="\t")
    md.index = md.SampleID

    props = methods.track(tbl, md, em_iterations=5)
    exp_dim = (1, 51)
    assert props.shape == exp_dim

    src_sum = props.sum(axis=1).item()
    np.testing.assert_almost_equal(src_sum, 1.0)
