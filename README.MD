
![Header](https://capsule-render.vercel.app/api?type=waving&color=0:4e54c8,100:8f94fb&height=200&section=header&text=LEXI_AI%20⚖️&fontSize=38&fontColor=ffffff&fontAlignY=35&desc=Korean%20Legal%20RAG%20Assistant%20powered%20by%20EXAONE%203.5&descAlignY=60&animation=fadeIn)

# ⚖️ LEXI_AI - AI 민사 상담 웹 애플리케이션

**LEXI_AI**는 한국어에 최적화된 대형언어모델 **EXAONE 3.5** 기반으로 작동하며,  
법률 질문 응답 및 계약서 자동 생성을 수행하는 FastAPI 기반 백엔드 프로젝트입니다.

---

## 🧾 목차

- [📌 개요](#📌-개요)
- [🧠 기술 및 아키텍처 설명](#🧠-기술-및-아키텍처-설명)
- [⚙️ 설치 및 실행 방법](#⚙️-설치-및-실행-방법)
- [🖥️ Windows 환경에서 GPU 사용 가이드](#🖥️ Windows 환경에서 GPU 사용 가이드)
- [🖥️ 사용 예시](#🖥️-사용-예시)
- [📁 프로젝트 구조](#📁-프로젝트-구조)
- [💡 향후 기능](#💡-향후-기능)
- [🙌 기여 및 라이센스](#🙌-기여-및-라이센스)

---

## 📌 개요

- ✅ **법률 AI 서비스**: 한국어 법률 질의응답 & 계약서 자동 작성
- ✅ **한국어 특화 모델 EXAONE 3.5 기반**
- ✅ **RAG 방식 채택**: 외부 벡터 DB(ChromaDB) 기반 법률 정보 검색 후 답변 생성
- ✅ **양자화 모델 사용**: 4-bit 양자화로 VRAM 8GB 환경에서도 효율적

---

## 🧠 기술 및 아키텍처 설명

### 🚀 RAG (Retrieval-Augmented Generation) 방식 사용 이유

> 기존 LLM 모델의 법률 내재 지식은 제한적입니다.  
> 따라서 외부에서 수집된 공공 법률 데이터를 벡터화하고,  
> 이를 기반으로 관련 법령·판례를 검색 후 응답에 반영합니다.

### 🔒 정확도와 신뢰도 보장

- **모든 데이터는 국가법령정보센터**에서 크롤링
- **문장 단위로 정제 및 벡터화**
- 법적 효력이 있는 응답 제공

### 🔍 Legal-BERT + EXAONE 3.5

```
사용자 질문 입력
    ↓
EXAONE이 질문 이해
    ↓
Fine-tuned Legal-BERT로 벡터 DB에서 유사 법령/판례 검색
    ↓
EXAONE이 참조하여 답변 생성
```

### 🧠 주요 프롬프트

**답변 시스템 (answer.py)**:
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
```

**계약서 생성 (doc_create.py)**:
```python
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
---

## 🖥️ Windows 환경에서 GPU 사용 가이드

1. **Windows에서 WSL(리눅스 환경) 설치**
2. **Anaconda 또는 Miniconda로 가상환경 생성**
3. **CUDA 버전 확인**
   
bash
   nvidia-smi

4. **CUDA 호환 PyTorch 설치**
   
bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

5. **Pytorch를 설치 하면 cuDNN 과 같은 필요한 라이브러리들이 자동적으로 설치가 됩니다.**

---

## ⚙️ 설치 및 실행 방법

### 1. 패키지 설치
```bash
git clone https://github.com/urbantour0809/LEXI_AI.git
cd LEXI_AI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. GPU 모델 실행
```bash
cd generate
python server.py
```

> 📡 외부 연결 시:
```bash
ngrok http 8001
```

---

## 🖥️ 사용 예시

### 문서 생성 API (Postman)
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

### AI 응답 생성
```python
inputs = tokenizer(prompt, return_tensors="pt").to(device)
outputs = model.generate(**inputs, max_new_tokens=512)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

---

## 📁 프로젝트 구조

```
📦 backend/
├── generate/
│   ├── server.py          # FastAPI 서버
│   ├── answer.py          # EXAONE 응답 생성
│   ├── search.py          # 판례 검색 (ChromaDB)
│   ├── doc_create.py      # 계약서 생성 및 PDF 변환
├── document/              # 생성된 PDF 저장 폴더
├── static/                # 정적 리소스 (favicon 등)
├── main.py                # Cloudtype 프록시 서버
├── .env                   # LOCAL_GPU_SERVER 설정
```

---

## 🔩 주요 코드

### 양자화 설정 (4bit)
```python
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)
```

---

## 💡 향후 추가 기능

- [ ] ✅ 계약서 버전 관리 (수정/이력 추적)
- [ ] ✅ 사용자 인증 및 저장소 연동
- [ ] ✅ 판례 요약 기능
- [ ] ✅ GPT 기반 계약서 감정 기능

---

## 📚 기술 스택

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-💨-brightgreen?logo=fastapi" />
  <img src="https://img.shields.io/badge/EXAONE-3.5-informational?logo=deeplearning-red" />
  <img src="https://img.shields.io/badge/ChromaDB-Search-orange" />
  <img src="https://img.shields.io/badge/Legal_Bert-Search-purple" />
  <img src="https://img.shields.io/badge/TensorFlow-ML-orange?logo=tensorflow" />
  <img src="https://img.shields.io/badge/PyTorch-🔥-red?logo=pytorch" />
</p>

---

## 🙌 기여 & 라이센스

- 본 프로젝트는 개인 연구 및 학습 목적으로 배포되었습니다.
- 기술 및 모델 관련 문의는 Issues 또는 이메일로 보내주세요.
- [EXAONE 3.5](https://huggingface.co/LGAI-EXAONE)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Cloudtype](https://cloudtype.io/)
- ngrok

---

<p align="center">
  <b>LEXI_AI - 정확하고 신뢰할 수 있는 한국어 법률 어시스턴트</b><br/>
  <em>powered by EXAONE and Legal-Bert</em>
</p>
