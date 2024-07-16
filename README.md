# OCR_Subtitle_Chinese
This project focuses on developing an Optical Character Recognition (OCR) system to extract Chinese subtitles from video content efficiently. Using advanced OCR techniques and machine learning algorithms, the system will offer a robust solution for accurate subtitle recognition Chinese-language videos.

conda create --name OCR-China python=3.8 <br>
conda activate OCR-China <br>
pip install -r requirements.txt

### Run OCR for video
-Case 1: With low subtitle run: <br>
python main.py --format 1  <br>
-Case 2: With high subtitle run: <br>
python main.py --format 2 

### Export to output capcut format
python postprocess.py

### Optimize timestemp for srt format
python capcut.py


### last one
You need to create a folder to input video, and you can rename to have nothing for a change in the raw source

