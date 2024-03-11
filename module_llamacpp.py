"""

This is part of a deliberately 'small' micro-operation
to do a finite operation
in a set of sets of operations
in a structured externalized-tabular project-object-database format

this may not seem different from plum-pudding model output, but it is.

With this building block
many modular avenues for doing task, and testing-benchmarking abilities, are opened up.
Modular-recombinant processes.


Instructions:
1. Install Jan and download some models
2. Download any other models and put in the models folders in their own folders
3. Use this from anywhere, putting in the path to the models' folder

note:
There is a function to tell you what gguf models you already have and can pick from
You can use a shortened version of the model name.
 - get_model_path_by_name(base_path, model_name)


Note:
Context-history looks like a big mystery...

TODO:

fix broken skeleton structure:
- 

todo: make a cli_gguf.py version that takes
parameters, e.g. taking pack-unpack as the input
or otherwise normal input instructions.

experiment with .csv format output





add a chat_llamacapp.py

using chat-context wrapper from Mixtral et all

"""

import subprocess
import os
from datetime import datetime, UTC



def ensure_path_exists(path):
    """
    Check if the specified path exists.

    Args:
    path (str): The path to check for existence.

    Raises:
    IOError: If the specified path does not exist.
    """
    if not os.path.exists(path):
        raise IOError(f"The specified path does not exist: {path}")


