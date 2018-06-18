from setuptools import setup
setup(
        name='getcomic',
        description='A command line tool to download comics from readcomiconline.to',
        url='https://github.com/VinitraMk/getcomic-cli',
        author='VinitraMk',
        author_email='vinitramk@gmail.com',
        packages=[
            'getcomic'
        ],
        version="1.0.1",
        entry_points={
            'console_scripts':[
                'getcomic=getcomic.getcomic:main',
            ],
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Operating System :: POSIX',
            'Programming Language :: Python',
        ],
    )
