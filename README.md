# Prompt Generator API

A simple prompt generator API for Stable Diffusion / Midjourney / Dall-e based in Python.

The API takes an initial prompt of a few words, and generates an extended and detailed prompt.

Based on the implementation of the [FredZhang7/distilgpt2-stable-diffusion-v2](https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2) model.

**Contributions are welcome :)**
## Example

**Initial prompt**

> cat with sunglasses

**Results of this prompt using Stable Diffusion v1.5**

![rdm-figure](img/simple-prompt.png)

**Generated prompt using this API**
> cat with sunglasses, in the style of studio ghibli painting. cinematic lighting from right side on image and sharp focus by jean - baptiste monge! octane render redshift unreal engine 5 lumen global illumination ray tracing hdr arstation pixar disney tone mapping shiny reflectionsordan grimmer 4 k 8 lois van baal enki bilan ilya

**Results of this prompt using Stable Diffusion v1.5**

![rdm-figure](img/generated-prompt.png)

## Installation and usage

The API currently provides a POST endpoint to generate the prompt, configured to run at **/generate**

1. Install the dependencies:
```sh
pip install --upgrade torch transformers flask flask_restful flask_limiter
```
2. Clone the code of this repository:
```sh
git clone https://github.com/jordip/prompt-generator-api.git
```
3. Run main.py from the root path:
```sh
python3 main.py
```
4. Send a POST request to your instance of the API:
```sh
curl http://127.0.0.1:5000/generate -H "Content-Type: application/json" -d '{"prompt":"cat with sunglasses"}' -X POST
```
### Required arguments

- prompt
  - The beginning of the prompt.

### Optional arguments

- temperature
  - A higher temperature will produce more diverse results, but with a higher risk of less coherent text. Default: 0.9
- top_k
  - The number of tokens to sample from at each step. Default: 80
- max_length
  - The maximum number of tokens for the output of the model. Default: 80
- repetition_penalty
  - The penalty value for each repetition of a token. Default: 1.2
- num_return_sequences
  - The number of results to generate. Default: 5
## Features

### Blacklist

blacklist.txt contains a list of terms to be replaced from the returned prompt. One term per line.

### Usage limits

The API is configured to limit the amount of requests received per minute by a single user.