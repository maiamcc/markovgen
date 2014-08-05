from sys import argv

script, source = argv

source_file = open(source)

source_text = source_file.read()

source_file.close()

new_source = source_text.translate(None, "0123456789_")
new_source = new_source.replace("Chapter", "")
new_source = new_source.replace("CHAPTER", "")


source_file = open(source, "w")

source_file.write(new_source)

source_file.close()