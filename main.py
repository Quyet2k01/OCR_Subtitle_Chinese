import os
import cv2
import argparse
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=False, lang='ch')

def extract_frames(video_path, output_folder, frames_per_second, crop_format):
    cap = cv2.VideoCapture(video_path)
    # Hiển thị FPS của video
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video FPS: {fps}")
    count = 0
    interval = int(fps / frames_per_second)

    success, image = cap.read()
    while success:
        frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if frame_id % interval == 0:
            cropped_image = crop_subtitle(image, crop_format)
            cv2.imwrite(os.path.join(output_folder, f"frame_{count}.jpg"), cropped_image)
            count += 1
        success, image = cap.read()
    cap.release()

def crop_subtitle(image, crop_format):
    height, width, _ = image.shape

    if crop_format == 1:
        crop_top = int(height * 0.920)
        crop_bottom = int(height * 0.98)
    elif crop_format == 2:
        crop_top = int(height * 0.825)
        crop_bottom = int(height * 0.9)
    else:
        raise ValueError("Invalid crop format specified. Use 1 or 2.")

    crop_left = int(width * 0.2)  
    crop_right = int(width * 0.8)  
    cropped_image = image[crop_top:crop_bottom, crop_left:crop_right]
    return cropped_image

def process_frames(frames_folder, output_file, frames_per_second):
    with open(output_file, 'w', encoding='utf-8') as f:
        index = 1
        for frame_name in sorted(os.listdir(frames_folder), key=lambda x: int(x.split('_')[1].split('.')[0]) if 'frame_' in x else float('inf')):
            if frame_name.endswith('.jpg') and 'frame_' in frame_name:
                frame_path = os.path.join(frames_folder, frame_name)
                img = cv2.imread(frame_path)
                results = ocr.ocr(img)

                if results and len(results) > 0:
                    result_list = results[0]
                    if result_list:
                        text_list = [box[1][0] for box in result_list]
                    else:
                        text_list = []
                else:
                    text_list = []

                frame_number = int(frame_name.split('_')[1].split('.')[0])
                start_time = frame_number / frames_per_second
                end_time = start_time + 1 / frames_per_second

                for text in text_list:
                    start_hours = int(start_time // 3600)
                    start_minutes = int((start_time % 3600) // 60)
                    start_seconds = int(start_time % 60)
                    start_milliseconds = int((start_time % 1) * 1000)

                    end_hours = int(end_time // 3600)
                    end_minutes = int((end_time % 3600) // 60)
                    end_seconds = int(end_time % 60)
                    end_milliseconds = int((end_time % 1) * 1000)

                    time_format = f"{start_hours:02}:{start_minutes:02}:{start_seconds:02},{start_milliseconds:03} --> {end_hours:02}:{end_minutes:02}:{end_seconds:02},{end_milliseconds:03}"

                    f.write(f"{index}\n")
                    f.write(f"{time_format}\n")
                    f.write(text + '\n')
                    f.write('\n')

                    index += 1

def process_videos_in_folder(crop_format):
    root_folder = 'video'
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.mp4'):
                video_path = os.path.join(dirpath, filename)
                video_name = os.path.splitext(filename)[0]
                frames_folder = os.path.join(dirpath, f'{video_name}_frames')
                output_file = os.path.join(dirpath, f'{video_name}.srt')
                
                if not os.path.exists(frames_folder):
                    os.makedirs(frames_folder)
                
                frames_per_second = 30
                extract_frames(video_path, frames_folder, frames_per_second, crop_format)
                process_frames(frames_folder, output_file, frames_per_second)
                
                print(f"Processed video: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Extract subtitles from videos.')
    parser.add_argument('--format', type=int, choices=[1, 2], required=True, help='Crop format (low or high).')
    
    args = parser.parse_args()
    
    process_videos_in_folder(args.format)
    print("Subtitle extraction completed for all videos!")

if __name__ == "__main__":
    main()
