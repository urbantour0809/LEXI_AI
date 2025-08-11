## LEXI.AI — 법률 상담/문서 생성 풀스택 애플리케이션

AI 기반 법률 상담과 문서 생성을 제공하는 모노레포 프로젝트입니다. 백엔드는 Spring Boot, 프론트엔드는 React로 구성되어 있으며 JWT 인증, 이메일 기반 계정 복구, 채팅 보관 기능을 지원합니다.

### 모듈 구조
- `src/main/java` — Spring Boot 백엔드 (API, 인증, JPA, 메일)
- `lawbot-frontend/` — React 프론트엔드 (CRA, 라우팅, 채팅 UI)
- `gradle/wrapper/` — Gradle Wrapper 설정

---

## 기술 스택
- **백엔드**: Java 17, Spring Boot 3.4.1, Spring Security, Spring Data JPA(Hibernate 6.2), Thymeleaf, JavaMail, JJWT 0.11.5
- **데이터베이스**: MySQL 8
- **프론트엔드**: React 19, react-router-dom 7, axios, react-spinners, react-markdown
- **빌드/도구**: Gradle, dotenv-java

---

## 빠른 시작

### 사전 준비
- Java 17 (JDK)
- Node.js 18+ (권장 LTS)
- MySQL 8 (로컬 DB)
- SMTP 계정 (예: Gmail 앱 비밀번호)

### 환경 변수 설정 (이메일)
Spring Boot는 `application.properties`에서 아래 값을 참조합니다. OS 환경 변수에 설정하세요.
- `MAIL_USERNAME` — 발신 이메일 계정
- `MAIL_PASSWORD` — 앱 비밀번호(또는 SMTP 비밀번호)

Windows PowerShell 예시:
```powershell
setx MAIL_USERNAME "your-email@gmail.com"
setx MAIL_PASSWORD "your-app-password"
```

### 데이터베이스 준비
`application.properties` 기본값은 아래와 같습니다. 로컬 MySQL에 `lawyer_ai` 데이터베이스를 생성하고 계정 정보를 환경에 맞게 수정하세요.
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/lawyer_ai
spring.datasource.username=root
spring.datasource.password=1234
spring.jpa.hibernate.ddl-auto=update
```

### 백엔드 실행
- Windows: `gradlew.bat clean build` 후 `gradlew.bat bootRun`
- macOS/Linux: `./gradlew clean build` 후 `./gradlew bootRun`

기본 포트: `http://localhost:8080`

### 프론트엔드 실행
```bash
cd lawbot-frontend
npm install
npm start
```
기본 포트: `http://localhost:3000` (보안 정책상 3000 포트 사용 권장)

---

## 핵심 기능
- **회원가입/로그인**: JWT 발급 및 보관
- **개인정보 조회**: 토큰 기반 보호 API
- **채팅 보관**: 대화 생성/목록/메시지 저장
- **계정 복구**: 이메일로 인증코드 전송 및 검증
- **AI 연동**: 외부 LLM 엔드포인트와 법률 문서 생성

---

## API 요약

### 인증/사용자
- `POST /api/Signup`
  - Body: `{ username, password, confirmPassword, name, email, ... }`
  - 응답: `"회원가입 성공"`
- `POST /api/login`
  - Body: `{ username, password }`
  - 응답: `{ token, user_id }`
- `GET /api/user/info`  
  - Header: `Authorization: Bearer <JWT>`
  - 응답: `{ id, email, name, phone }` (미인증 시 403)

### 채팅
- `POST /api/chats/chat`  
  - Body: `{ user_id, title }` → 새 채팅 생성, 응답에 `chatId`
- `GET /api/chats/chats/{userId}`  
  - 사용자 채팅 목록 조회
- `POST /api/chats/message`  
  - Body: `{ chat_id, sender: "user"|"ai", text }` → 메시지 저장
- `GET /api/chats/chat/{chatId}`  
  - 특정 채팅 메시지 목록

### 계정 복구
- `POST /api/recovery/send`  
  - Body: `{ email }` → 복구 코드 전송
- `POST /api/recovery/verify`  
  - Body: `{ code }` → 코드 검증(성공 시 비밀번호 변경 페이지로 이동)

### AI 연동 (프론트엔드에서 호출)
- 상담: `POST https://port-0-lawyer-ai-m2eej1jqd8b44d66.sel4.cloudtype.app/ask`  
  - Body: `{ question }` → 응답 `{ answer }`
- 문서 생성: `POST https://port-0-lawyer-ai-m2eej1jqd8b44d66.sel4.cloudtype.app/generate-document`  
  - Body: `{ contract_type, party_a, party_b, contract_date, additional_info }`  
  - 응답: `{ download_link }`

---

## CORS 및 인증
- 허용 오리진: `http://localhost:3000`, `http://localhost:8080` 등  
  다른 포트를 사용할 경우 `SecurityConfig`의 CORS 설정을 업데이트하세요.
- `Bearer` 토큰은 로그인 성공 시 응답 본문으로 전달되며, 프론트엔드는 `localStorage`에 저장하여 보호 API 호출 시 헤더에 포함합니다.

---

## 개발 팁
- JWT 서명 키(`jwt.secret`)는 Base64 인코딩된 256비트(32바이트) 이상이어야 합니다.  
  예시 프로퍼티: `jwt.secret=...` (소스 커밋 금지)
- 메일 발송 실패(400/402 유사) 시 대부분 환경 변수 누락이 원인입니다. `MAIL_USERNAME/PASSWORD`를 확인하세요.
- 403 에러는 토큰 누락/만료/유효성 실패일 수 있습니다. `Authorization: Bearer <token>` 헤더를 확인하세요.
- 500 에러는 메서드/URL 실수, 파라미터 누락, DB/SMTP 연결 문제 가능성이 높습니다.

---

## 스크립트 모음
- 백엔드 테스트: `gradlew.bat test` 또는 `./gradlew test`
- 프론트엔드: `npm start`, `npm run build`, `npm test`

---

## 프로젝트 구조(요약)
```text
LEXI_AI/
├─ src/main/java/Lawyerai/Lawyer_ai/   # Spring Boot 코드 (컨트롤러/서비스/보안/JPA)
├─ src/main/resources/                 # 설정 및 템플릿
├─ lawbot-frontend/                    # React 앱 (페이지/컴포넌트/정적자원)
└─ gradle/wrapper/                     # Gradle Wrapper
```

---

## 트러블슈팅 체크리스트
- **이메일 오류**: SMTP 계정, 포트(587), TLS 설정 확인. 환경 변수 설정 여부 확인
- **DB 연결 오류**: DB명/계정/비밀번호, 포트(3306) 확인. `ddl-auto=update`로 스키마 자동 생성
- **CORS 오류**: 프론트 실행 포트가 CORS 허용 목록에 있는지 확인
- **토큰 관련**: 만료/서명키 오류 로그 확인, 재로그인으로 갱신

---


