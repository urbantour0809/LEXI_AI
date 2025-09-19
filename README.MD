
![Header](https://capsule-render.vercel.app/api?type=waving&color=0:4e54c8,100:8f94fb&height=200&section=header&text=LEXI_AI%20⚖️&fontSize=38&fontColor=ffffff&fontAlignY=35&desc=Korean%20Legal%20RAG%20Assistant%20powered%20by%20EXAONE%203.5&descAlignY=60&animation=fadeIn)

# ⚖️ LEXI_AI - AI 민사 상담 웹 애플리케이션

**LEXI_AI**는 한국어에 최적화된 대형언어모델 **EXAONE 3.5** 기반으로 작동하며,  
법률 질문 응답 및 계약서 자동 생성을 수행하는 FastAPI 기반 백엔드 프로젝트입니다.

> 한국어 법률 상담을 위한 대화형 AI 시스템  
> **EXAONE 3.5 + RAG + Legal-BERT** 기반으로 정확성과 신뢰도를 높였습니다.  

---

## 📌 프로젝트 소개  

- **법률 AI 서비스**: 한국어 법률 질의응답 & 계약서 자동 작성  
- **한국어 특화 모델 적용**: EXAONE 3.5 + Legal-BERT  
- **RAG 기반 검색**: ChromaDB로 판례/법령을 찾아 근거와 함께 답변  
- **경량화 모델**: 4-bit 양자화로 GPU 8GB 환경에서도 원활히 실행  

---

## ⚙️ 기술 스택

| 영역 | 기술 |
|------|------|
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?logo=springboot&logoColor=white) |
| **Frontend** | ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black) |
| **Database & VectorDB** | ![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-yellow) |
| **AI/ML** | ![Exaone](https://img.shields.io/badge/Exaone%203.5-AI-blueviolet) ![LegalBERT](https://img.shields.io/badge/LegalBERT-NLP-orange) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white) |
| **Infra & DevOps** | ![Cloudtype](https://img.shields.io/badge/Cloudtype-4285F4?logo=googlecloud&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black) ![Ngrok](https://img.shields.io/badge/Ngrok-1F1F1F?logo=ngrok&logoColor=white) |

---

## 🧩 아키텍처  

```
사용자 질의 
   ↓
ChromaDB (판례/법령 검색)
   ↓
EXAONE 3.5 + Legal-BERT (근거 반영 답변 생성)
   ↓
FastAPI / SpringBoot (API 통합)
   ↓
React.js (프론트엔드 UI)
```

---

## 🚀 주요 기능  

- 법률 질의응답 (Q&A)  
- 계약서 자동 생성 (근로/임대/기타 문서 지원)  
- 판례 및 법령 검색 (ChromaDB 기반)  
- PDF 문서 생성 및 저장  
- 관리자 기능: 검색 로그 및 데이터 관리  

---

## 🔍 문제와 해결  

- **GPU 메모리 부족 (RTX 4060, 8GB)**  
  → 4bit 양자화 + 메모리 최적화 옵션 적용, CPU fallback 도입  
- **검색 정확도 부족**  
  → 메타데이터 필터링 + 법률 문서 전처리로 검색 성능 개선  
- **답변 신뢰도 문제**  
  → RAG와 Legal-BERT 결합으로 일관성 강화  

---

## 📁 프로젝트 구조  

```
LEXI_AI/
├── backend/
│   ├── generate/          # AI 응답 및 계약서 생성
│   ├── search.py          # 판례/법령 검색 (ChromaDB)
│   ├── answer.py          # EXAONE 응답 처리
│   └── doc_create.py      # 계약서 PDF 변환
├── frontend/              # React 프론트엔드
├── document/              # 생성된 문서 저장
├── main.py                # Cloudtype 프록시 서버
└── .env                   # 환경변수 설정
```

---

<p align="center">
  <b>LEXI – 한국어 법률에 특화된 AI 어시스턴트</b><br/>
  <em>Powered by EXAONE & Legal-BERT</em>
</p>
