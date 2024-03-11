"""
For use with Jan or another directory of models,
this will return a list of optional gguf model-paths
for the llama-cpp api
"""

import os

def find_folders_and_files_with_gguf(base_path):
    folders_and_files_with_gguf = []
    # Iterate through all items in base path
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Check each file in the directory
            for file in os.listdir(item_path):
                # Check if the file ends with '.gguf'
                if file.endswith('.gguf'):
                    # Construct the desired string format: basefolder/filename
                    result = f"{item}/{file}"
                    folders_and_files_with_gguf.append(result)
                    break  # Found a matching file, no need to check the rest
    return folders_and_files_with_gguf

# Base path where to search for folders and gguf files
# base_path = '/home/oops/jan/models'

# # Call the function and print the result
# folders_and_files = find_folders_and_files_with_gguf(base_path)
# for result in folders_and_files:
#     print(f"Model @->  {result}")




def add_segment_to_absolute_base_path(additional_segment):
    # Get the absolute path to the current user's home directory
    home_directory = os.path.expanduser("~")
    # print(f"Home Directory: {home_directory}")  # Debugging print

    # Create an absolute path by joining the home directory with the additional segment
    absolute_path = os.path.join(home_directory, additional_segment)
    # print(f"Joined Path Before abspath: {absolute_path}")  # Debugging print

    # Ensure the path is absolute (this should not change the path if already absolute)
    absolute_path = os.path.abspath(absolute_path)
    # print(f"Final Absolute Path: {absolute_path}")  # Debugging print

    return absolute_path




base_path = add_segment_to_absolute_base_path("jan/models/")

folders_and_files_with_gguf = find_folders_and_files_with_gguf(base_path)

print("\nAvailable Models:")

for this_model_path in folders_and_files_with_gguf:
    print("     ", this_model_path)

print("\n\n")

# def get_model_path_by_name(base_path, model_name):
#     # Call the function to get all folders and files with gguf
#     folders_and_files = find_folders_and_files_with_gguf(base_path)
    
#     # Filter results by model name
#     matching_models = [path for path in folders_and_files if model_name in path]
    
#     # Check the number of matches and return accordingly
#     if len(matching_models) == 1:
#         return matching_models[0]
#     elif len(matching_models) > 1:
#         return "Error: More than one model found matching the given name. Please be more specific."
#     else:
#         return "Error: No models found matching the given name."

# # Example usage
# base_path = '/home/oops/jan/models'
# model_name = ".gguf"
# model_path = get_model_path_by_name(base_path, model_name)

# print(model_path)
