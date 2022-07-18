# Translations

All messages displayed to the user will be read from a JSON file named after the locale set in the *'language'* variable

```
language = 'pt_BR'
encoding = 'utf-8'
```
## How to add a new language

- Create a *ll_LL.json* file in the **./language/** directory (*en_GB.json* for British English, for example)

```
.
+-- language/
|   +-- pt_BR.json
|   +-- es_AR.json
|   +-- en_US.json

```

- The JSON file should have the following structure:

```
{
  "date_format": "",

  "enter_data": "",

  "invalid_data_error": "",

  "enter_data_again": "",

  "file_not_resized": "",

  "non_image_error": "",

  "final_message": {
                    "singular": "",
                    "plural": ""
                  },

  "saved_to": {
                "singular": "",
                "plural": ""
              },

  "check_the_log": ""
}

```

- You'll only edit the **""** with the message in the chosen language, and the **name of the keys can't be changed**

- **No key should be removed from the structure**, if you don't want to use it, just assign an empty string (**""**) to it

- If there's no difference between singular and plural forms, enter the same message for both keys:

```
"final_message": {
                  "singular": "This is the final message",
                  "plural": "This is the final message"
                },
```

## Keys description

- **"date_format"**: Use format code to specify the date format for the log entries. ([Format Codes Reference](https://www.w3schools.com/python/gloss_python_date_format_codes.asp))

```
"date_format": "%d/%b/%Y %H:%M:%S"
```

- **"enter_data"**: First message displayed to the user. Asks to enter a size in pixels for the new largest dimension.

- **"invalid_data_error"**: In case user enters an invalid input, this message will be displayed.

- **"enter_data_again"**: This message will be displayed after the "invalid_data_error" message, asking again for a new largest dimension size. Can be used to provide examples of valid inputs.

- **"file_not_resized"**: This message will be written to the log file in case the input size is larger than the original image's dimensions. The following variables can be passed to this message:

  - *{file_name}*: Name of the file wich was failed to resize.
  - *{new_largest_dimension}*: The new size specified by the user.
  - *{img_width}*: Original image's width.
  - *{img_height}*: Original image's height.


- **"non_image_error"**: Written to the log file in case there's a non image file in the *./imgs/* directory. Accepts the variable:

  - *{error}*: The *Image.UnidentifiedImageError* raised when Image.open() receives a non image file as an argument.


- **"final_message"**: Message displayed at the end of execution. Can be used to inform how many files were actually resized. Accepts the variable:

  - *{total_files_resized}*: Number of resized files.


- **"saved_to"**: This is a complementary final message, informing, for example, where the resized images were saved to. Accepts the variable:

  - *{resized_images_dir}*: Path to the resized images directory.


- **"check_the_log"**: If something was written to the log file, this message will be displayed informing to check the log file for more details. Accepts the variable:

  - *{log_file}*: Name of the log file.
