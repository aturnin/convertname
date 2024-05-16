from bs4 import BeautifulSoup as bs
import zipfile

STR_ERROR = 'convert error '
STR_DEFAULT = ''


def conv_epub(fname):
    """
    Defines a name of a file 'epub' from its metadata.
    'fname' it is a way to a name of a file
    """

    try:
        zpf = zipfile.ZipFile(fname)
        zpf_f1 = zpf.read('META-INF/container.xml')
        soup = bs(zpf_f1, features='xml')

        tag = soup.rootfile
        fname_content = tag.attrs['full-path']

        zpf_f2 = zpf.read(fname_content)
        soup = bs(zpf_f2, features='xml')

        book_title = get_target_string(soup, 'dc:title')
        book_creator = get_target_string(soup, 'dc:creator')

        if book_creator == STR_DEFAULT and book_title == STR_DEFAULT:
            out_str = STR_ERROR

        elif book_creator == STR_DEFAULT:
            out_str = book_title

        elif book_title == STR_DEFAULT:
            out_str = book_creator

        else:
            out_str = book_creator + ' - ' + book_title

    except:
        out_str = STR_ERROR
        print('ERROR= ', fname)

    return out_str


def conv_fb2(fname):
    """
    Defines a name of a file 'fb2' from its metadata.
    'fname' it is a way to a name of a file
    """

    try:
        fp = open(fname, 'rb')
        soup = bs(fp, features='xml')
        fp.close()

        book_title = get_target_string(soup, 'book-title')
        book_firstname = get_target_string(soup, 'first-name')
        book_lastname = get_target_string(soup, 'last-name')

        if book_firstname == STR_DEFAULT and book_lastname == STR_DEFAULT and book_title == STR_DEFAULT:
            out_str = STR_ERROR

        elif book_title == STR_DEFAULT and book_lastname != STR_DEFAULT:
            out_str = book_lastname + ' ' + book_firstname

        elif book_lastname == STR_DEFAULT and book_title != STR_DEFAULT and book_firstname != STR_DEFAULT:
            out_str = book_firstname + ' - ' + book_title

        elif book_lastname == STR_DEFAULT and book_title != STR_DEFAULT and book_firstname == STR_DEFAULT:
            out_str = book_title

        elif book_lastname == STR_DEFAULT and book_title == STR_DEFAULT and book_firstname != STR_DEFAULT:
            out_str = book_firstname

        else:
            out_str = book_lastname + ' ' + book_firstname + ' - ' + book_title
    except:
        out_str = STR_ERROR
        print('ERROR= ', fname)

    return out_str


def get_target_string(tag, tag_str):
    """
    Finds value on a label 'tag_str' in metadata 'tag'
    """

    tag1 = tag.find(tag_str)
    if tag1 is None:
        out_str = STR_DEFAULT
    else:
        out_str = tag1.getText()

    return out_str
