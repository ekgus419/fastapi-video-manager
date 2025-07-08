## 🔐 Auth API 문서

### ✅ 1. 로그인 API

| 항목 | 설명 |
| --- | --- |
| **Method** | `POST` |
| **URL** | `/v1/auth/login` |
| **Request Body** | `email`, `password` (`LoginRequestDto`) |
| **Response** | `access_token`, `refresh_token` (JWT 페어) |
| **권한** | ❌ 인증 불필요 |
| **예외 처리** | `401 Unauthorized` – 이메일 또는 비밀번호 불일치 |

---

### ✅ 2. 토큰 재발급 API

| 항목 | 설명 |
| --- | --- |
| **Method** | `POST` |
| **URL** | `/v1/auth/refresh` |
| **Request Body** | `refresh_token` (`RefreshRequestDto`) |
| **Response** | 새 `access_token` + 기존 `refresh_token` |
| **권한** | ❌ 인증 불필요 |
| **예외 처리** |`401 Unauthorized` | - refresh token 디코딩 실패- 저장된 토큰과 불일치 |

## 🏢 Corporation API 문서

### ✅ 1. 기업 생성 + 관리자 등록

| 항목 | 설명 |
| --- | --- |
| **Method** | `POST` |
| **URL** | `/v1/corporations` |
| **Request Body** | `CorporationCreateRequestDto`→ 기업명, 플랜, 만료일, 관리자 이메일/비밀번호 포함 |
| **Response** | 생성된 `CorporationResponseDto` |
| **권한** | ❌ 인증 불필요 (회원가입처럼 사용) |
| **예외 처리** | `400 Conflict` – 중복된 기업명 존재 시 |

---

### ✅ 2. 기업 ID로 단건 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/corporations/id/{corporation_id}` |
| **Query Params** | 없음 |
| **Response** | 해당 기업의 `CorporationResponseDto` |
| **권한** | ✅ 인증 필요 없음 |
| **예외 처리** | `404 Not Found` – 존재하지 않는 기업 ID인 경우 |

---

### ✅ 3. 기업 이름으로 단건 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/corporations/{name}` |
| **Query Params** | 없음 |
| **Response** | 해당 이름의 `CorporationResponseDto` |
| **권한** | ✅ 인증 필요 없음 |
| **예외 처리** | `404 Not Found` – 존재하지 않는 기업명인 경우 |

---

### ✅ 4. 전체 기업 목록 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/corporations` |
| **Query Params** | 없음 |
| **Response** | `List[CorporationResponseDto]` |
| **권한** | ✅ 인증 필요 없음 |
| **예외 처리** | 없음 |

---

### ✅ 5. 기업 정보 수정

| 항목 | 설명 |
| --- | --- |
| **Method** | `PUT` |
| **URL** | `/v1/corporations/{corporation_id}` |
| **Request Body** | `CorporationUpdateRequestDto` (기업명, 플랜, 만료일) |
| **Response** | 수정된 `CorporationResponseDto` |
| **권한** | ✅ 같은 기업의 **admin 유저만 가능** |
| **예외 처리** | `400 Conflict` – 기업명 중복 |
| **예외 처리** | `403 Forbidden` – 관리자가 아닌 경우 |

---

### ✅ 6. 기업 삭제

| 항목 | 설명 |
| --- | --- |
| **Method** | `DELETE` |
| **URL** | `/v1/corporations/{corporation_id}` |
| **Response** | 삭제 성공 여부 (`true`) |
| **권한** | ✅ 같은 기업의 **admin 유저만 가능** |
| **예외 처리** |  |
| • `403 Forbidden` | 관리자가 아닌 경우 |
| • `404 Not Found` | 기업이 존재하지 않는 경우 |

## 🔐 Refresh Token API 문서

### ✅ 사용자별 Refresh Token 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/tokens/{user_id}` |
| **Path Param** | `user_id` (int) – 조회할 사용자 ID |
| **Response** | 해당 사용자의 `RefreshTokenResponseDto` |
| **권한** | ✅ 같은 기업의 **admin 유저만 가능** |
| **예외 처리** | `404 Not Found` – 해당 유저에 대한 Refresh Token이 없을 경우 |
| **예외 처리** | `403 Forbidden` – 관리자가 아닌 경우 (또는 다른 기업 소속) |

## 👤 User API 문서

### ✅ 1. 회원 생성

| 항목 | 설명 |
| --- | --- |
| **Method** | `POST` |
| **URL** | `/v1/users` |
| **Request Body** | `UserCreateRequestDto`(이메일, 비밀번호, 기업 ID 등) |
| **Response** | 생성된 `UserResponseDto` |
| **권한** | ✅ 같은 기업의 **admin**만 가능 |
| **예외 처리** | `409 Conflict` – 동일 이메일이 같은 기업에 이미 존재 |

---

### ✅ 2. 회원 이메일로 단건 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/users/{email}` |
| **Response** | 해당 이메일의 `UserResponseDto` |
| **권한** | ✅ **같은 기업의 admin** 또는 **본인** |
| **예외 처리** | `404 Not Found` – 해당 이메일의 유저 없음 |

---

### ✅ 3. 회원 ID로 단건 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/users/id/{user_id}` |
| **Response** | 해당 ID의 `UserResponseDto` |
| **권한** | ✅ **같은 기업의 admin** 또는 **본인** |
| **예외 처리** | `404 Not Found` – 해당 ID의 유저 없음 |

---

### ✅ 4. 전체 회원 목록 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/users` |
| **Response** | `List[UserResponseDto]` |
| **권한** | ✅ 같은 기업의 **admin**만 가능 |
| **예외 처리** | 없음 |

