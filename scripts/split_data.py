import os
import shutil
import random

def test_train_split(
        input_dir,
        output_train_dir,
        output_test_dir,
        train_ratio=0.8
):
    # Create train and test directories if they don't exist
    os.makedirs(output_train_dir, exist_ok=True)
    os.makedirs(output_test_dir, exist_ok=True)

    classes = [cls for cls in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, cls))]
    for cls in classes:
        cls_path = os.path.join(input_dir, cls)
        print(f'cls_path: {cls_path}')
        images = [image for image in os.listdir(cls_path) if image.endswith('.jpg') or image.endswith('.png')]
        print(images)
        random.shuffle(images)
        split = int(len(images) * train_ratio)
        train_images = images[:split]
        test_images = images[split:]

        # Create subdirectories for the current class
        train_class_dir = os.path.join(output_train_dir, cls)
        test_class_dir = os.path.join(output_test_dir, cls)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)

        for img in train_images:
            shutil.copy(os.path.join(cls_path, img), os.path.join(train_class_dir, img))
            xml_file = os.path.splitext(img)[0] + '.xml'
            if os.path.exists(os.path.join(cls_path, xml_file)):
                shutil.copy(os.path.join(cls_path, xml_file), os.path.join(train_class_dir, xml_file))

        for img in test_images:
            shutil.copy(os.path.join(cls_path, img), os.path.join(test_class_dir, img))
            xml_file = os.path.splitext(img)[0] + '.xml'
            if os.path.exists(os.path.join(cls_path, xml_file)):
                shutil.copy(os.path.join(cls_path, xml_file), os.path.join(test_class_dir, xml_file))

if __name__ == '__main__':
    test_train_split('data/raw_images', 'data/images/train', 'data/images/test')
