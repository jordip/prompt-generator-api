from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import logging
import json
import uuid

# default config
save_to_file = False
default_args = {
    'temperature': {
        'default': 0.9,
        'range': [0,1]
    },
    'top_k': {
        'default': 8,
        'range': [1, 200]
    },
    'max_length': {
        'default': 80,
        'range': [1, 200]
    },
    'repetition_penalty': {
        'default': 1.2,
        'range': [0, 10]
    },
    'num_return_sequences': {
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
    parser.add_argument(arg, type=float, required=False)
class PromptGenerator(Resource):

    # validate range, set value
    def validateArgs(self, args):
        for arg, def_arg in default_args.items():
            if arg in args and args[arg]:
                if def_arg['range'][0] < args[arg] > def_arg['range'][1]:
                    abort(500, message=f"{arg} out of range. Min {def_arg['range'][0]}, Max {def_arg['range'][1]}")
                globals()[arg] = args[arg]
            else:
                globals()[arg] = def_arg['default']

    # post method
    def post(self):
        args = parser.parse_args()
        self.validateArgs(args)

        prompt = args['prompt']
        request_uuid = uuid.uuid4()
        try:
            # build model
            tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            model = GPT2LMHeadModel.from_pretrained('FredZhang7/distilgpt2-stable-diffusion-v2')
        except Exception as e:
            logging.error(f"Exception encountered while attempting to install tokenizer")
            abort(500, message=f"There was an error processing your request")
        try:
            # generate prompt
            logging.debug(f"Generate new prompt from: \"{prompt}\"")
            input_ids = tokenizer(prompt, return_tensors='pt').input_ids
            output = model.generate(input_ids, do_sample=True, temperature=temperature,
                                    top_k=top_k, max_length=max_length,
                                    num_return_sequences=num_return_sequences,
                                    repetition_penalty=repetition_penalty,
                                    penalty_alpha=0.6, no_repeat_ngram_size=1,
                                    early_stopping=True)
            tempString = []
            for i in range(len(output)):
                tempString.append(
                    tokenizer.decode(output[i], skip_special_tokens=True)
                )

            # save results to file
            if save_to_file:
                with open(f"{request_uuid}.json", 'w') as f:
                    json.dump(tempString, f)

            return tempString

        except Exception as e:
            logging.error(
                f"Exception encountered while attempting to generate prompt: {e}")
            abort(500, message=f"There was an error processing your request")


api.add_resource(PromptGenerator, '/generate')

if __name__ == '__main__':
    # app.debug = True
    app.run()