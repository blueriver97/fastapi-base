# FastAPI-Base

---

<!-- TOC -->

- [FastAPI-Base](#fastapi-base)
  - [Setup](#setup)
  - [서버 설치](#서버-설치)
  - [서버 실행](#서버-실행)
    - [파이썬 실행](#파이썬-실행)
    - [Uvicorn 실행](#uvicorn-실행)
    - [Pytest 테스트](#pytest-테스트)
  - [Issue](#issue)
    - [1. How to install pymssql on macOS (Using SQL server)](#1-how-to-install-pymssql-on-macos-using-sql-server)

## <!-- TOC -->

FastAPI 프로젝트 공통 템플릿

## Setup

```bash
./init.sh
pip install -r requirements.txt
```

## 서버 설치

```bash
# Dev
pip install -e .

# Prod
pip install .
```

## 서버 실행

<aside>
💡Websocket 서버 시작 시 other_asgi_app으로 HTTP 서버도 동작함.
</aside>

```bash
cd tests
python3 run_server.py
```

### Uvicorn 실행

**HTTP**

```bash
# Dev
uvicorn base.api:http_app --host=0.0.0.0 --port=9090 [--reload --reload-dir src/base] --env-file tests/dev.env

# Prod
uvicorn base.api:http_app --host=0.0.0.0 --port=9090 [--workers 4] --env-file tests/prod.env
```

**Websocket**

```bash
# Dev
uvicorn base.api:ws_app --host=0.0.0.0 --port=9090 [--reload --reload-dir src/base] --env-file tests/dev.env

# Prod
uvicorn base.api:ws_app --host=0.0.0.0 --port=9090 [--workers 4] --env-file tests/prod.env
```

### Pytest 실행

`test_xxx.py` 파일을 실행하여 테스트를 수행함.

```bash
cd tests/pytest

# Default
pytest [test_file_name]

# Debug
# -vv : verbose, 상세 정보 출력
# -s : 수행 테스트의 표준 출력을 캡처함
pytest -vv -s [test_file_name]
```

---

## 이슈 처리

### 1. How to install pymssql on macOS (Using SQL server)

```zsh
brew install freetds
tsql -C
#Compile-time settings (established with the "configure" script)
#                            Version: freetds v1.3.20
#             freetds.conf directory: /opt/homebrew/etc
#     MS db-lib source compatibility: no
#        Sybase binary compatibility: yes
#                      Thread safety: yes
#                      iconv library: yes
#                        TDS version: 7.3
#                              iODBC: no
#                           unixodbc: yes
#              SSPI "trusted" logins: no
#                           Kerberos: yes
#                            OpenSSL: yes
#                             GnuTLS: no
#                               MARS: yes
```

```zsh
brew install openssl
openssl version
# OpenSSL 3.1.2 1 Aug 2023 (Library: OpenSSL 3.1.2 1 Aug 2023)
```

```zsh
echo 'export LDFLAGS="-L/opt/homebrew/opt/freetds/lib -L/opt/homebrew/opt/openssl@3/lib"' >> ~/.zshrc
echo 'export CFLAGS="-I/opt/homebrew/opt/freetds/include"' >> ~/.zshrc
echo 'export CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include"' >> ~/.zshrc
source ~/.zshrc
pip install pymssql
```
