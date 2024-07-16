Module with 2 classes: `FilesSeparator` and `SortingVariables` for separating files into folders.

Each folder will contain `num` files, starting from `start_folder_num`.

If number of files is not equally divisible by number of folders, last folder will contain fewer files than the others.

Folders names will be like `folder-1`, `folder-2`, etc. (see `start_folder_name` parameter to change it).

Other folders in work folder will be ignored.



Parameters:

`work_folder`: path to work folder, if None - work folder will be current folder (where script is located).

`num`: number of files to separate for each folder.

`start_folder_name`: start name of folders names where files will be moved (e.g. if set to "folder-", first folder will be "folder-1" and so on).

`start_folder_num`: number of starting folder (e.g. if set to 3, first folder will be "folder-3" and so on).

`sorting`: if None - files will be not sorted and will be moved randomly. Sorting variables you can grab from `SortingVariables` class.

`reverse`: if True - files will be sorted in reverse order (doesn't work if `sorting` is None).

Example:
```python
from files_mover import FilesSeparator, SortingVariables

separator = FilesSeparator(
    work_folder="/home/user/temp_folder",
    num=50,
    start_folder_name="images--",
    start_folder_num=1,
    sorting=SortingVariables.NAME,
    reverse=True
)
print(separator.info())  # Print info about files and new folders:
# current directory: /home/user/temp_folder
# number of files: 179
# number of folders to create: 4
# start folder: images--1
# end folder: images--4

separator.move()  # Actual process
```
