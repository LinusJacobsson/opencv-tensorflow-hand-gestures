import cv2 as cv
import os 
import argparse
import random

def capture_images(
        save_dir, 
        gesture_name,
        num_images,
        video_file=None
):
    os.makedirs(os.path.join(save_dir, gesture_name), exist_ok=True)
    count = 0 

    if video_file: # Use video file instead of live capture
        cap = cv.VideoCapture(video_file)
        total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

        # Make sure we get correct number of frames
        num_frames = min(total_frames, num_images)
        
        frame_indices = sorted(random.sample(range(total_frames), num_frames))
        
        for idx in frame_indices:
            cap.set(cv.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if not ret:
                continue # Skip frame if it can't be read properly

            img_name = os.path.join(save_dir, gesture_name, f'{gesture_name}_{count}.jpg')
            cv.imwrite(img_name, frame)
            print(f'Image {img_name} saved from frame {idx}.')
            count += 1

        cap.release()
        print(f'Finished - saved {count} images from video.')

    else:
        # Use webcam directly
        cap = cv.VideoCapture(0) # Change arg for different video source.
        print(f'Press "s" to save frame, "q" to quit.')
        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                print('Failed to grab frame from webcam.')
                break
        
            cv.imshow('Capture Images - Press "s" to save, "q" to quit.', frame)
            key = cv.waitKey(1) & 0xFF

            if key == ord('s'):
                img_name = os.path.join(save_dir, gesture_name, f'{gesture_name}_{count}.jpg')
                cv.imwrite(img_name, frame)
                print(f'Image {img_name} saved.')
                count += 1
            elif key == ord('q'):
                print('Quitting webcam capture.')
                break
        cap.release()
        cv.destroyAllWindows()
        print(f'Finished - saved {count} images from webcam.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Capture training data for hand gesture recognition.')
    parser.add_argument('--save_dir', type=str, default='data/raw_images11', help='Directory to save images.')
    parser.add_argument('--gesture_name', type=str, required=True, help='Name of hand gesture class.')
    parser.add_argument('--num_images', type=int, default=5, help='Number of images to capture.')
    parser.add_argument('--video_file', type=str, help='Path to existing video file.')
    args = parser.parse_args()

    capture_images(args.save_dir, args.gesture_name, args.num_images, args.video_file)