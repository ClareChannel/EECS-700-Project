import re

class BlinkFill:
    def __init__(self, examples):
        self.examples = examples
        self.patterns = self.learn_patterns(examples)
        
    def learn_patterns(self, examples):
        patterns = []
        for input_str, output_str in examples:
            #generate a regex pattern for each example
            input_parts = self.extract_parts(input_str)
            output_pattern = self.map_output(input_parts, output_str)
            patterns.append((input_parts, output_pattern))
        return patterns
    
    def extract_parts(self, string):
        #split the string by spaces, commas, etc. (can be generalized to more cases)
        return re.split(r'\s+', string)
    
    def map_output(self, input_parts, output_str):
        #map the input parts to output
        output_parts = re.split(r'\s+', output_str)
        pattern = []
        
        #check how the input parts are reordered in the output
        for part in output_parts:
            if part in input_parts:
                pattern.append(('literal', input_parts.index(part)))
            else:
                pattern.append(('static', part))
        return pattern

    def apply_pattern(self, input_str, pattern):
        input_parts = self.extract_parts(input_str)
        output_str = []
        for p_type, value in pattern:
            if p_type == 'literal':
                output_str.append(input_parts[value])
            elif p_type == 'static':
                output_str.append(value)
        return ' '.join(output_str)
    
    def transform(self, new_input):
        for input_parts, pattern in self.patterns:
            return self.apply_pattern(new_input, pattern)

#examples
examples = [
    ("John Johnson", "Johnson, John"),
    ("Jane Smith", "Smith, Jane")
]

blinkfill = BlinkFill(examples)
new_input = "Brooke John"
print(blinkfill.transform(new_input))
