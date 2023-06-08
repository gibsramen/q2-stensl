from qiime2.plugin import Plugin, Int, Str, Metadata
from q2_types.feature_table import FeatureTable, Frequency, RelativeFrequency

from ._methods import track
from . import __version__

plugin = Plugin(
    name="stensl",
    version=__version__,
    website="https://github.com/gibsramen/q2-stensl",
    short_description=("Plugin for STENSL source-tracking"),
    description=(
        "QIIME2 plugin for using the STENSL microbial source tracking"
        "tool"
    ),
    package="q2_stensl"
)

PARAMS = {
    "metadata": Metadata,
    "em_iterations": Int
}

PARAMS_DESC = {
    "metadata": "Sample metadata in FEAST format",
    "em_iterations": "Max expectation-maximization iterations"
}


plugin.methods.register_function(
    function=track,
    inputs={"table": FeatureTable[Frequency]},
    input_descriptions={
        "table": "Feature table with sources and sinks"
    },
    parameters=PARAMS,
    parameter_descriptions=PARAMS_DESC,
    outputs=[
        ("proportions", FeatureTable[Frequency])
    ],
    output_descriptions={
        "proportions": "Contributions from sources"
    },
    name="Microbial source-tracking",
    description=(
        "Microbial source-tracking using STENSL"
    )
)
