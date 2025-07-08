## REST Client 테스트 시나리오 정리

---

### ✅ 1단계: `corporations_test.http` – 기업 및 관리자 생성 및 관리

기업 생성 시 관리자 계정이 함께 생성됩니다.
```
POST /v1/corporations              # 기업 + 관리자 생성
GET /v1/corporations               # 전체 기업 조회
GET /v1/corporations/id/{id}       # 기업 ID로 단건 조회
GET /v1/corporations/{name}        # 기업명으로 조회
PUT /v1/corporations/{id}          # 기업 정보 수정
DELETE /v1/corporations/{id}       # 기업 삭제
```

### 💡 유료 플랜 만료 자동 처리 확인
| 요구사항 | 설명 |
| --- | --- |
| 유료 플랜은 만료일이 존재 | `plan_expire_at` 필드로 판단 |
| 만료 시 자동 FREE 전환 | 	APScheduler 기반 스케줄러가 24시간마다 실행되어 자동 처리 |

🔚 수동 확인 방법
- 기업 생성 시 `plan`을 PAID로 설정하고, `plan_expire_at`을 과거 시점으로 설정
- 24시간을 기다리거나 `src/core/scheduler.py`에서 `IntervalTrigger(seconds=10)` 등으로 테스트 가능
- 일정 시간이 지난 후 기업 조회 시 plan이 FREE로 변경되었는지 확인

---

### ✅ 2단계: `auth_test.http` – 로그인 / 토큰 발급 및 갱신

생성한 관리자 계정으로 로그인 후 access_token / refresh_token 확보
```
POST /v1/auth/login              # 관리자 로그인 (JWT 토큰 발급)
POST /v1/auth/refresh            # refresh_token으로 access_token 갱신
```

📝 이후 API 요청 시 다음 헤더를 반드시 포함해야 합니다:
```
Authorization: Bearer {{access_token}} or Authorization: Bearer {{admin_access_token}}
```

---

### ✅ 3단계: `users_test.http` – 회원 관리

```
POST /v1/users                           # guest 회원 생성
GET /v1/users                            # 전체 회원 목록 조회
GET /v1/users/{email}                    # 이메일로 조회
GET /v1/users/id/{id}                    # ID로 조회
PUT /v1/users/{id}                       # 회원 정보 수정
DELETE /v1/users/{id}                    # 회원 삭제 (선택)
```

---

### ✅ 4단계: `videos_test.http` – 영상 등록 및 관리

```
POST /v1/videos                          # 영상 등록
GET /v1/videos                           # 전체 영상 조회
GET /v1/videos/{corp_id}                 # 기업별 영상 조회
GET /v1/videos/id/{id}                   # 단건 조회
PUT /v1/videos/{id}                      # 영상 정보 수정
DELETE /v1/videos/{id}                   # 영상 soft delete
PUT /v1/videos/{id}/restore              # 삭제 영상 복구 (유료 기업만 가능)
```

---

### ✅ 5단계: `videos_test.http` – 영상 스트리밍 요청

```
POST /v1/videos                          # 🎬 영상 등록 (관리자 전용)
GET /v1/videos                           # 📋 전체 영상 목록 조회
GET /v1/videos/{corporation_id}         # 🏢 기업별 영상 목록 조회
GET /v1/videos/id/{video_id}            # 🔍 영상 단건 조회
GET /v1/videos/stream/{video_id}        # 📡 영상 스트리밍 (회원 10포인트 지급, 로그 생성)
PUT /v1/videos/{video_id}               # ✏️ 영상 수정 (관리자 전용)
DELETE /v1/videos/{video_id}            # ❌ 영상 삭제 (관리자 전용)
PUT /v1/videos/{video_id}/restore       # ♻️ 삭제된 영상 복구 (유료 플랜 기업 관리자만 가능)
```

---

### ✅ 6단계: `view_logs_test.http` – 시청 로그 확인 및 수동 생성

```
GET /v1/view-logs/{user_id}/{video_id}  # 해당 회원의 시청 여부 조회
POST /v1/view-logs                      # 시청 로그 수동 생성 (테스트 용도)
```

---

### ✅ 7단계: `tokens_test.http` – Refresh Token 확인

```
GET /v1/tokens/{user_id}                # 해당 회원의 refresh_token 조회
```

📝 DB에 저장된 refresh_token과 클라이언트의 요청 토큰이 일치하는지 비교 가능

---

## 🧪 전체 테스트 흐름 요약

```
[기업 + 관리자 생성]
→ [관리자 로그인 → access_token 확보]
→ [회원 생성]
→ [영상 등록]
→ [스트리밍 요청 → 시청 로그 + 포인트 증가]
→ [시청 여부 조회]
→ [refresh_token 확인]
```