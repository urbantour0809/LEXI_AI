# 🖥 기술 스택
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-💨-brightgreen?logo=fastapi" />
  <img src="https://img.shields.io/badge/EXAONE-3.5-informational?logo=deeplearning-red" />
  <img src="https://img.shields.io/badge/ChromaDB-Search-orange" />
  <img src="https://img.shields.io/badge/Legal_Bert-Search-purple" />
</p>

# ⚖️ LEXI Backend – 법률 질문 & 계약서 생성기 (EXAONE 기반)

> 한국어 법률 질문 응답부터 자동 계약서 생성까지, EXAONE 3.5 기반 FastAPI 백엔드

---

##  <img src="https://www.lgresearch.ai/img/solution/exaone_logo.png" alt="EXAONE Logo" width="28" style="vertical-align: middle;"/> 왜 EXAONE 3.5?

- ✅ **한국어 특화 모델**: 한국어 법률/판례에 최적화된 EXAONE 3.5 사용
- ✅ **자연어 이해력 우수**: 복잡한 문장 구조도 안정적으로 처리
- ✅ **LLM + RAG 조합**: 판례 및 임베딩 검색 기반의 정확한 응답

---

## 🧠 시스템 아키텍처 및 기술 개요

### ✅ RAG 방식을 선택한 이유
- EXAONE 모델 자체에 내장된 법률 지식은 한계가 있을 수 있으므로, **외부 법률 데이터를 활용한 Retrieval-Augmented Generation(RAG)** 방식을 채택했습니다.
- 사용자의 질문에 대해 사전에 구축한 **정제된 법률 임베딩 데이터셋**에서 관련 정보를 검색하고, 이를 기반으로 EXAONE이 답변을 생성합니다.
- 이 방식은 단순한 생성 기반 모델보다 **정확성, 신뢰성, 최신성**이 훨씬 높습니다.

### ✅ 국가법령정보센터 기반 데이터셋
- 모든 법률 및 판례 데이터는 **국가법령정보센터**에서 수집된 **검증된 공공 데이터**로만 구성되어 있습니다.
- 이러한 데이터는 문장 단위로 정제 후 벡터화되어, 질문에 가장 적합한 법령 및 판례를 검색할 수 있습니다.
- 결과적으로 **신뢰할 수 있는 법적 근거**를 포함한 응답을 사용자에게 제공합니다.

### ✅ Legal-BERT 모델 파인튜닝 (검색 특화)
- [Huggingface의 Legal-BERT](https://huggingface.co/nlpaueb/legal-bert-base-uncased) 모델을 파인튜닝하여 **법률 전문 검색용 임베딩 모델**로 활용하였습니다.
- 사용자의 질문을 입력받으면, 다음과 같은 구조로 동작합니다: <br>
**[ 사용자 질문 입력 ]** ⇒ **[ EXAONE 3.5 모델이 질문 이해 ]** ⇒ **[ Legal-BERT 모델로 관련 법령 및 판례 벡터 검색 ]** ⇒ **[ 관련 법률 내용을 참조하여 EXAONE이 답변 생성 ]**
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

### 🤖 답변 & 계약서 프롬프트
```python

# 답변 (answer.py)
    prompt = f"""
    [시스템 지시사항]
    당신은 대한민국의 전문 법률 자문가입니다. 
    10년 이상의 실무 경험을 바탕으로 정확하고 실용적인 법률 자문을 제공합니다.
    모든 답변은 한국어로 작성하며, 다음 형식을 준수합니다:

    1. 먼저 질문의 핵심 쟁점을 명확히 파악하여 제시
    2. 관련 법령과 판례를 근거로 논리적인 분석 제공
    3. 실무적 관점에서 구체적인 해결방안 제시
    4. 필요한 경우 추가적인 법적 고려사항 안내

    답변 작성 시 주의사항:
    - 별표(*) 기호를 사용하지 마세요
    - 글머리 기호가 필요할 경우 '-' 또는 '1.', '2.' 등의 숫자를 사용하세요
    - 강조가 필요한 경우 '중요:', '주의:' 등의 접두어를 사용하세요

    [사용자 질문]
    {query}

    [참고 법령 및 판례]
    {relevant_text}

    [법률 검토 의견]
    """

#계약서 작성 (doc_create.py)
prompt = f"""
    다음 정보를 바탕으로 {contract_type}를 작성해주세요.
    
    [필수 작성 지침]
    1. 문서 형식:
       - 제목, 전문, 본문, 날짜, 서명란 순으로 구성
       - 각 조항은 명확한 번호와 소제목 포함
       - 전문에는 계약의 배경과 목적을 명시
    
    2. 문서 특성:
       {document_type_instructions.get(contract_type, "계약 조항을 명확하게 작성하세요.")}
    
    3. 형식 요구사항:
       - 법률 용어는 정확하고 일관되게 사용
       - 모든 금액과 날짜는 숫자와 한글을 병기
       - 각 페이지 하단에 당사자 날인란 포함
    
    [계약 정보]
    계약 당사자:
    - 갑측: {party_a}
    - 을측: {party_b}
    
    계약일자: {contract_date}
    
    추가 계약내용:
    {additional_info}

    --- 계약서 시작 ---
    """

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
5. **Pytorch를 설치 하면 cuDNN 과 같은 필요한 라이브러리들이 자동적으로 설치가 됩니다.**

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