def api_llamacapp(
    prompt, cpp_path, model_path_base, model_and_folder, parameter_dict=[]
):
    """
    requires:
        import subprocess

    function/script code in python to make use of llama.cpp cli
    in project pipelines,
    e.g. to swap-in for another API (public cloud, not private)
    e.g. to use a local mode instead of an online-api (local, offline, private)

    """

    prompt = re.sub(r'\s+', ' ', prompt.strip())

    prompt = prompt.replace("\\", "\\\\")  
    prompt = prompt.replace("\n", "")
    prompt = prompt.replace("\\n", "")

    # prompt = prompt.replace('json', '')  
    # prompt = prompt.replace('"', '')  
    prompt = prompt.replace('"', '\\"')
    # prompt = prompt.replace('`', '\\`')          
    # prompt = prompt.replace("'", "\\'")  

    prompt = prompt.strip()

    # inspection
    print("api_llamacapp() starto!!")
    print(f"""
    prompt -> {prompt}

    cpp_path -> {cpp_path}
    model_path_base -> {model_path_base}
    model_and_folder -> {model_and_folder}
    parameter_dict -> {parameter_dict}
    """)




    ######################
    # Make paths absolute
    ######################
    cpp_path = os.path.abspath(cpp_path)
    model_path_base = os.path.abspath(model_path_base)

    # make new path
    # Constructing the whole model path by joining the two parts
    whole_model_path = os.path.join(model_path_base, model_and_folder)
    # Make absolute
    whole_model_path = os.path.abspath(whole_model_path)


    #############################
    # double checking file paths
    #############################
    path_list_to_check = [
        cpp_path,
        whole_model_path
    ]

    for this_path in path_list_to_check:
        ensure_path_exists(this_path)

    #############
    # Parameters
    #############

    parameter_string = ""

    #######################################
    # Construct string of extra parameters
    ########################################
    for key, value in parameter_dict.items():

        # There will be a key, so add it in
        parameter_string += str(key) + " "

        # if there is a value, add that too
        if value:
            parameter_string += str(value) + " "

    print(f"parameter_string -> {parameter_string}")

    # Define the command as a string
    command = f"""
    make -j && ./main 2>/dev/null -m {whole_model_path} {parameter_string} --prompt "{prompt}"
    """

    # Define the command as a string
    command = f"""
    ./main 2>/dev/null -m {whole_model_path} {parameter_string} --prompt "{prompt}"
    """

    # Define the command as a string
    command = f"""./main 2>/dev/null -m {whole_model_path} --prompt "{prompt}" {parameter_string}"""

    # note: set threads to cpu count

    # Define the command as a string
    command = f"""./main 2>/dev/null -m {whole_model_path} --temp {parameter_dict["--temp"]} --top-k {parameter_dict["--top-k"]} --top-p {parameter_dict["--top-p"]} --min-p {parameter_dict["--min-p"]} --seed {parameter_dict["--seed"]} --tfs {parameter_dict["--tfs"]} --typical {parameter_dict["--typical"]} --mirostat {parameter_dict["--mirostat"]} --mirostat-lr {parameter_dict["--mirostat-lr"]} --mirostat-ent {parameter_dict["--mirostat-ent"]} --threads {str(int(os.cpu_count()))} --ctx-size {parameter_dict["--ctx-size"]} -p "{prompt}" """

    # # inspection
    print(f"command -> {repr(command)}")

    possible_exception = ""

    #################################
    # Try to Run Model, Prompt Model
    #################################
    """
    Use subprocess.run to execute the ~bash cli command
    Shell=True is used to interpret the command as a string and execute it through the shell
    This is necessary for commands that involve shell operators like '&&'

    make -j && ./main 2>/dev/null -m /home/xxx/jan/models/tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p "What is a horseshoe crab?"

    ./main 2>/dev/null -m /home/xxx/jan/models/tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p "What is a horseshoe crab?"

    """
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=cpp_path
        )

    except Exception as e:
        possible_exception = str(e)

    #######################################
    # Examine and Handle Attpted Model Use
    #######################################

    # get return coce (zero means no error, 1 or other means error)
    return_code_zero_means_ok = result.returncode

    if result.returncode == 0:

        # Assuming valid output means non-empty stdout
        if result.stdout.strip():
            #####################################
            # Look for Standard Ouput (no error)
            #####################################

            # Valid output received; print the standard output
            # print(f"result.returncode=={result.returncode}--Assisant: ")
            # print(result.stdout)

            # get return coce (zero means no error, 1 or other means error)
            return_code_zero_means_ok = result.returncode

            # Write a custom status message
            status_message = f"status_message: OK!!"

            # The model's output
            model_output = result.stdout

            # Make a tuple of output data for granular separate use
            ok_output_tuple = (return_code_zero_means_ok, status_message, model_output)

            # pseudo return
            return ok_output_tuple

        else:
            ##################################
            # Look for Standard Error message
            ##################################

            # No valid output; check if there's an error message
            if result.stderr.strip():
                # Print the standard error if error info is available
                status_message = f"api_llamacapp() ERROR: An error occured. {possible_exception}"

                # The model's ERROR output
                model_output = f"api_llamacapp()  result.stderr.strip() STDERR: {result.stderr}"

                # Make a tuple of output data for granular separate use
                not_ok_output_tuple = (
                    return_code_zero_means_ok,
                    status_message,
                    model_output,
                )

                # pseudo return
                return not_ok_output_tuple

            else:  # No error reported, BUT no output either !!

                # No output and no error; might indicate an unexpected issue or simply no output for the input
                status_message = (
                    f"Strange: No output and no detected errors. {possible_exception}"
                )

                # No error reported, BUT no output either
                model_output = "blank"

                # Make a tuple of output data for granular separate use
                not_ok_output_tuple = (
                    return_code_zero_means_ok,
                    status_message,
                    model_output,
                )

                # pseudo return
                return not_ok_output_tuple

    elif result.returncode != 0:

        # No output and no error; might indicate an unexpected issue or simply no output for the input
        status_message = (
            f"Error: # No output and no error; might indicate an unexpected issue or simply no output for the input. {possible_exception}"
        )

        if result.stderr.strip():
            # The model's ERROR output
            model_output = f"STDERR: {result.stderr}"
        else:
            # No error reported, BUT no output either
            model_output = f"No standard output or STDERR standard error"

        # Make a tuple of output data for granular separate use
        not_ok_output_tuple = (return_code_zero_means_ok, status_message, model_output)

        # pseudo return
        return not_ok_output_tuple


##############
# Setup Layer
##############



def get_absolute_base_path():
    # Get the absolute path to the current user's home directory (Starts from root, ends at home directory)
    home_directory = os.path.expanduser("~")  # e.g., "/home/john"

    absolute_path = os.path.abspath(home_directory)

    return absolute_path


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


