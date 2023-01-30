# Translations

All messages displayed to the user will be read from a JSON file named after the locale set in the _--language_ flag:

```bash
python3 resize_images.py --language pt_BR --encoding utf-8
```

## How to add a new language

- Create a _ll_LL.json_ file in the **./language/** directory (_en_GB.json_ for British English, for example).

```bash
.
+-- language/
|   +-- pt_BR.json
|   +-- es_AR.json
|   +-- en_US.json

```

- The JSON file should have the following structure:

```json
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

```json
"final_message": {
                  "singular": "This is the final message",
                  "plural": "This is the final message"
                },
```

## Keys description

- **"date_format"**: Use format code to specify the date format for the log entries. ([Format Codes Reference](https://www.w3schools.com/python/gloss_python_date_format_codes.asp))

```json
"date_format": "%d/%b/%Y %H:%M:%S"
```

- **"enter_data"**: First message displayed to the user. Asks to enter a size in pixels for the new largest dimension.

- **"invalid_data_error"**: In case user enters an invalid input, this message will be displayed. Accepts the variable:

  - _{input_value}_: The invalid input entered by the user.

- **"enter_data_again"**: This message will be displayed after the "invalid_data_error" message, asking again for a new largest dimension size. Can be used to provide examples of valid inputs.

- **"file_not_resized"**: This message will be written to the log file in case the input size is larger than the original image's dimensions. The following variables can be passed to this message:

  - _{file_name}_: Name of the file wich was failed to resize.
  - _{new_largest_dimension}_: The new size specified by the user.
  - _{img_width}_: Original image's width.
  - _{img_height}_: Original image's height.

- **"non_image_error"**: Written to the log file in case there's a non image file in the _./imgs/_ directory. Accepts the variable:

  - _{error}_: The _Image.UnidentifiedImageError_ raised when Image.open() receives a non image file as an argument.

- **"final_message"**: Message displayed at the end of execution. Can be used to inform how many files were actually resized. Accepts the variable:

  - _{total_files_resized}_: Number of resized files.

- **"saved_to"**: This is a complementary final message, informing, for example, where the resized images were saved to. Accepts the variable:

  - _{resized_images_dir}_: Path to the resized images directory.

- **"check_the_log"**: If something was written to the log file, this message will be displayed informing to check the log file for more details. Accepts the variable:

  - _{log_file}_: Name of the log file.
