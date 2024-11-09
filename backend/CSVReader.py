import csv
import time
import re
from mysql_utils import MySqlUtils
import chardet
#from SEP_logger import SEPLogger


#logger = SEPLogger("./", "SEP_Application.log")

class CSVReader:

    #Entry point
    def __init__(self, directory, file_name):
        print("\nInserting: " + file_name)
        self.directory = directory
        self.file_name = file_name
        self.data = []

        with open(directory + file_name, "rb") as f:
            result = chardet.detect(f.read())

        with open(directory + file_name, newline='', encoding=result["encoding"]) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            #[self.data.append(row) for row in reader]
            for row in reader:
                new_row = []
                count = 0
                for elem in row:
                    if elem != '':
                        new_row.append(elem.replace(" ", "_").replace(".", "_").replace("__", "_"))
                        count += 1
                    else:
                        if count == 0:
                            new_row.append(elem.replace("", "placeholder"))
                            count += 1
                #print(new_row)
                self.data.append(new_row)

        try:
            print(self.data[0][1])
            print("Auto-detected ';' -> Starting to insert.")
        except:
            print("Auto-detected ',' -> Starting to insert.")
            self.data = []
            with open(directory + file_name, newline='', encoding=result["encoding"]) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    new_row = []
                    count = 0
                    for elem in row:
                        if elem != '':
                            new_row.append(elem.replace(" ", "_").replace(".", "_").replace("__", "_"))
                            count += 1
                        else:
                            if count == 0:
                                new_row.append(elem.replace("", "placeholder"))
                                count += 1
                    self.data.append(new_row)



    def insert_into_database(self, db: MySqlUtils):
        # Create a Table (if it not exists already) named filename (w/o .csv)
        if "-" in self.file_name:
            self.file_name = self.file_name.replace("-", "_").replace(" ", "_")
            print(f"""CREATE TABLE IF NOT EXISTS {self.file_name.replace('.csv', '')} (dataset_uid TEXT NOT NULL, {', '.join([col.replace('"', '').replace("/", "_").replace(")", "")
 + ' TEXT' for col in self.data[0]])});""")
            print("\n")

        try:
            db.exec(f"""CREATE TABLE {self.file_name.replace('.csv', '')} (dataset_uid TEXT NOT NULL, {', '.join([col.replace('"', '').replace("/", "_").replace("(", "").replace(")", "") + ' TEXT' for col in self.data[0]])});""")
            counter = 1
            for entry in self.data[1:]:
                build_header_str = ""
                build_content_str = ""
                for i in range(0, len(entry)):
                    entry[i] = entry[i].replace("'", "")
                    if i == 0:
                        build_header_str = f"(dataset_uid, {self.data[0][i]}, "
                        build_content_str = f"('{counter}', '{entry[i]}', "
                    elif i == len(entry) - 1:
                        build_header_str += f"{self.data[0][i]})"
                        build_content_str += f"'{entry[i]}');"
                    else:
                        build_header_str += f"{self.data[0][i]}, "
                        build_content_str += f"'{entry[i]}', "

                # If some parts are missing
                if build_content_str[-1:] != ";":
                    build_header_str = re.sub(r',\s*$', ')', build_header_str)
                    build_content_str = re.sub(r',\s*$', ');', build_content_str)

                #print(f"RUNNING -> INSERT INTO {self.file_name.replace('.csv', '')} {build_header_str} VALUES {build_content_str}")
                try:
                    #logger.log("STATEMENT", f"INSERT INTO {self.file_name.replace('.csv', '')} {build_header_str} VALUES {build_content_str}")
                    db.exec(f"INSERT INTO {self.file_name.replace('.csv', '')} {build_header_str} VALUES {build_content_str}")
                except:
                    print("ERROR -> RETRYING")
                    time.sleep(0.05)
                    db.exec(
                        f"INSERT INTO {self.file_name.replace('.csv', '')} {build_header_str} VALUES {build_content_str}")
                counter += 1
                time.sleep(0.005)

            print(f"[ SUCCESS ]: Inserted {self.file_name} successfully.")

        except Exception as e:
            print(e)
            print(f"\n\n[ ERROR ]: Could not insert {self.file_name}.")
            #logger.log(f"[ ERROR ]: Could not insert {self.file_name}.", e)



if __name__ == "__main__":
    print("starting to insert")
    csvAction = CSVReader("../datasets/", "aachenvornamen2021-commasep-decimalpoint.csv")
    csvAction.insert_into_database(MySqlUtils("127.0.0.1", 3306, "root", "1234", "SEP"))
    print("stopping")