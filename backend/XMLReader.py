import xml.etree.ElementTree as ET


class XMLReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_xml(self):
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            for child in root:
                print("Start element:", child.tag)
                for key, value in child.attrib.items():
                    print("Attribute:", key, "=", value)

                for grandchild in child:
                    print("Start element:", grandchild.tag)
                    print("Text:", grandchild.text)
                    print("End element:", grandchild.tag)

                print("End element:", child.tag)

        except FileNotFoundError:
            print("File not found:", self.file_path)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    reader = XMLReader("example.xml")
    reader.parse_xml()
