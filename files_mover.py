import os
from enum import Enum

SCRIPT_NAME = "files_mover.py"


class SortingVariables(Enum):
    """
    Enum with sorting variables.
    """
    RANDOM = None
    CREATING_DATE = "ctime"
    MODIFICATION_DATE = "mtime"
    NAME = "name"
    FILE_SIZE = "size"
    FILE_TYPE = "type"

    def __str__(self) -> str:
        return self.value


class FilesSeparator:
    """
    Class for separating files into folders.

    Each folder will contain `num` files, starting
    from `start_folder_num`.

    If number of files is not equally divisible by number of folders,
    last folder will contain fewer files than the others.

    Folders names will be like `folder-1`, `folder-2`, etc.
    (see `start_folder_name` parameter to change it).

    Other folders in work folder will be ignored.

    Methods:

    :meth:`info()`: Returns dictionary with info about
    :class:`FilesSeparator` object.

    :meth:`info_str()`: String representation of
    :class:`FilesSeparator` object.

    :meth:`info_print()`: Print info about
    :class:`FilesSeparator` object.

    :meth:`move()`: Actual process: creates folders and moves files
    into them. Sorting files if it set to do so.

    :param work_folder: path to work folder,
     if None - work folder will be current folder
     (where script is located).

    :param num: number of files to separate for each folder.

    :param start_folder_name: start name of folders names where files
     will be moved (e.g. if set to "folder-", first folder will be
     "folder-1" and so on).

    :param start_folder_num: number of starting folder (e.g. if set
     to 3, first folder will be "folder-3" and so on).

    :param sorting: if None, files will be not sorted and will be
     moved randomly. Sorting variables you can grab
     from :class:`SortingVariables` class.

    :param reverse: if True, files will be sorted in reverse order
     (doesn't work if sorting is None).

    Example:

    >>> separator = FilesSeparator(
    ...     work_folder="/home/user/temp_folder",
    ...     num=50,
    ...     start_folder_name="images--",
    ...     start_folder_num=1,
    ...     sorting=SortingVariables.NAME,
    ...     reverse=True
    ... )
    >>> separator.info_print()  # Print info about files and new folders:
    # current directory: /home/user/temp_folder
    # number of files: 179
    # number of folders to create: 4
    # start folder: images--1
    # end folder: images--4
    >>> separator.move()  # Actual process
    """
    def __init__(
            self,
            work_folder: str | None = None,
            num: int = 50,
            start_folder_name: str = "folder-",
            start_folder_num: int = 1,
            sorting: SortingVariables | str | None = SortingVariables.RANDOM,
            reverse: bool = False
    ):
        if work_folder is not None:
            os.chdir(work_folder)
        self._work_folder = os.getcwd()
        self._files = next(os.walk(self._work_folder))[2]
        if SCRIPT_NAME in self._files:
            self._files.remove(SCRIPT_NAME)
        self._n = num
        self._start_folder_name = start_folder_name
        self._start_folder_num = start_folder_num
        self._max_folder_num = (len(self._files) // self._n +
                                (1 if len(self._files) % self._n else 0))
        self._sorting = str(sorting)
        self._reverse = reverse

    def __str__(self) -> str:
        """
        String representation of
        :class:`FilesSeparator` object.
        Simply returns method :meth:`info_str()`.
        :return: str
        """
        return self.info_str()

    def _sort_files(self) -> None:
        """
        Sort files inplace. If sorting is None or not in
        :class:`SortingVariables`, nothing will happen.
        :return: None
        """
        sorting_vars = {
            "ctime": os.path.getctime,
            "mtime": os.path.getmtime,
            "name": os.path.basename,
            "size": os.path.getsize,
            "type": lambda f: os.path.splitext(f)[1]
        }
        if self._sorting in sorting_vars:
            self._files.sort(key=sorting_vars[self._sorting],
                             reverse=self._reverse)

    def info(self) -> dict:
        """
        Returns dictionary with info about
        :class:`FilesSeparator` object.
        :return: dict
        """
        return {
            "current directory": self._work_folder,
            "number of files": len(self._files),
            "number of folders to create": self._max_folder_num,
            "start folder": f"{self._start_folder_name}"
                            f"{self._start_folder_num}",
            "end folder": f"{self._start_folder_name}"
                          f"{self._max_folder_num +
                             self._start_folder_num - 1}"
        }

    def info_str(self) -> str:
        """
        String representation of
        :class:`FilesSeparator` object.
        Simply returns string representation
        of method :meth:`info()`.
        :return: str
        """
        return "\n".join([f"{k}: {v}" for k, v in self.info().items()])

    def info_print(self):
        """
        Print info about
        :class:`FilesSeparator` object.
        :return: None
        """
        print(self)

    def move(self) -> None:
        """
        Actual process: creates folders and moves files to them.
        Sorting files if it set to do so.
        :return: None
        """
        if not self._files:
            raise ValueError("No files to move!")
        print("Moving files to folders...")
        self._sort_files()
        for i in range(0, self._max_folder_num):
            folder = f"{self._start_folder_name}{i + self._start_folder_num}"
            print("Creating folder " + folder)
            if folder in os.listdir(self._work_folder):
                raise ValueError("Folder already exists!")
            os.mkdir(folder)
            for j in range(i * self._n, (i + 1) * self._n):
                if j < len(self._files):
                    os.rename(self._files[j],
                              f"{folder}/{self._files[j]}")
                else:
                    break
        print("Done!")
