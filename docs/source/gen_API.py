import os
from os.path import join, dirname
from operator import itemgetter

def write_docstring(main_path, source_path,
                    fname, fwrite = 'API.rst',
                    main_header = 'API Reference',
                    sub_header = 'Library'):
    """ Writes a Sphinx-markdown-formatted file that generates docstrings for 
    all classes and functions within the ``fname`` Python file.

    Parameters
    ----------
    main_path : str
        The path to the main package directory.
    source_path : str
        The path to the Sphinx source folder containing the .rst files.
    fname : str
        Name of the .py file to generate docstrings for (include extension).
    fwrite : str
        Name of the .rst to write docstrings to (include extension).
    main_header : str
        The top-level header for the markdown file.
    sub_header : str, optional
        Appended to the subheader associated with the ``fname`` (e.g. if 
        ``fname = 'test.py'`` and ``sub_header = 'Library'``, the section
        header for ``test.py`` becomes "Test Library").

    Notes
    -----
    If a file of the name ``fwrite`` is passed into the function, it will be 
    deleted completely and rebuilt. If no file of that name exists, one will 
    be created.

    Classes are placed at the top of the document, with functions following, 
    and both are internally sorted alphabetically. Functions that have leading underscores will be ignored.
    Ex: 
        def _z(*):
            <function contents>
        class Z(*):
            <class contents>
        def f(*):
            <function contents>
        def a(*):
            <function contents>
        class G(*):
            <class contents>
        class B(*):
            <class contents>
        
        will be sorted as B, G, Z, a, f.
    """
    os.chdir(main_path)
    fr = open(fname, 'r')
    flines = fr.readlines()
    fr.close()
    os.chdir(source_path)
    fw = open(fwrite, 'a+')

    # Creating headers
    if os.stat(fwrite).st_size == 0:
        fw.write('#' * len(main_header) + \
                 '\n{0}\n'.format(main_header) + \
                 '#' * len(main_header) + \
                 '\n\n\n')
    if sub_header is not None: sub_header = ' ' + sub_header
    else: sub_header = ''
    fw.write('*' * (len(fname[:-3]) + len(sub_header)) + \
             '\n{0}{1}\n'.format(fname[:-3].capitalize(), sub_header) + \
             '*' * (len(fname[:-3]) + len(sub_header)) + \
             '\n\n')

    # Gathering all functions and classes as tuples of (name, type).
    # Single-letter functions are appended a unique string to prevent them from
    # being incorrectly sorted.
    names = []
    for line in flines:
        if line[0:5] == 'class':
            names.append((line[6:line.find(':')], 'C'))
        if line[0:3] == 'def':
            fname = line[4:line.find('(')]
            if len(fname) == 1: fname = fname.lower() + 'GENAPIFUNC'
            if fname[0] is not '_': names.append((fname, 'F'))
    # Sorting by type first and then alphabetically
    names = sorted(names, key = itemgetter(1,0))

    for name in names:
        # Fixing single-letter function names
        if 'GENAPIFUNC' in name[0]:
            name = (name[0].replace('GENAPIFUNC', ''), 'F')
            name = (name[0].upper(), 'F')

        # Writing to file in Sphinx markdown format
        fw.write(name[0] + '\n')
        fw.write(('=' * len(name[0])) + '\n\n')
        if name[1] is 'C':
            fw.write('.. autoclass:: phidl.geometry.{0}\n'.format(name[0]))
            fw.write('   :members:\n'
                     '   :inherited-members:\n'
                     '   :show-inheritance:\n\n\n')
        else:
            fw.write('.. autofunction:: phidl.geometry.{0}\n\n\n' \
                     .format(name[0]))
    fw.close()

#%%
main_path = join(dirname(dirname(dirname(__file__))), 'phidl')
source_path = dirname(__file__)
fwrite = 'API.rst'
os.chdir(source_path)
try: os.remove(join(source_path, 'API.rst'))
except: pass

write_docstring(main_path = main_path, source_path = source_path,
                fname = 'geometry.py', fwrite = fwrite)