import sijiao_dict

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

def jaccard_similarity(x, y):
    """ 
    Returns the Jaccard similarity between two lists.
    
    Parameters:
    x (list): First list of elements.
    y (list): Second list of elements.
    
    Returns:
    float: Jaccard similarity between two lists.
    """
    intersection_cardinality = len(set(x).intersection(set(y)))
    union_cardinality = len(set(x).union(set(y)))
    return intersection_cardinality / float(union_cardinality)

# Example usage with Chinese characters
text1 = '你敢信骷髅岛扛把子金刚'
text2 = '你敢信骷髅岛扛把'

mapped_text1 = map_characters_to_numbers(text1, sijiao_dict.dic)
mapped_text2 = map_characters_to_numbers(text2, sijiao_dict.dic)

similarity = jaccard_similarity(mapped_text1, mapped_text2)
print(f"Jaccard similarity between '{text1}' and '{text2}': {similarity}")
