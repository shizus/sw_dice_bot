
from setuptools import setup, find_packages

setup(
    name="sw_dice_simulator",
    version="1.0.0",
    description="Star Wars: Edge of the Empire Dice Roller",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Babel"],
    entry_points={
        "console_scripts": [
            "sw_dice_simulator=sw_dice_simulator.main:main",
        ],
    },
)