def prompt_setup_llamacpp(prompt):
    parameter_dict = {
        "--temp N": 0.8,  # (default value is 0.8)
        "--top-k": 40,  # (selection among N most probable. default: 40)
        "--top-p": 0.9,  # (probability above threshold P. default: 0.9)
        "--min-p": 0.05,  # (minimum probability threshold. default: 0.05)
        "--seed": -1,  # seed, =1 is random seed
        "--tfs": 1,  # (tail free sampling with parameter z. default: 1.0) 1.0 = disabled
        "--threads": 8,  # (~ set to number of physical CPU cores)
        "--typical": 1,  # (locally typical sampling with parameter p  typical (also like ~Temperature) (default: 1.0, 1.0 = disabled).
        "--mirostat": 2,  # (default: 0,  0= disabled, 1= Mirostat, 2= Mirostat 2.0)
        "--mirostat-lr": 0.05,  # (Mirostat learning rate, eta.  default: 0.1)
        "--mirostat-ent": 3.0,  # (Mirostat target entropy, tau.  default: 5.0)
        "--ctx-size": 500,  # Sets the size of the prompt context
    }


    model_path_base = add_segment_to_absolute_base_path("jan/models/")
    model_name = "tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    cpp_path = add_segment_to_absolute_base_path("code/llama_cpp/llama.cpp")

    result = api_llamacapp(
        prompt, cpp_path, model_path_base, model_name, parameter_dict
    )

    # get third part of tuple
    exit_code = result[0]
    message = result[1]
    assistant_says = result[2]

    # print(f"exit_code - > {exit_code}")
    # print(f"message - > {message}")
    # print(f"assistant_says - > {assistant_says}")

    return assistant_says


def jan_model_history_local_gguf_api(this_model, converstion_history):

    #######################
    # Tune Your Paramaters
    #######################
    parameter_dict = {
        "--temp N": 0.8,  # (default value is 0.8)
        "--top-k": 40,  # (selection among N most probable. default: 40)
        "--top-p": 0.9,  # (probability above threshold P. default: 0.9)
        "--min-p": 0.05,  # (minimum probability threshold. default: 0.05)
        "--seed": -1,  # seed, =1 is random seed
        "--tfs": 1,  # (tail free sampling with parameter z. default: 1.0) 1.0 = disabled
        "--threads": 8,  # (~ set to number of physical CPU cores)
        "--typical": 1,  # (locally typical sampling with parameter p  typical (also like ~Temperature) (default: 1.0, 1.0 = disabled).
        "--mirostat": 2,  # (default: 0,  0= disabled, 1= Mirostat, 2= Mirostat 2.0)
        "--mirostat-lr": 0.05,  # (Mirostat learning rate, eta.  default: 0.1)
        "--mirostat-ent": 3.0,  # (Mirostat target entropy, tau.  default: 5.0)
        "--ctx-size": 500,  # Sets the size of the prompt context
    }

    # set your local jan path
    # model_path_base = "/home/xxx/jan/models/"

    # model_name = "tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

    # cpp_path = "/home/xxx/code/llama_cpp/llama.cpp"


    model_path_base = add_segment_to_absolute_base_path("jan/models/")
    model_name = "tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    cpp_path = add_segment_to_absolute_base_path("code/llama_cpp/llama.cpp")

    prompt = str(converstion_history)

    result = api_llamacapp(
        prompt, cpp_path, model_path_base, model_name, parameter_dict
    )

    # get third part of tuple
    exit_code = result[0]
    message = result[1]
    assistant_says = result[2]

    # print(f"exit_code - > {exit_code}")
    # print(f"message - > {message}")
    # print(f"assistant_says - > {assistant_says}")

    return assistant_says


"""
For use with Jan or another directory of models,
this will return a list of optional gguf model-paths
for the llama-cpp api
"""


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
                if file.endswith(".gguf"):
                    # Construct the desired string format: basefolder/filename
                    result = f"{item}/{file}"
                    folders_and_files_with_gguf.append(result)
                    break  # Found a matching file, no need to check the rest
    return folders_and_files_with_gguf


