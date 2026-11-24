# src/vision_rgb — 사람 인식 (일반 카메라)

**역할:** 일반 카메라 영상에서 사람(피규어)을 찾아 바닥 좌표(cm)로 바꾼 뒤 `PersonResult`로 내보냅니다.
**주 담당:** SW/AI

## 여기에 넣는 것
- 카메라 입력, 사람 인식 추론, 픽셀→바닥 좌표 변환 코드
- 관련 REQ: REQ-005, REQ-006, REQ-015, REQ-016

## 넣지 않는 것
- 모델 학습 코드 → `training/`
- 학습된 모델 파일(.pt, .onnx, .tflite) → `models/` (깃 제외)

> 이 폴더 규칙은 [CONTRIBUTING.md](../../CONTRIBUTING.md)와 [AGENTS.md](../../AGENTS.md)를 따릅니다.
