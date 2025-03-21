import openai

# Load API key from file
with open("OpenAI_API_Key.txt", "r") as f:
    OPENAI_API_KEY = f.read().strip()

openai.api_key = OPENAI_API_KEY
client = openai.OpenAI(api_key = OPENAI_API_KEY)
# Your Assistant ID
ASSISTANT_ID = "asst_eGaU51vpRsSfGvMGGjbd7KUb"

def upload_file(file_path):
    """Uploads a file to OpenAI and returns the file ID."""
    with open(file_path, "rb") as file:
        response = client.files.create(
            file=file,
            purpose="assistants"
        )
    return response.id  # Use `.id` instead of `["id"]`


def attach_file_to_assistant(assistant_id, file_id):
    """Attaches a file to an assistant."""
    response = client.beta.assistants.files.create(
        assistant_id=assistant_id,
        file_id=file_id
    )
    return response


if __name__ == "__main__":
    file_path = "sat_phone.pdf"  # Change this to your actual file

    # Upload the file
    file_id = upload_file(file_path)
    print(f"Uploaded File ID: {file_id}")

    # Attach the file to the assistant
    update_response = attach_file_to_assistant(ASSISTANT_ID, file_id)
    print(f"File {file_id} attached to Assistant {ASSISTANT_ID}")
