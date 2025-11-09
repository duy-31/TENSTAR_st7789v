from setuptools import setup, find_packages

setup(
    name="TENSTAR_st7789v",
    version="1.1.0",
    author="Duy-31",
    author_email="bui.duyhuan@free.fr",
    description="Enhanced ST7789V display library for Raspberry Pi with text rendering and animation support",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/duy-31/TENSTAR_st7789v",
    project_urls={
        "Homepage": "https://github.com/duy-31/TENSTAR_st7789v",
        "Issues": "https://github.com/duy-31/TENSTAR_st7789v/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Multimedia :: Graphics",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.13",
    install_requires=[
        "gpiozero",
        "spidev",
        "lgpio",
        "pigpio",
        "RPi.GPIO",
        "numpy",
        "Pillow"
    ],
    include_package_data=True,
)
