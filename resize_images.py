import sys

from modules import Arguments
from modules import Messages
from modules import ResizerLogger
from modules import ImageResizer

def main():
    Arguments.get_arguments()
    Arguments.validate()

    ResizerLogger.init(Arguments.args['log_file'])

    Messages.set_language(Arguments.args['language'])

    images_dir = Arguments.args['images_dir']
    resized_dir = Arguments.args['resized_dir']

    if Arguments.args['size']:
        new_dimension = int(Arguments.args['size'].strip('px'))
    else:
        new_dimension = ImageResizer.get_largest_dimension(
                        Messages.output('enter_data'),
                        Messages.output('invalid_data_error'),
                        Messages.output('enter_data_again'))
    ImageResizer.resize_all(images_dir, resized_dir, new_dimension)

    total = ImageResizer.total_files_resized
    if total == 1:
        final_message = Messages.output("final_message", "singular")
        final_message += Messages.output("saved_to", "singular")
    else:
        final_message = Messages.output("final_message", "plural")
        if total > 1:
            final_message += Messages.output("saved_to", "plural")

    print(final_message.format(
        total_files_resized=total,
        resized_images_dir=Arguments.args["resized_dir"]
    ))

    if ResizerLogger.log_has_something:
        print(Messages.output("check_the_log").format(log_file=Arguments.args["log_file"]))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
