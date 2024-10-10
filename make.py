from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset

# 사용자 정의 데이터셋 클래스
class TextDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {
            'input_ids': self.encodings['input_ids'][idx],
            'attention_mask': self.encodings['attention_mask'][idx],
            'labels': self.encodings['input_ids'][idx],  # 모델의 labels는 일반적으로 input_ids와 동일함
        }

    def __len__(self):
        return len(self.encodings['input_ids'])

# 텍스트 파일 로드
def load_text_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        texts = f.readlines()
    return texts

# 토크나이저 및 모델 로드
def prepare_model():
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
    
    # 패딩 토큰 설정
    tokenizer.pad_token = tokenizer.eos_token  # eos_token을 pad_token으로 사용

    return model, tokenizer

# 텍스트 데이터 토크나이징
def tokenize_texts(tokenizer, texts):
    return tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

# 학습 설정 및 실행
def fine_tune_model(model, tokenized_texts):
    # Dataset 생성
    dataset = TextDataset(tokenized_texts)

    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=2,
        num_train_epochs=3,
        logging_dir="./logs"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    trainer.train()

if __name__ == "__main__":
    # 1. 데이터 로드
    texts = load_text_data('combined_texts.txt')

    # 2. 모델 준비 및 토크나이저 적용
    model, tokenizer = prepare_model()
    tokenized_texts = tokenize_texts(tokenizer, texts)

    # 3. 모델 파인 튜닝
    fine_tune_model(model, tokenized_texts)