import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # or "0,1" for multiple GPUs

import pandas as pd
import torch
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
from random import randrange
import torch
import statistics

from evaluate import load
bertscore = load("bertscore")

# General parameters
output_dir = "../models/finetuned/llama-sem3_50ep" 
temp = 0.6
max_new_tokens = 50
gpu = "cuda:0"

print(f"\nModel: {output_dir}\nTemperature: {temp}\n")

# load base LLM model and tokenizer
model = AutoPeftModelForCausalLM.from_pretrained(
    output_dir,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,    
    load_in_4bit=True,
    device_map=gpu,        
)
tokenizer = AutoTokenizer.from_pretrained(output_dir)

df = pd.read_excel('dataset/test_sem_ext2.xlsx')
df = df.fillna("")

response_column = df['value'].tolist()
instruction_column = df['sentence'].tolist()

# Create datasets
dataset = [{'response': r, 'instruction': i} for r, i in zip(response_column, instruction_column)]

sample = dataset[randrange(len(dataset))]
print(f"Random sample: \n{sample}\n")

sub_prompt = "Use the Input below to create a sentence in expressive english, which could have been used to generate the Input logical form."

preds = []

match = 0
for i in range(len(dataset)):
    d = dataset[i]
    
    prompt = f"""### Instruction:
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
