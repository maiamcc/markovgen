from sys import argv

script, source = argv

source_file = open(source)

source_text = source_file.read()

source_file.close()

header2 = "Lord Of The Rings - Part 2 - The Two Towers By J R R Tolkien"
header3 = "Lord Of The Rings - Part 3 - The Return Of The King By J R R Tolkien"
new_source = source_text.translate(None, "0123456789_")
new_source = new_source.replace("Chapter", "")
new_source = new_source.replace("CHAPTER", "")
new_source = new_source.replace("BOOK", "")
new_source = new_source.replace(header2, "")
new_source = new_source.replace(header3, "")


source_file = open(source, "w")

source_file.write(new_source)

source_file.close()