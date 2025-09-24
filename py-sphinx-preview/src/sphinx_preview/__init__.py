"""Fast HTML preview of Sphinx projects"""

from io import StringIO
import os
from sphinx.application import Sphinx
from strip_ansi import strip_ansi

__version__ = "0.1.0"


class SphinxPreview:
    """Thin wrapper around Sphinx. API is a bit cumbersome (non-pythonic) but it's because it's designed to be easily used in Pyodide without too much type translating"""

    def __init__(self, srcdir: str, confdir: str, outdir: str) -> None:
        self.status = StringIO()
        self.warnings = StringIO()
        doctreedir = os.path.join(outdir, ".doctrees")

        app = Sphinx(
            srcdir=str(srcdir),
            confdir=str(confdir),
            outdir=str(outdir),
            doctreedir=str(doctreedir),
            buildername="html",
            status=self.status,
            warning=self.warnings,
        )
        self.app = app

    def build(self) -> dict[str, str]:
        self.app.build()
        return {
            "status": strip_ansi(self.status.getvalue()),
            "warnings": strip_ansi(self.warnings.getvalue()),
        }