# Base path where to search for folders and gguf files
# base_path = '/home/xxx/jan/models'

# # Call the function and print the result
# folders_and_files = find_folders_and_files_with_gguf(base_path)
# for result in folders_and_files:
#     print(f"Model @->  {result}")


def sanitize_for_bash(input_str):
    """
    Sanitize a string by replacing curly braces, square brackets, and double quotes
    with parentheses and single quotes to avoid bash conflicts.

    Args:
    - input_str (str): The input string to be sanitized.

    Returns:
    - str: The sanitized string.
    """
    # Replace curly braces and square brackets with parentheses
    sanitized_str = input_str.replace("{", "(").replace("}", ")")
    sanitized_str = sanitized_str.replace("[", "(").replace("]", ")")
    sanitized_str = sanitized_str.replace("[", "(").replace("]", ")")

    # experimental:
    sanitized_str = sanitized_str.replace(
        """'role': 'system', 'content'""", "Instruction you must follow"
    )
    sanitized_str = sanitized_str.replace(
        """'role': 'assistant', 'content'""", "Then you said"
    )
    sanitized_str = sanitized_str.replace(
        """'role': 'user', 'content'""", "Then I said"
    )

    # Replace double quotes with single quotes
    sanitized_str = sanitized_str.replace('"', "'")

    return sanitized_str


def get_model_path_by_name(base_path, model_name):


    # inspection
    print(f"base_path -> {base_path}")
    print(f"model_name -> {model_name}")
    # Call the function to get all folders and files with gguf
    folders_and_files = find_folders_and_files_with_gguf(base_path)

    # Filter results by model name
    matching_models = [path for path in folders_and_files if model_name in path]

    # Check the number of matches and return accordingly
    if len(matching_models) == 1:
        # # inspection
        # print(matching_models[0])

        return matching_models[0]
    elif len(matching_models) > 1:
        print(f"Error: More than one model found matching the given name. Please be more specific: {matching_models}")
    else:
        raise "Error: No models found matching the given name."


# # Example usage
# base_path = '/home/xxx/jan/models'
# model_name = input("Please enter the model name you are looking for: ")
# model_path = get_model_path_by_name(base_path, model_name)

# print(model_path)


def call_ggug_modelname_history(model_nickname, converstion_history):

    #######################
    # Tune Your Paramaters
    #######################
    parameter_dict = {
        "--temp N": 0.8,  # (default value is 0.8)
        "--top-k": 40,  # (selection among N most probable. default: 40)
        "--top-p": 0.9,  # (probability above threshold P. default: 0.9)
        "--min-p": 0.05,  # (minimum probability threshold. default: 0.05)
        "--seed": -1,  # seed, =1 is random seed
        "--tfs": 1,  # (tail free sampling with parameter z. default: 1.0) 1.0 = disabled
        "--threads": 8,  # (~ set to number of physical CPU cores)
        "--typical": 1,  # (locally typical sampling with parameter p  typical (also like ~Temperature) (default: 1.0, 1.0 = disabled).
        "--mirostat": 2,  # (default: 0,  0= disabled, 1= Mirostat, 2= Mirostat 2.0)
        "--mirostat-lr": 0.05,  # (Mirostat learning rate, eta.  default: 0.1)
        "--mirostat-ent": 3.0,  # (Mirostat target entropy, tau.  default: 5.0)
        "--ctx-size": 500,  # Sets the size of the prompt context
    }

    # set your local jan path
    # model_path_base = "/home/xxx/jan/models/"



    # print(model_path)

    # cpp_path = "/home/xxx/code/llama_cpp/llama.cpp"

    model_path_base = add_segment_to_absolute_base_path("jan/models/")
    model_path = get_model_path_by_name(model_path_base, model_nickname)

    # model_name = "tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    cpp_path = add_segment_to_absolute_base_path("code/llama_cpp/llama.cpp")


    prompt = f"{sanitize_for_bash(str(converstion_history))}"
    result = api_llamacapp(
        prompt, cpp_path, model_path_base, model_path, parameter_dict
    )

    # get third part of tuple
    exit_code = result[0]
    message = result[1]
    assistant_says = result[2]

    # print(f"exit_code - > {exit_code}")
    # print(f"message - > {message}")
    # print(f"assistant_says - > {assistant_says}")

    return assistant_says


