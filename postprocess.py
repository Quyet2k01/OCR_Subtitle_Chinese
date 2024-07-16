import os
import re
import CharSimilarity
import sijiao_dict
def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def parse_srt(content):
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)
    subtitles = [{'index': m[0], 'start': m[1], 'end': m[2], 'text': m[3].replace('\n', ' ')} for m in matches]
    return subtitles

def char_similarity(str1, str2):
    if not str1 or not str2:
        return 0.0
    return CharSimilarity.similarity(str1, str2, tone=True, shape=False)
def similarity(x, y):
    """ 
    Returns the similarity between two lists.
    
    Parameters:
    x (list): First list of elements.
    y (list): Second list of elements.
    
    Returns:
    float: Jaccard similarity between two lists.
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
def process_srt(subtitles):
    for i in range(1, len(subtitles) - 1):
        text_A = subtitles[i]['text']
        text_B = subtitles[i-1]['text']
        text_C = subtitles[i+1]['text']

        mapped_A = map_characters_to_numbers(text_A, sijiao_dict.dic)
        mapped_B = map_characters_to_numbers(text_B, sijiao_dict.dic)
        mapped_C = map_characters_to_numbers(text_C, sijiao_dict.dic)

        sim_AC = similarity(mapped_A, mapped_C)
        sim_BC = similarity(mapped_B, mapped_C)
        sim_AB = similarity(mapped_A, mapped_B)
        sim_AB_v2 = char_similarity(text_A, text_B)
        if sim_AB>=0.6:
            subtitles[i]['text'] = text_B

        elif sim_AB<0.6:
            subtitles[i]['text'] = text_A

    return subtitles

def write_srt(subtitles, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for sub in subtitles:
            file.write(f"{sub['index']}\n{sub['start']} --> {sub['end']}\n{sub['text']}\n\n")

def process_srt_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.srt'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            srt_content = read_srt(input_file)
            subtitles = parse_srt(srt_content)
            processed_subtitles = process_srt(subtitles)
            write_srt(processed_subtitles, output_file)

# Example usage
input_folder = 'video/'
output_folder = 'srt_files_processed/'

process_srt_files(input_folder, output_folder)
