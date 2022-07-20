#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
from setuptools import find_packages, setup
from ttwlsave import __version__

def readme():
    with open('README.md') as f:
        return f.read()

app_name = 'ttwl-cli-saveedit'

setup(
        name=app_name,
        version=__version__,
        packages=find_packages(),
        license='zlib/libpng',
        description='Tiny Tina\'s Wonderlands Savegame Editor',
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://github.com/abramhindle/ttwl-cli-saveedit',
        author='CJ Kucera, Abram Hindle',
        author_email='cj@apocalyptech.com, web@softwareprocess.es',
        data_files=[
            # I always like these to be installed along with the apps
            (f'share/{app_name}', ['COPYING.txt', 'README.md', 'README-saves.md', 'README-profile.md']),
            # Seems helpful to bundle the Protobuf definitions (via Gibbed) in here
            (f'share/{app_name}/protobufs', [os.path.join('protobufs', f) for f in sorted(os.listdir('protobufs'))]),
            # Seems less helpful to package my mod testing gear, but whatever.
            (f'share/{app_name}/item_exports', ['mod_testing_gear.txt']),
            ],
        package_data={
            'ttwlsave': [
                'resources/inventoryserialdb.json.gz',
                'resources/balance_name_mapping.json.gz',
                'resources/balance_to_inv_key.json.gz',
                ],
            },
        install_requires=[
            'protobuf ~= 3.0, >= 3.12',
            ],
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: zlib/libpng License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Games/Entertainment :: First Person Shooters',
            'Topic :: Utilities',
            ],
        entry_points={
            'console_scripts': [

                # Savegame-related scripts
                'ttwl-save-edit = ttwlsave.cli_edit:main',
                'ttwl-save-info = ttwlsave.cli_info:main',
                'ttwl-save-import-protobuf = ttwlsave.cli_import_protobuf:main',
                'ttwl-save-import-json = ttwlsave.cli_import_json:main',
                'ttwl-process-archive-saves = ttwlsave.cli_archive:main',

                # Profile-related scripts
                'ttwl-profile-edit = ttwlsave.cli_prof_edit:main',
                'ttwl-profile-info = ttwlsave.cli_prof_info:main',
                'ttwl-profile-import-protobuf = ttwlsave.cli_prof_import_protobuf:main',
                'ttwl-profile-import-json = ttwlsave.cli_prof_import_json:main',
                ],
            },
        )