# ###################
# # Use direct prompt
# ###################
# prompt = "What is a horseshoe crab?"
# assistant_reponds = prompt_setup_llamacpp(prompt)
# # print(type(assistant_reponds))

# print(
#     """
# ###################
# Use direct prompt
# ###################
# prompt = "What is a horseshoe crab?"
# assistant_reponds = prompt_setup_llamacpp(prompt)
# """
# )

# print(assistant_reponds)




data = [
    {"role": "system", "content": "You are a talking bird."},
    {"role": "assistant", "content": "Squawk, I am a bird."},
    {"role": "user", "content": "what is a bird?"},
]


#############################
# Use model select + history
#############################
conversation_history = [
    {"role": "system", "content": "You are a friendly assistant."},
    {"role": "user", "content": "Is cooking easy?"},
    {"role": "assistant", "content": "Yes, it is. What shall we cook?"},
    {"role": "user", "content": "Let's make bread."},
    {"role": "assistant", "content": "Here is a good cornbread recipe..."},
    {"role": "user", "content": "What seafood are we cooking now?"},
]


"""
input: 3 dictionaries
1. conversation history dict that include system instruction (if any)
2. a parameters dict
3. a model selection dict

"""

def gguf_api(conversation_history_context_list, parameter_dict, configies_dict):

    ############################   
    # Take conversation history
    ############################

    # Define the path to the system_instructions directory
    system_instructions_dir = "system_instructions_files"

    # make absolute path
    system_instructions_dir = os.path.abspath(system_instructions_dir)

    # Check if the system_instructions directory exists
    if not os.path.exists(system_instructions_dir):
        # If the directory does not exist, create it
        os.makedirs(system_instructions_dir)

    # from datetime import datetime, UTC
    date_time = datetime.now(UTC)
    clean_timestamp = date_time.strftime('%Y%m%d%H%M%S%f')

    system_instruction_file_name = f"{clean_timestamp}_instructions.txt"

    # Add system_instruction_file to path
    system_instructions_dir = os.path.join(system_instructions_dir, system_instruction_file_name)

    with open(system_instructions_dir, "w") as f_load:
        for item in conversation_history_context_list:
            if item["role"] == "system":
                f_load.write(item["content"])
                # print(item["content"])

                # set "instruct" in model parameters
                # system_instruction_file_location = f"--instruct {system_instructions_dir}"
                parameter_dict["--instruct"] = system_instructions_dir
                break
            else:
                print("Note: no instruct found.")
                pass

    # search from the end backwards [-1] as that is where the user prompt will be:
    for item in conversation_history_context_list[-1:]:
        if item["role"] == "user":
            prompt = item["content"]
            # print(prompt)
            break
        else:
            print("Warning, no user prompt found.")
            print(conversation_history_context_list)
            prompt = conversation_history_context_list


    ################################################
    # Setting up and formatting single, line prompt
    ################################################

    system_role = ""
    user_role = ""

    for item in conversation_history_context_list:
        if item["role"] == "system":

            system_role += "(System Instruction) System: "

            system_role += item["content"] + ' '
            # print(system_role)
            break
        else:
            print("Note: no instruct found.")
            pass

    # search from the end backwards [-1] as that is where the user prompt will be:
    for item in conversation_history_context_list[-1:]:
        if item["role"] == "user":


            user_role += "(User Instruction) User: "

            user_role += item["content"] + ' '
            # print(user_role)
            break
        else:
            print("Warning, no user prompt found. defaulting to cleaned whole context")
            print(conversation_history_context_list)
            prompt = conversation_history_context_list
            prompt = prompt.replace("\\", "")
            prompt = prompt.replace("\n", "")
            prompt = prompt.replace("\\n", "")
            prompt = prompt.replace('"', "")
            prompt = prompt.replace('`', "")        
            prompt = prompt.replace("'", "")


    # make whole prompt
    prompt = system_role + user_role

    prompt = prompt.replace("\n", "")
    prompt = prompt.replace("\\n", "")

    # inspection
    print(f"repr(prompt) -> {repr(prompt)}")

    # # set your local jan path
    model_path_base = configies_dict["model_path_base"]
    model_nickname = configies_dict["model_nickname"]

    # point to llama.cpp where install in local system
    cpp_path = configies_dict["cpp_path"]

    # point to where model is, ideally: ~models/model_name/model.gguf 
    model_path = get_model_path_by_name(model_path_base, model_nickname)

    print(f"model_path - > {model_path}")
    print(f"parameter_dict - > {parameter_dict}")



    ###########################
    # Call low level llama.cpp
    ###########################
    result = api_llamacapp(
        prompt, cpp_path, model_path_base, model_path, parameter_dict
    )

    # get third part of tuple
    exit_code = result[0]
    message = result[1]
    assistant_says = result[2]

    print(f"exit_code - > {exit_code}")
    print(f"message - > {message}")
    print(f"len(assistant_says) - > {len(assistant_says)}")

    ###########################
    # Clean up and return
    ###########################

    # # remove old instructions file
    # if os.path.exists(system_instructions_dir):
    #     os.remove(system_instructions_dir)

    return result




