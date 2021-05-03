from setuptools import setup

APP=['bible_ui.py']
DATA_FILES = ['search_verse.py','defaults.txt','convert.py','acronym.txt',\
'ASV.txt','bible_KJV.txt','WEB.txt','NASB.txt',\
'simplified.txt','triditional.txt']
OPTIONS = {'packages': ['pandas']}

setup(
    app = APP,
    data_files = DATA_FILES,
    options = {'py2app':OPTIONS},
    setup_requires=['py2app']
)
