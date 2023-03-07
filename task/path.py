import os
import posixpath


_os_alt_seps = list(
    sep for sep in [os.sep, os.path.altsep] if sep is not None and sep != "/"
)


class PathNotSafe(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f"PathNotSafe: {self.path!r}"


# based on werkzeug.security.safe_join
def safe_join(directory, sub_path):
    """Safely join untrusted path to a base
    directory to avoid escaping the base directory.
    """
    if not directory:
        # Ensure we end up with ./path if directory="" is given,
        # otherwise the first untrusted part could become trusted.
        directory = "."

    parts = [directory]

    filename = sub_path
    if filename != "":
        filename = posixpath.normpath(filename)

    if (
        any(sep in filename for sep in _os_alt_seps)
        or os.path.isabs(filename)
        or filename == ".."
        or filename.startswith("../")
    ):
        raise PathNotSafe(sub_path)

    parts.append(filename)

    return posixpath.join(*parts)
