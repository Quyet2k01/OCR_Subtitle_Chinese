import os
import CharSimilarity
import sijiao_dict

def similarity(x, y):
    """ 
    Returns the similarity between two lists.
    
    Parameters:
    x (list): First list of elements.
    y (list): Second list of elements.
    
    Returns:
    float: Similarity between two lists.
    """
    intersection_cardinality = len(set(x).intersection(set(y)))
    union_cardinality = len(set(x).union(set(y)))
    if union_cardinality == 0:
        return 0.0
    return intersection_cardinality / float(union_cardinality)

def map_characters_to_numbers(text, char_map):
    """
    Map characters in the input text to their corresponding numbers using the provided character map.
    
    Parameters:
    text (str): Input string with Chinese characters.
    char_map (dict): Dictionary mapping Chinese characters to numbers.
    
    Returns:
    list: List of numbers corresponding to the input characters.
    """
    return [char_map[char] for char in text if char in char_map]

def merge_subtitles(srt_content):
    subtitles = srt_content.strip().split('\n\n')
    
    merged_subtitles = []
    current_start = None
    current_end = None
    current_text = None
    
    for subtitle in subtitles:
        parts = subtitle.split('\n')
        if len(parts) < 3:
            continue
        number = parts[0]
        time_range = parts[1]
        text = ''.join(parts[2:])
        
        start_time, end_time = time_range.split(' --> ')
        
        # Check if the current end time is greater than the new start time and adjust if needed
        if current_end and start_time <= current_end:
            start_time = current_end
            
        if current_text is None:
            current_start = start_time
            current_end = end_time
            current_text = text
        elif similarity(map_characters_to_numbers(current_text, sijiao_dict.dic), map_characters_to_numbers(text, sijiao_dict.dic)) == 1:
            current_end = end_time
        else:
            merged_subtitles.append(f'{len(merged_subtitles) + 1}\n{current_start} --> {current_end}\n{current_text}')
            current_start = start_time
            current_end = end_time
            current_text = text
    
    if current_text is not None:
        merged_subtitles.append(f'{len(merged_subtitles) + 1}\n{current_start} --> {current_end}\n{current_text}')
    
    return '\n\n'.join(merged_subtitles)

def process_srt_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.srt'):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)
            
            with open(input_file_path, 'r', encoding='utf-8') as file:
                srt_content = file.read()
            
            merged_srt_content = merge_subtitles(srt_content)
            
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(merged_srt_content)
    
    print("Processing completed!")

# Ví dụ sử dụng
input_folder = 'srt_files_processed'
output_folder = 'capcut_format'

process_srt_files(input_folder, output_folder)
