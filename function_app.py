import azure.functions as func
import logging
import sys
import importlib.util

# Initialize the function app with anonymous HTTP authorization level
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

    # Path to the compiled .pyc file
    
# Define the HTTP trigger function
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if a file is included in the request
    file = req.files.get('file')
    pyc_file = 'hello.cpython-311.pyc'

    # Load the .pyc file
    spec = importlib.util.spec_from_file_location('my_module', pyc_file)
    my_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_module)

    if file:
        # Extract file details
        file_name = file.filename
        content_type = file.content_type
        file_size = len(file.read())
        result = my_module.greet(file_name)
    
        
        # Create response with file details
        response_message = (
            f"File uploaded successfully.\n"
            f"File Name: {file_name}\n"
            f"Content Type: {content_type}\n"
            f"File Size: {file_size} bytes\n"
            f"greet:{result}"
        )
        return func.HttpResponse(response_message, status_code=200)
    else:
        # If no file is provided, inform the user
        return func.HttpResponse(
            "No file was uploaded. Please upload a file to get its details.",
            status_code=400
        )
