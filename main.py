"""
Provides a simple Python API to generate prompts for AI image generation
"""
import os
import re
import logging
import json
import uuid
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# default config
save_to_file = False
default_args = {
    'temperature': {
        'type': float,
        'default': 0.9,
        'range': [0, 1]
    },
    'top_k': {
        'type': int,
        'default': 8,
        'range': [1, 200]
    },
    'max_length': {
        'type': int,
        'default': 80,
        'range': [1, 200]
    },
    'repetition_penalty': {
        'type': float,
        'default': 1.2,
        'range': [0, 10]
    },
    'num_return_sequences': {
        'type': int,
        'default': 5,
        'range': [1, 5]
    },
}

app = Flask("PromptGeneratorAPI")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('prompt', required=True)

# optional arguments
for arg, def_arg in default_args.items():
    parser.add_argument(arg, type=def_arg['type'], required=False)

# limit the amount of requests per user
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]
)

class PromptGenerator(Resource):
    """Prompt Generator Class

    Args:
        Resource Resource: Flask restful resource
    """

    def validate_args(self, args):
        """Validate range, set dynamic variables value

        Args:
            args dict: Arguments provided in the request
        """
        for arg, def_arg in default_args.items():
            if arg in args and args[arg]:
                if def_arg['range'][0] < args[arg] > def_arg['range'][1]:
                    abort(500,
                          message=f"{arg} out of range. Min {def_arg['range'][0]}, Max {def_arg['range'][1]}")
                globals()[arg] = args[arg]
            else:
                globals()[arg] = def_arg['default']

    def get_blacklist(self):
        """Check and load blacklist

        Returns:
            list: List of terms from the blacklist dictionary
        """
        blacklist_filename = 'blacklist.txt'
        blacklist = []
        if not os.path.exists(blacklist_filename):
            logging.warning("Blacklist file missing: %s", blacklist_filename)
            return blacklist
        with open(blacklist_filename, 'r') as f:
            for line in f:
                blacklist.append(line)

            return blacklist

    def post(self):
        """Post method

        Returns:
            string: JSON list with the generated prompts
        """
        args = parser.parse_args()
        self.validate_args(args)

        prompt = args['prompt']
        request_uuid = uuid.uuid4()
        try:
            # build model
            tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            model = GPT2LMHeadModel.from_pretrained('FredZhang7/distilgpt2-stable-diffusion-v2')
        except Exception as e:
            logging.error(
                "Exception encountered while attempting to install tokenizer: %s", e)
            abort(500, message="There was an error processing your request")
        try:
            # generate prompt
            logging.debug("Generate new prompt from: \"%s\"", prompt)
            input_ids = tokenizer(prompt, return_tensors='pt').input_ids
            output = model.generate(input_ids, do_sample=True, temperature=temperature,
                                    top_k=top_k, max_length=max_length,
                                    num_return_sequences=num_return_sequences,
                                    repetition_penalty=repetition_penalty,
                                    penalty_alpha=0.6, no_repeat_ngram_size=1,
                                    early_stopping=True)
            prompt_output = []
            blacklist = self.get_blacklist()
            for count, value in enumerate(output):
                prompt_output.append(
                    tokenizer.decode(value, skip_special_tokens=True)
                )
                for term in blacklist:
                    prompt_output[count] = re.sub(
                        term, "", prompt_output[count], flags=re.IGNORECASE)

            # save results to file
            if save_to_file:
                with open(f"{request_uuid}.json", 'w') as f:
                    json.dump(prompt_output, f)

            return prompt_output

        except Exception as e:
            logging.error(
                "Exception encountered while attempting to generate prompt: %s", e)
            abort(500, message="There was an error processing your request")


api.add_resource(PromptGenerator, '/generate')

if __name__ == '__main__':
    app.run(debug=False)
