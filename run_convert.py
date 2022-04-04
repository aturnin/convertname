import os
import sys
import pathlib
import modul_conv as mc


def clear_fname(fname):
    """
    Cleans from a line not suitable symbols
    """
    fname = fname.replace(':', '')
    fname = fname.replace('"', '')
    fname = fname.replace('?', '')
    fname = fname.replace('*', '')
    fname = fname.replace('\n', '')
    return fname


def convert_name(dirname):
    """
    Finds e-book files in the specified directory and subdirectories.
    Renames files to names in the "author-title" format from the metadata of the book.
    """

    num_rename = 0      # number of renamed files
    num_norename = 0    # number of files not renamed
    num_noextension = 0  # how many non-target files
    num_error = 0       # number of errors

    # files_indir = os.listdir(dirname)
    files_indir = os.walk(dirname)

    for root, dirs, files in files_indir:
        for file1 in files:

            old_pfile = os.path.join(root, file1)
            if os.path.isfile(old_pfile):
                file_extension = pathlib.Path(file1).suffix
                new_fname = mc.STR_ERROR

                if file_extension == '.epub':
                    new_fname = mc.conv_epub(old_pfile)
                elif file_extension == '.fb2':
                    new_fname = mc.conv_fb2(old_pfile)
                else:
                    num_noextension = num_noextension + 1
                    continue

                new_fname = clear_fname(new_fname)
                if not new_fname == mc.STR_ERROR:
                    new_pfname = os.path.join(root, new_fname + file_extension)
                    if os.path.isfile(old_pfile) and not (old_pfile == new_pfname):
                        num_tryname = 0
                        while os.path.isfile(new_pfname):
                            num_tryname = num_tryname + 1
                            new_fname1 = new_fname + \
                                '(' + str(num_tryname) + ')'
                            new_pfname = os.path.join(
                                root, new_fname1 + file_extension)
                        try:
                            os.rename(old_pfile, new_pfname)
                            num_rename = num_rename + 1
                        except:
                            num_error = num_error + 1
                            print('It is not possible to change the file name: ' +
                                  old_pfile + ' to ' + new_pfname)

                    # if there is no file or the name does not change
                    else:
                        num_norename = num_norename + 1

                else:
                    num_error = num_error + 1
                    print('Error: Not getting a name for the file:  ', old_pfile)
            else:
                print('Error: Directory, can t be.')

    return num_rename, num_norename, num_noextension, num_error


# e:\projects\winpython\sony_reader3

if __name__ == '__main__':

    if len(sys.argv) > 1:
        dirname = sys.argv[1]
    else:
        dirname = os.curdir

    print('Specified directory: {}'.format(dirname))
    num_rename, num_norename, num_noextension, num_error = convert_name(
        dirname)
    print('Number of: renamed files={}, files not renamed={}, non-target files={}, errors={}'
          .format(num_rename, num_norename, num_noextension, num_error))
