import io

# Holds a two dimensional array of data to be read or written from a file.
# The file is read in the constructor. If overwrite is set to True, the file is not read.
# The file is written with the write() function. Use the write() function when finished with the file.
class DataFile:
    def __init__(self, filename, overwrite = False, line_delimiter = ';', column_delimiter = ','):
        self.filename = filename
        self.overwrite = overwrite
        self.line_delimiter = line_delimiter
        self.column_delimiter = column_delimiter
        self.data = []

        # If the file is not set to overwrite, import all the contents of the file.
        if not overwrite:
            # Open the file to read.
            with open(filename, 'r') as f:
                string = ""
                # For each line in the file:
                for line in f:
                    # Add the line to the raw string.
                    string += line
            # Slice up the string and put it into this object's data field.
            lines = string.split(line_delimiter)
            for line in lines:
                values = line.split(column_delimiter)
                self.data.append(values)

    # Write all current data to the file.
    def write():
        string = ""
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data[i])):
                string += self.data[i][j]
                if j < len(self.data[i]) - 1:
                    string += self.column_delimiter
            if i < len(self.data[i]) - 1:
                string += self.line_delimiter

        with open(self.filename) as f:
            f.write(string)