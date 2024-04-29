Finetuning Multi-task LLama2 chat

---------------------------------------------------------

Fine-tuning Llama-2-7B-chat on 900 couples (logical form, sentence), from dataset/train_sem_ext2.xlsx:

llama_2_ft_lora_sem.py

##################

Inference (MATCHES and BERT-Score) with 100 unseen (logical form, sentence) from dataset/test_sem_ext2.xlsx:

llama_2_ft_bertscore_sem.py

##################

Inference (MATCHES and BERT-Score) from dataset/test_sem_ext2.xlsx, with weights merged with base model:

llama_2_ft_sem_merged.py

##################

Fine-tuning Llama-2-7B-chat on 1000 Open qa couples (answer, response), from dolly dataset:

llama_2_ft_lora_dolly.py

##################

Inference (MATCHES and BERT-Score) with 100 known couples (answer, response), from dolly dataset:

llama_2_ft_bertscore_dolly.py.py

##################

Inference (MATCHES and BERT-Score) with 100 known couples (answer, response) from dolly dataset, with weights merged with base model:

llama_2_ft_bertscore_dolly_merged.py

##################

Inference (MATCHES and BERT-Score) with 100 unseen (logical form, sentence) from dataset/test_sem_ext2.xlsx and with 100 known couples (answer, response) from dolly dataset, with combination (svd|linear|cat) of two adapters:

llama_2_ft_sem_dolly_pipe.py