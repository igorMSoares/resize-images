# Bulk Resize Images

<p align="right">
<img alt="MIT License" src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" />&nbsp;&nbsp;
<img alt="MIT License" src="https://img.shields.io/badge/license-MIT-%23373737?style=flat-square" />&nbsp;&nbsp;
<img alt="MIT License" src="https://img.shields.io/badge/Python 3-FFD43B?style=flat-square&logo=python&logoColor=blue" />&nbsp;&nbsp;
<img alt="MIT License" src="https://img.shields.io/badge/-%3E%20Command%20Line%20App-yellow?style=flat-square&color=373737" />
</p>

A command line application to resize all images in a directory, by getting the new size input from the user. All resized images will be saved to _./imgs/resized/_ by default.

I created this as a way to study python and also because I sometimes need to bulk resize large photos taken by camera.

Any suggestions and improvements will be most welcome! :wink:

## Overview

It **maintains the aspect ratio** and **orientation** of the original images, but it only resizes to **smaller** sizes, as it's intended to reduce large photo files and also to avoid quality loss by enlarging images.

The language of all the output messages can be set using the _--language_ (or _-l_) flag in the command line. (Default language is _pt_BR_)

```bash
python3 resize_images.py --language en_US
```

For now, **'pt_BR'**, **'es_AR'** and **'en_US'** are already available. New languages can be added by creating a _ll_LL.json_ file under the _./language_ directory. More information about that in the [./language/README.md](./language/README.md)

## Dependencies

- Pillow (PIL Fork)

```bash
pip install -r requirements.txt

# or just run:
# pip install Pillow
```

## How to use it

- Copy all the image files you want to resize to _./imgs/_ and run _resize_images.py_ :

```bash
# pt_BR is the default language:
python3 resize_images.py

# in english:
python3 resize_images.py -l en_US

# en castellano:
python3 resize_images.py -l es_AR
```

- To choose another image directory, use the _--images_dir_ (or _-d_) flag:

```bash
py resize_images.py --images_dir "path/to/images"
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

- The resized images will be saved to _'./imgs/resized'_ by default. To choose another destination, use the _--resized_dir_ (or _-r_) flag:

```bash
py resize_images.py --resized_dir "path/to/resized"
```

- The file _./log.txt_ will be used (when necessary) to output extra informations, like:

  - Warning whether any non image file is present in the images directory.

  - Informing that a given image file was not resized due to the new size being larger than the original image dimensions.

## Command-line Arguments

To see all the options run:

```bash
python3 resize_images.py -h
```
