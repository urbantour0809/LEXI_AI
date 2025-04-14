import os
import json
import chromadb
import torch
from transformers import AutoModel, AutoTokenizer

# 데이터 경로 설정
JSON_PATH = os.path.abspath("../dataset/판례목록.json")

# GPU 설정
device = "cuda" if torch.cuda.is_available() else "cpu"

# ChromaDB 설정
CHROMA_DB_PATH = "../dataset/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
legal_precedents_collection = chroma_client.get_or_create_collection(name="legal_precedents")

# Fine-tuned `legal-bert-base` 모델 로드
MODEL_PATH = "../ft_legal_bert/checkpoint-1185"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
embedding_model = AutoModel.from_pretrained(MODEL_PATH).to(device)

def embed_text(text):
    #Fine-tuned 모델을 사용하여 문장을 벡터화 (GPU 활용)
    if not isinstance(text, str) or not text.strip():
        return None  # 빈 문자열 또는 None 값 방지

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512).to(device)
    
    with torch.no_grad():
        outputs = embedding_model(**inputs)
    
    return outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]  # 1차원 리스트 변환

def process_precedents():
    # 판례 목록 데이터 처리 및 임베딩
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        precedents_data = json.load(f)

    for data in precedents_data:
        case_number = data.get("사건번호", "").strip()
        title = data.get("제목", "").strip()
        ruling = data.get("판시사항", "").strip()

        # 데이터 유효성 검사
        if not case_number or not title or not ruling:
            print(f"데이터 부족으로 건너뜀: 사건번호 {case_number}")
            continue

        # 판례 데이터 포맷 구성
        text_data = f"""
        📌 사건번호: {case_number}
        📌 제목: {title}
        📌 판시사항:
        {ruling}
        """.strip()

        # 벡터화 수행
        embedding = embed_text(text_data)
        if embedding is None:
            print(f"! 임베딩 실패로 건너뜀: 사건번호 {case_number}")
            continue

        # 기존 데이터 중복 확인
        existing_data = legal_precedents_collection.get(ids=[case_number])
        if existing_data and existing_data["ids"]:
            print(f"! 기존 데이터 스킵: 사건번호 {case_number}")
            continue

        # ChromaDB에 저장
        print(f"판례 추가 완료: 사건번호 {case_number}")
        legal_precedents_collection.add(
            ids=[case_number],
            embeddings=[embedding],
            metadatas=[{
                "case_number": case_number,  # 사건번호 저장
                "title": title,  # 제목 저장
                "text": text_data  # 전체 텍스트 저장
            }]
        )

if __name__ == "__main__":
    print("판례 목록 데이터 벡터화 시작...")
    process_precedents()
    print("모든 판례 목록 데이터 벡터화 완료!")
