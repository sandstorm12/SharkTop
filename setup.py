from setuptools import setup


def read_requirements(path='./requirements.txt'):
    with open(path, encoding='utf-8', errors='ignore') as file:
        install_requires = file.readlines()

    return install_requires


setup(
    name="SharkTop",
    version="0.8.4",
    author="Hamid Mohammadi",
    author_email="sandstormeatwo@gmail.com",
    description="Curses-based UI for GstShark",
    scripts=[
        'sharktop'
    ],
    install_requires=read_requirements()
)
