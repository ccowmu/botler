import io

# A file that can hold key-value pairs, or just plain values.
class DataFile:
    def __init__(self, filename, overwrite = False, entry_separator = ';', key_value_separator = ':'):
        self.filename = filename
        self.overwrite = overwrite
        self.entry_separator = entry_separator
        self.key_value_separator = key_value_separator
        self.data = {}

        # If the file is not set to overwrite, import all the contents of the file.
        if not overwrite:
            # Open the file to read.
            with open(filename, 'r') as f:
                # Read the file as a string
                string = ""
                for line in f:
                    string += line
                entries = tokenize(string, entry_separator)

                # Add each key-value pair to the dictionary.
                for entry in entries:
                    key_value = split_by(string, key_value_separator)
                    if len(key_value) > 1:
                        self.data[key_value[0]] = key_value[1]
                    # If there wasn't a key value, don't add anything.

    # Writes all current data to the file.
    def write(self):
        with open(self.filename, 'w') as f:
            for key, value in self.data:
                f.write(key)
                f.write(key_value_separator)
                f.write(value)
                f.write(entry_separator)

# Splits a string by a delimiter once. Returns an array of two strings. If the delimiter is not found, returns an array of the original string.
def split_by(string, delimiter):
    delim_location = string.find(delimiter)
    if delim_location >= 0:
        return [string[:delim_location], string[delim_location + 1:]]
    else:
        return [string]

# Splits a string by a character, but ignores it if it is preceded by the escape character.
def tokenize(string, delimiter = ',', escape = '\\'):
    array = []
    buf = ""
    escaping = False
    for c in string:
        if c == delimiter and not escaping:
            array.append(buf)
            print(buf)
            buf = ""
        elif c == escape and not escaping:
            escaping = True
        else:
            buf += c
            escaping = False
    if len(buf) > 0:
        array.append(buf)
    return array