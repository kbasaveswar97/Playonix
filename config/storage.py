"""Custom static files storage backends."""

from whitenoise.storage import CompressedManifestStaticFilesStorage


class NonStrictManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """WhiteNoise compressed-manifest storage that fails gracefully.

    With manifest_strict = False, a {% static %} reference to a file that
    isn't in the manifest (e.g. a typo or a not-yet-added asset) falls back
    to the given name instead of raising ValueError and 500-ing the whole
    site. The asset may 404 individually, but pages still render.
    """

    manifest_strict = False
