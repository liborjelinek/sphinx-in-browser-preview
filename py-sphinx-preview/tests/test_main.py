from pathlib import Path
from dir_content_diff import assert_equal_trees

from sphinx_preview import SphinxPreview

datadir = Path(__file__).parent / "data"
srcdir = datadir / "srcdir"
expected_out_dir = datadir / "expected_outdir"


def test_integration(tmp_path: Path):
    # *** Arrange ***
    outdir = tmp_path

    # *** Act ***
    preview = SphinxPreview(srcdir=srcdir, confdir=srcdir, outdir=outdir)
    console = preview.build()

    # *** Assert ***
    # Output files are the same
    assert_equal_trees(expected_out_dir, outdir)

    # Some status
    assert console["status"]

    # Warnings are not discarded
    assert (
        "index.rst:6: WARNING: image file not readable: missing.png"
        in console["warnings"]
    )
    assert (
        "index.rst:9: WARNING: Literal block expected; none found."
        in console["warnings"]
    )
    assert (
        "orphan.rst.rst: WARNING: document isn't included in any toctree"
        in console["warnings"]
    )
