\_\_## 브랜치 전략

### **브랜치 구성**

![gitflow-branch.png](gitflow-branch.png)

| 브랜치 유형 | 설명                      |
| ----------- | ------------------------- |
| main        | 배포 가능한 안정적인 코드 |
| develop     | 최신 개발 코드            |
| feature/\*  | 새로운 기능 개발          |
| release/\*  | 릴리스 준비               |
| hotfix/\*   | 긴급 수정                 |

### **작업 흐름**

1. **feature 브랜치에서 개발**:
   - develop에서 feature/feature-name 브랜치를 생성
   - 기능 개발 완료 후 develop 브랜치에 병합
2. **release 브랜치에서 릴리스 준비**:
   - develop에서 release/release-version 브랜치를 생성
   - 릴리스 준비, 버그 수정, 문서화 등을 수행 후 커밋
   - 준비 완료 후 main 브랜치에 병합하고, develop 브랜치에도 병합하여 최신 상태를 반영
3. **hotfix 브랜치에서 긴급 수정**:
   - main에서 hotfix/hotfix-name 브랜치를 생성
   - 긴급 수정 완료 후 main 브랜치와 develop 브랜치에 병합

### 커밋 메시지 가이드라인

| 브랜치     | 작성 샘플                        | 예시                                     |
| ---------- | -------------------------------- | ---------------------------------------- |
| main       | vX.Y.Z: <변경 요약>              | v1.0.0: 배포                             |
|            |                                  | v1.0.1: Merge branch hotfix/001          |
|            |                                  | v1.1.0: Merge branch release/001         |
| release/\* | release/vX.Y.Z: <내용>           | release/v1.0.0: 변경 이력, 안정화        |
| hotfix/\*  | hotfix/<id>: <버그 설명>         | hotfix/001: 버그 긴급 수정               |
| develop    | develop: <내용>                  | develop: 코드 리팩토링, 오타, 오류 수정  |
|            | develop: Merge branch <브랜치명> | develop: Merge branch feature/001 - 내용 |
|            |                                  | develop: Merge branch hotfix/001 - 내용  |
|            |                                  | develop: Merge branch release/v1.0.0     |
| feature/\* | feature/<id>: <내용>             | feature/001: 기능 추가                   |
