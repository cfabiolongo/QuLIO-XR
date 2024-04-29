import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # or "0,1" for multiple GPUs

import pandas as pd
from transformers import AutoTokenizer, LlamaTokenizer
from random import randrange

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

import statistics
from evaluate import load
bertscore = load("bertscore")
from datasets import load_dataset, Dataset, concatenate_datasets


adapters_name1 = f"../models/finetuned/llama-sem3_50ep"
adapters_name2 = f"../models/finetuned/llama-dolly_qa_100ep"

adapters_name_unified = f"../models/finetuned/llama-sem-dollywest"

temp = 0.6
comb_type = "linear"
w1 = 0.7  # fol
w2 = 0.3  # dolly

print("temp: ", temp)
print("combination type: ", comb_type)
print("weights: "+str(w1)+", "+str(w2))

#################################################################

base_model = "../models/7B-chat"
compute_dtype = getattr(torch, "float16")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(
        base_model, device_map={"": 0},  quantization_config=bnb_config
)
tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=True)

model = PeftModel.from_pretrained(model, adapters_name1, adapter_name="fol")
model.load_adapter(adapters_name2, adapter_name="dollywest")

model.add_weighted_adapter(["fol", "dollywest"], [w1,w2], combination_type=comb_type, adapter_name="dollywest_fol")

model.delete_adapter("fol")
model.delete_adapter("dollywest")
model.save_pretrained("../models/finetuned")

model = PeftModel.from_pretrained(model, "../models/finetuned/dollywest_fol")

# https://huggingface.co/docs/peft/package_reference/lora

# adapters (list) — List of adapter names to be merged.
# weights (list) — List of weights for each adapter.
# adapter_name (str) — Name of the new adapter.
# combination_type (str) — Type of merging. Can be one of [svd, linear, cat]. When using the cat combination_type you should be aware that rank of the resulting adapter will be equal to the sum of all adapters ranks. So it’s possible that the mixed adapter may become too big and result in OOM errors.
# svd_rank (int, optional) — Rank of output adapter for svd. If None provided, will use max rank of merging adapters.
# svd_clamp (float, optional) — A quantile threshold for clamping SVD decomposition output. If None is provided, do not perform clamping. Defaults to None.
# svd_full_matrices (bool, optional) — Controls whether to compute the full or reduced SVD, and consequently, the shape of the returned tensors U and Vh. Defaults to True.
# svd_driver (str, optional) — Name of the cuSOLVER method to be used. This keyword argument only works when merging on CUDA. Can be one of [None, gesvd, gesvdj, gesvda]. For more info please refer to torch.linalg.svd documentation. Defaults to None.

######################################################### 

max_new_tokens = 50

df = pd.read_excel('dataset/test_sem_ext2.xlsx')

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
            
    print(f"\nPrompt {i} :\n{d['response']}\n")
    print(f"Generated instruction:\n{gen}")
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



def attesa_input():
    # Stampa un messaggio
    print("\nPremi un tasto per continuare...")
    
    # Attendi l'input dell'utente
    input()

# Chiamata alla funzione di attesa
attesa_input()

# Il codice qui sotto verrà eseguito solo dopo che l'utente ha premuto un tasto
print("Esecuzione continua dopo l'input dell'utente...........")


# QA
#################################################################

print("\n\n########################################################\n\n")
max_new_tokens = 512

# Load dataset
dataset = load_dataset("databricks/databricks-dolly-15k", split="train")

# Filtra il dataset
filtered_dataset = dataset.filter(lambda example: example['category'] == "open_qa" and len(example['response']) < 100)

dataset_dolly = filtered_dataset.select(range(100))
# Stampa le prime 5 righe del dataset filtrato

# Colonel West dataset
df2 = pd.read_excel('dataset/west2.xlsx')

# Create datasets fol
dataset_west = Dataset.from_pandas(df2)
    
# Concatena i due dataset
dataset = concatenate_datasets([dataset_dolly, dataset_west])
dataset = dataset_dolly

sub_prompt="You are Joshua, an AI Assistant. Generate a response to the question given in Input."


preds = []
match = 0

for i in range(len(dataset)):

    if i > 99:
       print(f"\n------WEST------- Record #{i}:\n")
    else:
       print(f"\n----------------- Record #{i}:\n")
    
    d = dataset[i]   
              
    prompt = f"""### Instruction:
    {sub_prompt}    
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
            
    print(f"\nPrompt [{d['category']}]: {d['instruction']}\n")         
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