def mini_gguf_api(conversation_history_context_list, parameter_dict, configies_dict):

    ############################   
    # Take conversation history
    ############################

    # # Define the path to the system_instructions directory
    # system_instructions_dir = "system_instructions_files"

    # # make absolute path
    # system_instructions_dir = os.path.abspath(system_instructions_dir)

    # # Check if the system_instructions directory exists
    # if not os.path.exists(system_instructions_dir):
    #     # If the directory does not exist, create it
    #     os.makedirs(system_instructions_dir)

    # # from datetime import datetime, UTC
    # date_time = datetime.now(UTC)
    # clean_timestamp = date_time.strftime('%Y%m%d%H%M%S%f')

    # system_instruction_file_name = f"{clean_timestamp}_instructions.txt"

    # # Add system_instruction_file to path
    # system_instructions_dir = os.path.join(system_instructions_dir, system_instruction_file_name)

    # with open(system_instructions_dir, "w") as f_load:
    #     for item in conversation_history_context_list:
    #         if item["role"] == "system":
    #             f_load.write(item["content"])
    #             # print(item["content"])

    #             # set "instruct" in model parameters
    #             # system_instruction_file_location = f"--instruct {system_instructions_dir}"
    #             parameter_dict["--instruct"] = system_instructions_dir
    #             break
    #         else:
    #             print("Note: no instruct found.")
    #             pass

    # # search from the end backwards [-1] as that is where the user prompt will be:
    # for item in conversation_history_context_list[-1:]:
    #     if item["role"] == "user":
    #         prompt = item["content"]
    #         # print(prompt)
    #         break
    #     else:
    #         print("Warning, no user prompt found.")
    #         print(conversation_history_context_list)
    #         prompt = conversation_history_context_list


    ################################################
    # Setting up and formatting single, line prompt
    ################################################


    # make whole prompt
    prompt = conversation_history_context_list

    prompt = prompt.replace("\n", "")
    prompt = prompt.replace("\\n", "")

    # # inspection
    # print(f"prompt -> {repr(prompt)}")

    # # set your local jan path
    model_path_base = configies_dict["model_path_base"]
    model_nickname = configies_dict["model_nickname"]

    # point to llama.cpp where install in local system
    cpp_path = configies_dict["cpp_path"]

    # point to where model is, ideally: ~models/model_name/model.gguf 
    model_path = get_model_path_by_name(model_path_base, model_nickname)

    # inspection
    # print(f"conversation_history_context_list -> {conversation_history_context_list}")    
    # print(f"model_path - > {model_path}")
    # print(f"parameter_dict - > {parameter_dict}")


    ###########################
    # Call low level llama.cpp
    ###########################
    result = api_llamacapp(
        prompt, cpp_path, model_path_base, model_path, parameter_dict
    )

    # get third part of tuple
    exit_code = result[0]
    message = result[1]
    assistant_says = result[2]

    print(f"exit_code - > {exit_code}")
    print(f"message - > {message}")
    print(f"len(assistant_says) - > {len(assistant_says)}")

    ###########################
    # Clean up and return
    ###########################

    # # remove old instructions file
    # if os.path.exists(system_instructions_dir):
    #     os.remove(system_instructions_dir)

    return result


