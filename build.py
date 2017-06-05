#! python3
import datetime
import json
from csscompressor import compress

def main():
    # Open config file
    with open("config.json", 'r') as config_file:
        config = json.load(config_file)

    # Incriment the build counter
    config["build"] += 1

    # Print starting script message
    print("\n{} CSS; build #{}\n\nStarting...\n".format(config["name"], config["build"]))

    # Generate the CSS file header comment
    compiled_css = ""
    author_comment = "/*\n\tStylesheet for {}; build #{}\n\tAuthor{}: {}\n\tBuild Date: {}\n*/\n\n".format(
        config["name"], 
        config["build"], 
        "s" if len(config["authors"]) > 1 else "", 
        " & ".join(", ".join(config["authors"]).rsplit(', ', 1)),
        datetime.datetime.utcnow().strftime("%m/%d/%Y @ %H:%M UTC")
    )

    # Print messages for css file
    print("Reading from CSS files:")

    # Open indivual CSS files
    for file in config["files"]:
        # Try opening file
        try:
            with open('{}/'.format(config["css_directory"]) + file, 'r') as css_file:
                # Add css file to final CSS file
                compiled_css += "/* {}\n------------------------------------------------------------------------------ */\n".format(file) + css_file.read() + "\n\n"
                print("\t Succesfully added \"{}/{}\"".format(config["css_directory"], file))


        # Print error if file not found
        except FileNotFoundError:     
            print("\tError reading \"{}/{}\": File not Found".format(config["css_directory"], file))


    # Write css to file
    with open(config["unminified_file"], 'w') as output_file:
        output_file.write(author_comment + compiled_css)
        output_file.close()

    # Write minified css to file
    with open(config["minified_file"], 'w') as output_file:
        output_file.write(author_comment + compress(compiled_css))
        output_file.close()

    # Write config to file
    with open("config.json", 'w') as config_file:
        config_file.write(json.dumps(config, sort_keys=True, indent=4))
        config_file.close()

    # Print confirming CSS file was succesfully generated
    print("\nSuccesfully generated css files!")
    print("\tunminified: {}, minified: {}".format(config["unminified_file"], config["minified_file"]))

# Run Python script
if __name__ == '__main__':
    main()
