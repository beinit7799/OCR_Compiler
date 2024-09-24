import black
import subprocess

def format_python_code(code):
    try:
        formatted_code = black.format_str(code, mode=black.Mode())
        return formatted_code
    except Exception as e:
        print(f"Error formatting python code: {e}")
        return None

def format_c_cpp_code(code,language):
    try:
        result = subprocess.run(
            ['clang-format'], 
            input=code.encode(), 
            capture_output=True, 
            text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error formatting {language} code: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error formatting {language} code: {e}")
        return None

def format_java_code(code):
    try:
        # Format Java code using google-java-format
        result = subprocess.run(
            ['java', '-jar', 'google-java-format.jar', '--aosp', '--'],
            input=code.encode(),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error formatting Java code: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception occurred while formatting Java code: {e}")
        return None

def format_javascript_code(code):
    try:
        result = subprocess.run(
            ['prettier', '--stdin-filepath', 'file.js'], 
            input=code.encode(), 
            capture_output=True, 
            text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error formatting JavaScript code: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error formatting JavaScript code: {e}")
        return None
    
def format_code(processed_text):
    if 'def' in processed_text or 'import' in processed_text:
        language = 'Python'
        formatted_code = format_python_code(processed_text)
    elif '#include' in processed_text and 'std::' in processed_text:
        language = 'C++'
        formatted_code = format_c_cpp_code(processed_text,language)
    elif '#include' in processed_text or 'int main' in processed_text:
        language = 'C'
        formatted_code = format_c_cpp_code(processed_text,language)
    elif 'class' in processed_text and 'public static void main' in processed_text:
        language = 'Java'
        formatted_code = format_java_code(processed_text)
    elif 'function' in processed_text or 'console.log' in processed_text:
        language = 'Js'
        formatted_code = format_javascript_code(processed_text)
    else:
        language = 'unknown'
        formatted_code = processed_text

    return formatted_code, language