# # Define the request body
# request_body = {
#     "model": "mistral-small",  # 'mistral-small' is 8x7, vs. 'mistral-tiny' for 7b
#     "messages": conversation_history,
# }

# Send the request
# response = requests.post(endpoint_url, headers=headers, json=request_body)

# conversation_history = "What is a horseshoe crab?"

# response = call_ggug_modelname_history(model_nickname, converstion_history)
# print(
#     """
#     call_ggug_modelname_history("tinyllama", conversation_history)
#     """
# )
# response = call_ggug_modelname_history("tinyllama", conversation_history)


model_path_base = add_segment_to_absolute_base_path("jan/models/")
# model_name = "tinyllama-1.1b/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
cpp_path = add_segment_to_absolute_base_path("code/llama_cpp/llama.cpp")




# configies_dict = {
#     'model_path_base': "/home/xxx/jan/models/",
#     'model_nickname': "tinyllama",
#     'cpp_path': "/home/xxx/code/llama_cpp/llama.cpp"
# }


#############################
# Use model select + history
#############################
conversation_history = []

# Helper Function
def segment_for_adding_to_context_history(role, comment):

    if role == "user":
        segment = {"role": "user", "content": comment}

    elif role == "assistant":
        segment = {"role": "assistant", "content": comment}

    elif role == "system":
        segment = {"role": "system", "content": comment}

    else:
        print("error segment_for_adding_to_context_history(role, comment)")
        print(role, comment)
        print("error")

    return segment

import re


# Helper Function
def set_translator__system_prompt(context_history, target_language):

    ################
    # System Prompt
    ################


    # set translation language and structure of output in system
    text_input = f"""
    You are an expert helpful {target_language} language translator bot that produces high
    quality professional translations. You translate writen UTF-8 language, not emojis or syntax not
    readable by a person.

    You always deliver your translation in the same simple standard format
    between a demiter of three pipes
    |||YOUR TRANSLATION HERE|||


    Your translation format is like this, with no other commentary needed:
    |||your translation here|||

    You only translate into {target_language}.
    Your translations are clear, accurate, helpful, honrable, brief, polite, and professional.
    Your do you best to tranlsate every leaf value field leaving nothing blank.
    Every final leaf values MUST be translated.

    You always double check your work and make sure the translation is
    excellent in the context of the whole body of translation.
    """

    # Remove duplicate spaces
    text_input = re.sub(r'\s+', ' ', text_input.strip())

    role = "system"

    context_history.append(segment_for_adding_to_context_history(role, text_input))

    # # inspection
    # print("set_translator__system_prompt -> ", context_history)

    return context_history


"""## Add 'user' request for translation"""


# Helper Function
def set_translate__user_prompt(context_history, target_language, original_data):

    ###########################
    # User Translation Request
    ###########################


    # set translation language and structure of output in system
    text_input = f"""
    The person we are trying to help needs a {target_language} language translation of a text string.

    Carefully translate the original text string into {target_language}.
    The original string is: {original_data}

    Double check your work and make sure the translation is
    accurate, brief, and polite.

    Produce just a {target_language} language translation identified
    by surrounding tripple pipes. |||your translation her|||

    For example "a happy cat" translated into French would be expressed as 
    |||your translation here|||

    You can do it!!
    """




    # Remove duplicate spaces
    text_input = re.sub(r'\s+', ' ', text_input.strip())

    role = "user"

    context_history.append(segment_for_adding_to_context_history(role, text_input))

    # # inspection
    # print("set_translate__user_prompt", context_history)

    return context_history


################
################
################
################
# Run & Testing
################
################
################
################

