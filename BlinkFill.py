import re

# Sample patterns to start with 
NAME_REGEX = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'  # Simple full name pattern
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email pattern
PHONE_REGEX = r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b'  # US phone number

# Function to synthesize rules from examples
def synthesize_patterns(text: str, examples: dict):
    # Example: {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '123-456-7890'}
    name_pattern = NAME_REGEX
    email_pattern = EMAIL_REGEX
    phone_pattern = PHONE_REGEX
    
    # Add any adjustments from examples
    if 'name' in examples:
        # Synthesize a custom pattern based on the name example (e.g., specific formats)
        name_pattern = fr'\b{examples["name"].split()[0]}\s{examples["name"].split()[1]}\b'
    if 'email' in examples:
        # Similar for email, adjust the regex to capture specific email formats
        email_pattern = re.escape(examples['email'])
    if 'phone' in examples:
        # Adjust the phone regex based on the given example
        phone_pattern = re.escape(examples['phone'])
    
    return name_pattern, email_pattern, phone_pattern

# Function to extract information using synthesized patterns
def extract_info(text: str, name_pattern: str, email_pattern: str, phone_pattern: str):
    name = re.findall(name_pattern, text)
    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)
    
    return {
        "name": name[0] if name else None,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None
    }

# Main function
def synthesize_and_extract(text: str, examples: dict):
    # Synthesize patterns based on examples
    name_pattern, email_pattern, phone_pattern = synthesize_patterns(text, examples)
    
    # Extract information from the text
    return extract_info(text, name_pattern, email_pattern, phone_pattern)


# Example usage
input_text = "Contact John Doe via email john.doe@example.com or phone number (123) 456-7890."
examples = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "(123) 456-7890"
}

# Synthesizing and extracting
extracted_info = synthesize_and_extract(input_text, examples)
print(extracted_info)
