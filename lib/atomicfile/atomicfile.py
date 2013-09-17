# encoding: utf-8

import errno
import os
import tempfile


umask = os.umask(0)
os.umask(umask)


def copymode(src, dst, mode=None):
    """
    Copy the file mode from the file at path |src| to |dst|.
    If |src| doesn't exist, we're using |mode| instead. If |mode| is None,
    we're using |umask|.
    """
    try:
        st_mode = os.lstat(src).st_mode & 0o777
    except OSError as inst:
        if inst.errno != errno.ENOENT:
            raise
        st_mode = mode
        if st_mode is None:
            st_mode = ~umask
        st_mode &= 0o666
    os.chmod(dst, st_mode)


def mktemp(name, createmode=None):
    """
    Create a temporary file with the similar |name|.
    The permission bits are copied from the original file or |createmode|.

    Returns: the name of the temporary file.
    """
    d, fn = os.path.split(name)
    fd, temp = tempfile.mkstemp(prefix='.%s-' % fn, dir=d)
    os.close(fd)

    # Temporary files are created with mode 0600, which is usually not
    # what we want.  If the original file already exists, just copy
    # its mode.  Otherwise, manually obey umask.
    copymode(name, temp, createmode)
    return temp


class AtomicFile(object):
    """
    Writeable file object that atomically updates a file.

    All writes will go to a temporary file.
    Call close() when you are done writing, and AtomicFile will rename
    the temporary copy to the original name, making the changes visible.
    If the object is destroyed without being closed, all your writes are
    discarded.
    """
    def __init__(self, name, mode="w+b", createmode=None):
        self.__name = name  # permanent name
        self._tempname = mktemp(name, createmode=createmode)
        self._fp = open(self._tempname, mode)

        # delegated methods
        self.write = self._fp.write
        self.fileno = self._fp.fileno

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            return
        self.close()

    def close(self):
        if not self._fp.closed:
            os.fsync(self._fp.fileno())
            self._fp.close()
            os.rename(self._tempname, self.__name)

    def discard(self):
        if not self._fp.closed:
            try:
                os.unlink(self._tempname)
            except OSError:
                pass
            self._fp.close()

    def __del__(self):
        if getattr(self, "_fp", None):  # constructor actually did something
            self.discard()
