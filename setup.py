from setuptools import setup
setup(
        name='getcomic',
        packages=[
            'getcomic',
        ],
        version="1.0.1",
        entry_points={
            'console_scripts':[
                'getcomic=getcomic.getcomic:main',
            ],
        },
    )
