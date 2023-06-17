# Unicorn

Unicorn is a semantic-search enhanced Telegram chatbot. It uses OCR, pre-trained language models and FAISS 
to retrieve relevant passes from documents and generate answers to questions.

## Installation

Clone the Unicorn repository:

```git clone https://github.com/marcodsn/unicorn.git```

Install the required packages:

```pip install -r requirements.txt```

## Usage

Unicorn can be used to answer questions using factual data retrieved from PDF documents. It can also be used to answer
questions without using any documents, but the answers will be less accurate.

To start the bot, simply run:

```python main.py token```

Where `token` is the Telegram bot token. You can get a token by talking to @BotFather on Telegram.

## FAQ

- **Why is Unicorn so slow?** Currently, the default LLM used is the Metharme-13b model by PygmalionAI 
  (merged by TehVenom) which has to run in 4bit precision to fit on the average consumer GPU. If you prefer speed to accuracy, you
  can change the LLM model to a smaller one manually (check models/LLMs/metharme.py).
- **Why is Unicorn inaccurate?** Unicorn is still in its early stages of development and for this reason it is not flawless.
  If you find any bugs, please report them in the Issues section of this repository.
- **What are the VRAM requirements for Unicorn?** At the moment, Unicorn requires just over 8GB of VRAM to run the
  embedding model and the LLM model to generate answers. This can be reduced by changing the LLM model to a smaller one
  manually (in models/LLMs). Document analysis is also VRAM-intensive at the moment, so you will need more VRAM if you plan
  to use that feature.
- **Does Unicorn support multiple languages?** Unicorn works best with English, but it can be used with other languages
  as well (although the results will be less accurate).
- **Can I modify Unicorn's personality?** Yes, you can! You can change the persona by modifying the `character` variable
  in `main.py`.

## Roadmap

- [x] Move to a better OCR model
- [ ] Add support for multiple languages
- [ ] Add support for more document types
- [ ] Add support to use multiple documents at once
- [ ] Allow different characters (personas) for every user
- [ ] Add support for a default, always-loaded document (e.g. with information about the company/organization)
- [ ] Add more easily accessible settings

... And more to come!

## License

Unicorn is licensed under the MIT License. See the LICENSE file for more information.