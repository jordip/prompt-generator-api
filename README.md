# Prompt Generator API
A simple prompt generator API for Stable Diffusion / Midjourney / Dall-e based in Python.

Based on the implementation of the [FredZhang7/distilgpt2-stable-diffusion-v2](https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2) model.

**Work in progress!** Contributions are welcomed :)
## Requirements
The API is based in flask and uses transformers package to interact with the model.

To install required libraries run:

        pip install --upgrade transformers flask flask_restful

## Usage
The API currently provides a POST endpoint to generate the prompt, configured to run at **/generate**

Run main.py and send POST requests with the following arguments in JSON.

### Required arguments
- prompt
  - The beginning of the prompt.

### Optional arguments
- temperature
  - A higher temperature will produce more diverse results, but with a higher risk of less coherent text
- top_k
  - The number of tokens to sample from at each step
- max_length
  - The maximum number of tokens for the output of the model
- repetition_penalty
  - The penalty value for each repetition of a token
- num_return_sequences
  - The number of results to generate

### Blacklist
blacklist.txt contains a list of terms to be replaced from the returned prompt. One term per line.

## TODO
1. ~~Parametrize default arguments~~
2. ~~Add blacklist filtering~~
3. Smart cropping
4. Throttling
5. Standards