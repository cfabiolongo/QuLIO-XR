import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # or "0,1" for multiple GPUs

import torch
from peft import PeftModel    
from transformers import AutoModelForCausalLM, LlamaTokenizer
import pandas as pd
from datasets import load_dataset

import statistics

from evaluate import load
bertscore = load("bertscore")

model_name = f"../models/7B-chat"
adapters_name = f"../models/finetuned/llama-dolly_qa_100ep"

temp = 0.6
max_new_tokens = 20
gpu = "cuda:0"

df = pd.read_excel('dataset/test_lkb3_gnd.xlsx')

print(f"Starting to load the model {model_name} into memory")
print("temp: ",temp)

# Impostazione del dispositivo di calcolo (CPU o GPU)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

m = AutoModelForCausalLM.from_pretrained(
        model_name,
        # load_in_4bit=True,
        torch_dtype=torch.bfloat16,
        device_map=gpu
    )
model = PeftModel.from_pretrained(m, adapters_name)
model = model.merge_and_unload()
tokenizer = LlamaTokenizer.from_pretrained(model_name)

# Load dataset
dataset = load_dataset("databricks/databricks-dolly-15k", split="train")

# Filtra il dataset
filtered_dataset = dataset.filter(lambda example: example['category'] == "open_qa" and len(example["response"]) <= 100)

dataset = filtered_dataset.select(range(100))

sub_prompt="You are Joshua, an AI Assistant. Generate a response to the question given in Input."

preds = []
match = 0

for i in range(len(dataset)):

    print(f"\n---------------- Record #{i}:\n")
    
    d = dataset[i]   
              
    prompt = f"""### Instruction:
    {sub_prompt}
    ### Context: {d['context']}
    ### Input:
    {d['instruction']}

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
            
    print(f"\nPrompt: {d['instruction']}\n")
    print(f"Context: {d['context']}\n")        
    print(f"Generated instruction:\n{gen}")
    print(f"Ground truth:\n{d['response']}")

    preds.append(gen)       
    
    if str(d['response']).lower() == gen.lower():
        match = match + 1
        print("---> MATCH <---")

print(f"\n#Match: {match}\n")

results = bertscore.compute(predictions=preds, references=dataset['response'], model_type="distilbert-base-uncased")

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

