import time

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class Metharme:
    def __init__(self, character):
        self.character = "<|system|>" + character
        self.tokenizer = AutoTokenizer.from_pretrained("TehVenom/Metharme-7b-Merged-Safetensors")
        # self.model = AutoModelForCausalLM.from_pretrained("TehVenom/Metharme-7b-Merged-Safetensors", torch_dtype=torch.float16, device_map='auto')
        self.model = AutoModelForCausalLM.from_pretrained("TehVenom/Metharme-13b-Merged", load_in_4bit=True,
                                                          bnb_4bit_use_double_quant=False,
                                                          bnb_4bit_compute_dtype=torch.float16, device_map='auto')

    def generate(self, question, retrieved=None, history=None, max_new_tokens=200, max_length=200, do_sample=True, temperature=0.95,
                 top_k=30, top_p=0.9,
                 repetition_penalty=1.08, num_return_sequences=1):
        st = time.time()

        prompt = ""
        if history is not None:
            prompt += history
        if retrieved is not None:
            prompt += "<|retrieved|>" + retrieved
        prompt += "<|user|>" + question + "<|model|>"

        prompt_tokens = self.tokenizer.encode(prompt, return_tensors="pt")
        if len(prompt_tokens[0]) > 1500:
            prompt = prompt[len(prompt) - 1500:]
            
        prompt = self.character + prompt

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        input_ids = input_ids.to(self.model.device)
        output_sequences = self.model.generate(
            input_ids=input_ids,
            # max_length=max_length,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_return_sequences,
        )
        tokens_len = len(output_sequences[0]) - len(input_ids[0])
        print('Tokens per second:', tokens_len / (time.time() - st))
        return [self.tokenizer.decode(output_sequence, skip_special_tokens=True) for output_sequence in
                output_sequences][0][len(prompt):]
