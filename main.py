from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import gradio as gr
import logging

app = Flask("PromptGeneratorAPI")
api = Api(app)

# TODO parametrize the following
# default config
temperature = 0.9
top_k = 8
max_length = 80
repetition_penalty = 1.2
num_return = 5

class PromptGenerator(Resource):
    def get(self, input_prompt):
        try:
            tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            model = GPT2LMHeadModel.from_pretrained('FredZhang7/distilgpt2-stable-diffusion-v2')
        except Exception as e:
            logging.error(f"Exception encountered while attempting to install tokenizer")
            return [], 500
        try:
            logging.debug(f"Generate new prompt from: \"{input_prompt}\"")
            input_ids = tokenizer(input_prompt, return_tensors='pt').input_ids
            output = model.generate(input_ids, do_sample=True, temperature=temperature,
                                    top_k=top_k, max_length=max_length,
                                    num_return_sequences=num_return,
                                    repetition_penalty=repetition_penalty,
                                    penalty_alpha=0.6, no_repeat_ngram_size=1,
                                    early_stopping=True)
            logging.debug("Generation complete!")
            tempString = []
            for i in range(len(output)):
                tempString.append(
                    tokenizer.decode(output[i], skip_special_tokens=True)
                )

            return tempString

        except Exception as e:
            logging.error(
                f"Exception encountered while attempting to generate prompt: {e}")
            return [], 500

api.add_resource(PromptGenerator, '/generate/<input_prompt>')

if __name__ == '__main__':
    app.run()