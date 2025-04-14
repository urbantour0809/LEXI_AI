from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"

# 필요한 패키지 설치 확인
try:
    from accelerate import infer_auto_device_map
    from transformers import BitsAndBytesConfig
except ImportError:
    raise ImportError("`accelerate`와 `bitsandbytes` 패키지가 필요합니다. `pip install accelerate bitsandbytes`를 실행하세요.")

# GPU 사용 여부 확인
device = "cuda" if torch.cuda.is_available() else "cpu"

# 4비트 양자화 설정
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,                # 4비트 양자화 사용
    bnb_4bit_compute_dtype=torch.float16,  # 연산 시 float16 사용
    bnb_4bit_quant_type="nf4",       # NF4 양자화 타입 사용
    bnb_4bit_use_double_quant=True   # 이중 양자화로 메모리 추가 절약
)

# 모델 로드 (4비트 양자화 + GPU 자동 분배)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    device_map="auto",
    quantization_config=quantization_config
)

def generate_answer(query, relevant_docs, sources, scores):
    """ EXAONE 모델을 이용하여 법률 답변 생성 (GPU 활용) """

    if not relevant_docs:
        relevant_docs = ["참고할 법률 조항을 찾을 수 없습니다. 일반적인 법률 원칙을 적용하세요."]

    # `scores`가 2차원 리스트(`list[list]`)인지 확인 후 1차원으로 변환
    scores = [s for sublist in scores for s in (sublist if isinstance(sublist, list) else [sublist])]

    try:
        scores = [float(s) for s in scores]
    except ValueError:
        scores = [0.0] * len(scores)

    # 토큰 수 초과 방지: 관련 법률 내용을 3000자까지만 사용
    relevant_text = "\n".join(relevant_docs)[:3000]

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

    # 너무 긴 입력 방지: 4096 토큰 제한
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096).to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=1028,  # 출력 길이를 512 토큰으로 제한
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )

    # 전체 출력에서 프롬프트 부분을 제거하고 실제 답변만 추출
    full_response = tokenizer.decode(output[0], skip_special_tokens=True)
    answer = full_response.split("[법률 검토 의견]")[-1].strip()

    return answer
