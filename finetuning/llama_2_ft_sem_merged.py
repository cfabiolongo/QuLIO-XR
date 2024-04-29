import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # or "0,1" for multiple GPUs

import pandas as pd
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, LlamaTokenizer
from random import randrange
import torch
import statistics

from evaluate import load
bertscore = load("bertscore")

model_name = f"../models/7B-chat"
adapters_name = f"../models/finetuned/llama-sem2_50ep"

# General parameters
temp = 0.6
max_new_tokens = 50
gpu = "cuda:0"

print(f"\nadapters_name: {adapters_name}\nTemperature: {temp}\n")

m = AutoModelForCausalLM.from_pretrained(
        model_name,
        # load_in_4bit=True,
        torch_dtype=torch.bfloat16,
        device_map=gpu
    )
model = PeftModel.from_pretrained(m, adapters_name)
model = model.merge_and_unload()
tokenizer = LlamaTokenizer.from_pretrained(model_name)

df = pd.read_excel('dataset/test_sem_ext2.xlsx')
df = df.fillna("")

response_column = df['value'].tolist()
instruction_column = df['sentence'].tolist()

df['context'] = df['place'].astype(str) + " " + df['time'].astype(str)

context_column = df['context'].tolist()

# Create datasets
dataset = [{'response': r, 'instruction': i, 'context': c} for r, i, c in zip(response_column, instruction_column, context_column)]

sample = dataset[randrange(len(dataset))]
print(f"Random sample: \n{sample}\n")

sub_prompt = "Use the Input below to create a sentence in expressive english, which could have been used to generate the Input logical form. Consider Context if not empty."

preds = []

match = 0
for i in range(len(dataset)):
    d = dataset[i]
    
    prompt = f"""### Context: {sample['context']}
    ### Instruction:
    {sub_prompt}
    ### Input:
    {d['response']}

    ### Response:
    """

    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids.cuda()
    
    outputs = model.generate(
        input_ids=input_ids,        
        max_new_tokens=max_new_tokens,
        do_sample=True,
        top_p=0.9,
        temperature=temp,
        pad_token_id=model.config.eos_token_id,  # Imposta pad_token_id su eos_token_id
        attention_mask=torch.ones_like(input_ids)  # Imposta l'attention mask
    )  
    
    gen_full = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(prompt):]
    gen = gen_full.split("#")[0]
    gen = gen.strip()
            
    print(f"\nPrompt {i}:\n{d['response']}")
    print(f"Context: {d['context']}")
    print(f"\nGenerated instruction:\n{gen}")
    print(f"Ground truth:\n{d['instruction']}")
    
    preds.append(gen)       
    
    if str(d['instruction']).lower() == gen.lower():
        match = match + 1
        print("---> MATCH <---")

print(f"\n#Match: {match}\n")

results = bertscore.compute(predictions=preds, references=instruction_column, model_type="distilbert-base-uncased")

# Estrai la precisione dai risultati
precision_scores = results['precision']
# Estrai la precisione dai risultati
recall_scores = results['recall']
# Estrai la precisione dai risultati
f1_scores = results['f1']

precision_media = statistics.mean(precision_scores)
print("Media della precisione:", precision_media)

recall_media = statistics.mean(recall_scores)
print("Media della recall:", recall_media)

f1_media = statistics.mean(f1_scores)
print("Media della f1:", f1_media)
