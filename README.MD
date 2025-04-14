<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-💨-brightgreen?logo=fastapi" />
  <img src="https://img.shields.io/badge/EXAONE-3.5-informational?logo=deeplearning" />
  <img src="https://img.shields.io/badge/ChromaDB-Search-orange" />
</p>

# ⚖️ LEXI Backend – 법률 질문 & 계약서 생성기 (EXAONE 기반)

> 한국어 법률 질문 응답부터 자동 계약서 생성까지, EXAONE 3.5 기반 FastAPI 백엔드

---

## 🌟 왜 EXAONE 3.5?

- ✅ **한국어 특화 모델**: 한국어 법률/판례에 최적화된 EXAONE 3.5 사용
- ✅ **자연어 이해력 우수**: 복잡한 문장 구조도 안정적으로 처리
- ✅ **LLM + RAG 조합**: 판례 및 임베딩 검색 기반의 정확한 응답

---

## ⚙️ 양자화 설정 코드 (answer.py & doc_create.py)

```python
# ✅ 4비트 양자화 설정
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,                # 4비트 양자화 사용
    bnb_4bit_compute_dtype=torch.float16,  # 연산 시 float16 사용
    bnb_4bit_quant_type="nf4",       # NF4 양자화 타입 사용
    bnb_4bit_use_double_quant=True   # 이중 양자화로 메모리 추가 절약
)
```

> 🚀 VRAM 8GB에서도 EXAONE 구동이 가능하도록 설정된 초경량 양자화 방식입니다.

---

## 🧠 주요 AI 로직 코드 예시

### 🔍 ChromaDB 판례 검색
```python
results = collection.query(query_texts=[query], n_results=3)
return results["documents"]
```

### 🤖 EXAONE 모델 응답 생성
```python
inputs = tokenizer(prompt, return_tensors="pt").to(device)
outputs = model.generate(**inputs, max_new_tokens=512)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 📄 계약서 → PDF 변환
```python
pdfkit.from_string(html_html, pdf_path, configuration=pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf"))
```

---

## 🖥️ Windows 환경에서 GPU 사용 가이드

1. **Windows에서 WSL(리눅스 환경) 설치**
2. **Anaconda 또는 Miniconda로 가상환경 생성**
3. **CUDA 버전 확인**
   ```bash
   nvidia-smi
   ```
4. **CUDA 호환 PyTorch 설치**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
   ```

---

## 📂 프로젝트 구조

```
📦 backend/
├── generate/
│   ├── server.py          # FastAPI 서버
│   ├── answer.py          # EXAONE 기반 응답 생성
│   ├── search.py          # 판례 검색 (ChromaDB)
│   ├── doc_create.py      # 계약서 텍스트 → PDF
├── document/              # 생성된 문서 저장
├── static/                # favicon 등 정적 파일
├── main.py                # Cloudtype 프록시 서버
├── .env                   # LOCAL_GPU_SERVER 설정
```

---

## 🚀 실행 방법

```bash
# 1. 가상환경 생성
python -m venv venv
source venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 로컬 서버 실행
cd generate
python server.py
```

> 외부 연결 시:
```bash
ngrok http 8001
```

---

## 🔐 기타 보안 및 운영 팁

- `.env` 파일은 절대 외부에 노출하지 마세요!
- 모델 캐시가 누적되는 경우 `~/.cache/huggingface/` 경로 정리 필요
- PDFKit은 서버 배포 시 `wkhtmltopdf` 경로 설정 필수 (`/usr/bin/wkhtmltopdf`)

---

## 🧪 테스트용 API 예시 (Postman)

```json
POST /generate-document
{
  "contract_type": "근로계약서",
  "party_a": "홍길동",
  "party_b": "임꺽정",
  "contract_date": "2025-02-20",
  "additional_info": "계약 기간은 2년이며, 월급은 300만원입니다."
}
```

---

## 🙌 크레딧

- [EXAONE 3.5](https://huggingface.co/LGAI-EXAONE)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Cloudtype](https://cloudtype.io/)
- ngrok

---

<p align="center">
  <b>Lawyer.ai Backend: 빠르고 정확한 한국어 법률 서비스</b><br/>
  <em>문의 및 피드백은 언제든지 환영입니다!</em>
</p>
