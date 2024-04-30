from random import randrange
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments

# General parameters
epoche = 50
lr = 2e-3
path_model = f"../models/finetuned/llama-sem2_{epoche}ep"

print(f"\nEpoche: {epoche}\nLearning rate: {lr}\ndevice: {torch.cuda.current_device()}\n")

df = pd.read_excel('dataset/train_sem_ext2.xlsx')

response_column = df['value'].tolist()
instruction_column = df['sentence'].tolist()

# Create datasets
dataset = [{'response': r, 'instruction': i} for r, i in zip(response_column, instruction_column)]

sub_prompt = "Use the Input below to create a sentence in expressive english, which could have been used to generate the Input logical form."


def format_instruction(sample):
	return f"""### Instruction:
{sub_prompt}
### Input:
{sample['response']}

### Response:
{sample['instruction']}
"""

print(format_instruction(dataset[randrange(len(dataset))]))


""" python -c "import torch; assert torch.cuda.get_device_capability()[0] >= 8, 'Hardware not supported for Flash Attention'"
pip install ninja packaging
MAX_JOBS=4 pip install flash-attn --no-build-isolation
 """


# Hugging Face model id
# model_id = "../models/7B"  # non-gated
model_id = "../models/7B-chat"  # non-gated
# model_id = "meta-llama/Llama-2-7b-hf" # gated

# BitsAndBytesConfig int-4 config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
)

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    use_cache=False,        
)
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model

# LoRA config based on QLoRA paper
peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=64,
        bias="none",
        task_type="CAUSAL_LM",
)

# prepare model for training
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)

use_flash_attention = False

args = TrainingArguments(
    output_dir=path_model,
    num_train_epochs=epoche,
    per_device_train_batch_size=6 if use_flash_attention else 4,
    gradient_accumulation_steps=2,
    gradient_checkpointing=True,
    optim="paged_adamw_32bit",
    logging_steps=10,
    save_strategy="epoch",
    learning_rate=lr,
    bf16=True,
    tf32=True,
    max_grad_norm=0.3,
    warmup_ratio=0.03,
    lr_scheduler_type="constant",
    disable_tqdm= False # disable tqdm since with packing values are in correct
)


from trl import SFTTrainer

max_seq_length = 2048 # max sequence length for model and packing of the dataset

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    packing=True,
    formatting_func=format_instruction,
    args=args,  
)

# train
trainer.train() # there will not be a progress bar since tqdm is disabled

# save model
trainer.save_model(path_model)

print("\nFinetuning complete.")
print(f"\nPath model: {path_model}\n")

##### merging adapter weights into the base model #####

#from peft import AutoPeftModelForCausalLM

#model = AutoPeftModelForCausalLM.from_pretrained(
#    args.output_dir,
#    low_cpu_mem_usage=True,
#)

# Merge LoRA and base model
#merged_model = model.merge_and_unload()

# Save the merged model
#merged_model.save_pretrained(path_model_merged, safe_serialization=True)
#tokenizer.save_pretrained(path_model_merged)

# push merged model to the hub
# merged_model.push_to_hub("user/repo")
# tokenizer.push_to_hub("user/repo")
