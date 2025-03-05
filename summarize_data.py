import openai

with open('OpenAI_API_Key.txt', 'r') as file:
    openai_api_key = file.read().strip()

def summarize_text(text):
    """Use GPT-3.5 to summarize a line to a maximum of 20 words."""
    try:
        # Call the OpenAI API to summarize the line with the correct endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",  # Specify the chat model
            messages=[
                {"role": "user", "content": f"Summarize the following line into 20 words or less:\n{text}"}
            ],
            max_tokens=60,  # Adjust token limit as needed
            temperature=0.5,
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing line: {e}")
        return text  # Return the original line in case of error

def process_file(input_filename, output_filename):
    """Read the input file, process each line, and write the summarized text to the output file."""
    with open(input_filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in lines:
            # Clean up the line, strip leading/trailing whitespace
            cleaned_line = line.strip()
            if cleaned_line:
                # Summarize the line using GPT-3.5
                summarized_line = summarize_text(cleaned_line)
                # Write the summarized line to the output file
                outfile.write(summarized_line + "\n")

if __name__ == "__main__":
    input_file = "cleaned_user_requests.txt"
    output_file = "summarized_user_requests.txt"
    
    process_file(input_file, output_file)
    print(f"Summarization complete. Output saved to {output_file}")