---

### ✅ 5. 회원 정보 수정

| 항목 | 설명 |
| --- | --- |
| **Method** | `PUT` |
| **URL** | `/v1/users/{user_id}` |
| **Request Body** | `UserUpdateRequestDto` (수정할 값: 비밀번호, 권한 등) |
| **Response** | 수정된 `UserResponseDto` |
| **권한** | ✅ **본인 또는 같은 기업의 admin** |
| **예외 처리** | `404 Not Found` – 해당 ID의 유저 없음 |
| **예외 처리** | `403 Forbidden` – 권한이 없는 경우 (다른 기업 또는 guest가 타인 수정 시도) |

---

### ✅ 6. 회원 삭제 (Soft Delete)

| 항목 | 설명 |
| --- | --- |
| **Method** | `DELETE` |
| **URL** | `/v1/users/{user_id}` |
| **Response** | 삭제 성공 여부 (`true`) |
| **권한** | ✅ **본인 또는 같은 기업의 admin** |
| **예외 처리** |  |
| • `404 Not Found` | 해당 ID의 유저 없음 |
| • `403 Forbidden` | 권한이 없는 경우 |

## 🎥 Video API 문서

### ✅ 1. 영상 등록 (관리자 전용)

| 항목 | 설명 |
| --- | --- |
| **Method** | `POST` |
| **URL** | `/v1/videos` |
| **Request Body** | `VideoCreateRequestDto` (영상명, 파일 경로, 기업 ID) |
| **Response** | 등록된 `VideoResponseDto` |
| **권한** | ✅ **admin만 가능** |
| **예외 처리** | 없음 |

---

### ✅ 2. 영상 수정 (관리자 전용)

| 항목 | 설명 |
| --- | --- |
| **Method** | `PUT` |
| **URL** | `/v1/videos/{video_id}` |
| **Request Body** | `VideoUpdateRequestDto` (영상명 또는 파일 경로 변경) |
| **Response** | 수정된 `VideoResponseDto` |
| **권한** | ✅ **admin만 가능** |
| **예외 처리** | `404 Not Found` – 영상이 존재하지 않을 경우 |

---

### ✅ 3. 영상 삭제 (관리자 전용)

| 항목 | 설명 |
| --- | --- |
| **Method** | `DELETE` |
| **URL** | `/v1/videos/{video_id}` |
| **Response** | `true` |
| **권한** | ✅ **admin만 가능** |
| **예외 처리** | `404 Not Found` – 영상이 존재하지 않을 경우 |

---

### ✅ 4. 삭제된 영상 복구 (관리자 + 유료 기업 전용)

| 항목 | 설명 |
| --- | --- |
| **Method** | `PUT` |
| **URL** | `/v1/videos/{video_id}/restore` |
| **Response** | 복구된 `VideoResponseDto` |
| **권한** | ✅ **admin** + 소속 기업이 **PAID** 플랜 |
| **예외 처리** | `404 Not Found` – 영상이 없거나 삭제 상태가 아닌 경우 |
| **예외 처리** | `403 Forbidden` – 유료 플랜이 아닌 경우 |


---

### ✅ 5. 영상 단건 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/videos/id/{video_id}` |
| **Response** | `VideoResponseDto` |
| **권한** | ✅ 인증 필요 없음 |
| **예외 처리** | `404 Not Found` – 존재하지 않는 영상 ID인 경우 |

---

### ✅ 6. 전체 영상 목록 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/videos` |
| **Response** | `List[VideoResponseDto]` |
| **권한** | ✅ 인증 불필요 (공개 API) |
| **예외 처리** | 없음 |

---

### ✅ 7. 기업별 영상 목록 조회

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/videos/{corporation_id}` |
| **Response** | `List[VideoResponseDto]` |
| **권한** | ✅ 인증 필요 |
| **예외 처리** | 없음 |

---

### ✅ 8. 영상 스트리밍 요청 (자동 포인트 + 시청 로그)

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/videos/stream/{video_id}` |
| **Response** | `StreamingResponse` (MP4 영상 프록시 전달) |
| **부가 처리** | `VideoViewLog` 자동 생성• 유저에게 포인트 10점 지급 |  |
| **권한** | ✅ 로그인한 유저 |
| **예외 처리** | `404 Not Found` – 영상 또는 유저 없음• |
| **예외 처리** | `502 Bad Gateway` – 외부 스트리밍 실패 |


## 👁️ VideoViewLog (시청 로그) API 문서

### ✅ 1. 시청 여부 확인

| 항목 | 설명 |
| --- | --- |
| **Method** | `GET` |
| **URL** | `/v1/view-logs/{user_id}/{video_id}` |
| **Path Params** | `user_id` (회원 ID), `video_id` (영상 ID) |
| **Response** | `true` 또는 `false` (시청 여부) |
| **권한** | ✅ 인증 필요 |
| **예외 처리** | 없음 (존재 여부만 확인) |

---

### ✅ 2. 시청 로그 수동 생성

| 항목 | 설명 |
| --- | --- |
| **Method** | `POST` |
| **URL** | `/v1/view-logs` |
| **Request Body** | `VideoViewLogCreateRequestDto`→ `video_id` 필드 |
| **Response** | 생성된 `VideoViewLogResponseDto` |
| **권한** | ✅ 로그인한 사용자만 가능 |
| **처리 로직** | 현재 로그인된 유저 ID 기준으로 시청 로그 생성 |  
| **처리 로직** | `viewed_at`은 자동으로 현재 시간 입력됨 |
| **예외 처리** | 없음 (기록 실패 시 서버 오류 처리) |