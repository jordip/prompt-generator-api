# Prompt Generator API
A simple prompt generator API for Stable Diffusion / Midjourney / Dall-e based in Python.

Loosely based in the implementation of the [FredZhang7/distilgpt2-stable-diffusion-v2](https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2) by the Automatic1111 extension script by [imrayya](https://github.com/imrayya/stable-diffusion-webui-Prompt_Generator).

**Work in progress!** Contributions are welcomed :)
## Installation
1. Install required libraries.

        pip install gradio transformers flask flask_restful

2. Run main.py

        python3 main.py

3. Send the input prompt URL-encoded to http://yourserver.path/generate/

## TODO
1. Parametrize default values
2. Add blacklist filtering
3. Smart cropping
4. Throttling
5. Standards