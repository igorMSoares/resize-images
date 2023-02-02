# Bulk Resize Images

<p align="right">
<img alt="MIT License" src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" />&nbsp;&nbsp;
<img alt="MIT License" src="https://img.shields.io/badge/license-MIT-%23373737?style=flat-square" />&nbsp;&nbsp;
<img alt="MIT License" src="https://img.shields.io/badge/Python 3-FFD43B?style=flat-square&logo=python&logoColor=blue" />&nbsp;&nbsp;
</p>

A command-line application to resize all images in a directory, by getting the new size input from the user. All resized images will be saved to `./imgs/resized/` by default.

I created this as a way to study python and also because I sometimes need to bulk resize large photos taken by camera.

Any suggestions and improvements will be most welcome! :wink:

## Overview

It **maintains the aspect ratio** and **orientation** of the original images, but it only resizes to **smaller** sizes, as it's intended to reduce large photo files and also to avoid quality loss by enlarging images.

The language of all the output messages can be set using the `--language` (or `-l`) flag in the command line. (Default language is `pt_BR`)

```bash
python3 resize_images.py --language en_US
```

For now, **pt_BR**, **es_AR** and **en_US** are already available. New languages can be added by creating a `ll_LL.json` file under the `./language` directory. More information about that in the [./language/README.md](./language/README.md)

## Dependencies

- Pillow (PIL Fork)

```bash
pip install -r requirements.txt

# or just run:
# pip install Pillow
```

## How to use it

- Copy all the image files you want to resize to `./imgs/` and run `resize_images.py` :

```bash
# pt_BR is the default language:
python3 resize_images.py

# in english:
python3 resize_images.py -l en_US

# en castellano:
python3 resize_images.py -l es_AR
```

- To choose another image directory, use the `--images_dir` (or `-d`) flag:

```bash
python3 resize_images.py --images_dir "path/to/images"
```

- User will then be prompted to enter the new intended size, in pixels.

  - Examples of valid input values:
    ```bash
    > 1200px
    ```
    ```bash
    > 1200 px
    ```
    ```bash
    > 1200
    ```

- Note that the user will only enter the size of the **largest dimension**, no matter whether it is _width_ or _height_, as the **aspect ratio is to be preserved**.

- **All the images** in the chosen directory will be resized to the same largest dimension size.

- The resized images will be saved to `./imgs/resized` by default. To choose another destination, use the `--resized_dir` (or `-r`) flag:

```bash
python3 resize_images.py --resized_dir "path/to/resized"
```

- The file `./log.txt` will be used (when necessary) to output extra informations, like:

  - Warning whether any non image file is present in the images directory.

  - Informing that a given image file was not resized due to the new size being larger than the original image dimensions.

## Command-line Arguments

To see all the options run:

```bash
python3 resize_images.py -h
```
