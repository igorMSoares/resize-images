
# Bulk Resize Images

## Overview

Resizes all images in the *'./imgs'* folder, by getting the new size input from user.

It **maintains the aspect ratio** and **orientation** of the original images, but it only resizes to **smaller** sizes, as it's intended to reduce large photo files and also to avoid quality loss by enlarging images.

The language of all the output messages is set in the *language* variable (TO DO: pass the locale as an argument when running the resize_images.py).

For now, **'pt_BR'**, **'es_AR'** and **'en_US'** are already available. New languages can be added by creating a *ll_LL.json* file under the *./language* directory. More information about that in the [./language/README.md](./language/README.md)

I created this as a way to study python and also because I sometimes need to bulk resize large photos taken by camera.

Any suggestions and improvements will be most welcome! :wink:

## Dependencies

- Pillow (PIL Fork)
```
pip install --upgrade pip
pip install --upgrade Pillow
```

## How to use it

- Copy all the image files you want to resize to *'./imgs'* and run *resizeImgs.py* .

- User will then be prompted to enter the new intended size, in pixels.
  - Examples of valid input values:
    ```
    > 1200px
    ```
    ```
    > 1200 px
    ```
    ```
    > 1200
    ```

- Note that the user will only enter the size of the **largest dimension**, no matter whether it is *width* or *height*, as the **aspect ratio is to be preserved**.

- All the images in the *'./imgs'* folder will be resized to the same largest dimension size.

- The resized images will be saved to *'./imgs/resized'* .


- The file *'./log.txt'* will be used (when necessary) to output extra informations, like:
  - Warning whether any non image file is present in the *'./imgs'* folder.

  - Informing that a given image file was not resized due to the new size being larger than the original image dimensions.
