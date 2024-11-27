import os
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    print(f"Searching for XML files in: {path}")
    for root_dir, _, files in os.walk(path):
        for file in files:
            if file.endswith('.xml'):
                xml_file = os.path.join(root_dir, file)
                print(f"Processing file: {xml_file}")
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()

                    for member in root.findall('object'):
                        value = (
                            root.find('filename').text,
                            int(root.find('size/width').text),
                            int(root.find('size/height').text),
                            member.find('name').text,
                            int(member.find('bndbox/xmin').text),
                            int(member.find('bndbox/ymin').text),
                            int(member.find('bndbox/xmax').text),
                            int(member.find('bndbox/ymax').text),
                        )
                        xml_list.append(value)
                        print(f"Added entry: {value}")
                except Exception as e:
                    print(f"Error processing {xml_file}: {e}")

    column_names = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_names)
    return xml_df

def main():
    for directory in ['train', 'test']:
        image_path = os.path.join(os.getcwd(), f'data/images/{directory}')
        print(f"Base directory for search: {image_path}")
        xml_df = xml_to_csv(image_path)
        os.makedirs('data/annotations', exist_ok=True)  # Ensure annotations directory exists
        if not xml_df.empty:
            output_csv = f'data/annotations/{directory}_labels.csv'
            xml_df.to_csv(output_csv, index=False)
            print(f'Conversion of XML to CSV for {directory} was successful. Output saved to {output_csv}')
        else:
            print(f"No data found for {directory}.")

if __name__ == '__main__':
    main()
