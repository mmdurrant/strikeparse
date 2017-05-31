import os

from strikeparse.data_models import StrikeKit

PARSE_DIR = "d:\\Projects\\Music\\StrikePro\\strikeparse\\strikeparse\\data"

def main():
    # Iterate through the files in the data folder.
    # Print the file name.
    # Print the CSV representation of the kit indented.
    files = filter(lambda x: x.endswith(".skt"), os.listdir(PARSE_DIR))
    for x in files:
        kit_name = x[4:-4]
        full_path = "\\".join([PARSE_DIR, x])
        with open(full_path, 'rb') as f:
            d = f.read()
            kit = StrikeKit(raw_data=d)
            for i in kit.instruments:
                print(",".join([kit_name, i.csv()]))


if __name__ == "__main__":
    main()
