import base64
import hashlib
import importlib.util
import json
import os
import platform
import re
import socket
import sys
import uuid
from typing import Any, Dict, List, Optional, Union, Callable

import requests
from passlib.context import CryptContext


def post_http_api(
    url: str, uri: str, headers: Optional[Dict[str, str]] = None, body: Optional[Dict[str, Any]] = None
) -> Any:
    """
    HTTP POST 요청을 보내는 함수.

    :param url: API 주소
    :param uri: 리소스 URI
    :param headers: 헤더
    :param body: 데이터
    :return: 요청 결과
    """
    headers = headers or {"Content-type": "application/json"}
    response = requests.post(f"http://{url}{uri}", json=body, headers=headers)
    return _handle_response(response)


def get_http_api(url: str, uri: str, headers: Optional[Dict[str, str]] = None) -> Any:
    """
    HTTP GET 요청을 보내는 함수.

    :param url: API 주소
    :param uri: 리소스 URI
    :param headers: 헤더
    :return: 조회 결과
    """
    headers = headers or {"Content-type": "application/json"}
    response = requests.get(f"http://{url}{uri}", headers=headers)
    return _handle_response(response)


def delete_http_api(
    url: str, uri: str, body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None
) -> Any:
    """
    HTTP DELETE 요청을 보내는 함수.

    :param url: API 주소
    :param uri: 리소스 URI
    :param body: 데이터
    :param headers: 헤더
    :return: 요청 결과
    """
    headers = headers or {"Content-type": "application/json"}
    response = requests.delete(f"http://{url}{uri}", json=body, headers=headers)
    return _handle_response(response)


def _handle_response(response: requests.Response) -> Any:
    """HTTP 응답을 처리하는 함수."""
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.content.decode("utf-8")


def assert_api(
    right_answer: Dict[str, Any],
    url: str,
    uri: str = "",
    body: Optional[Dict[str, Any]] = None,
    parse_func: Optional[Callable] = None,
) -> bool:
    """
    API의 응답이 정답과 일치하는지 확인하는 함수.

    :param right_answer: 정답 문장
    :param url: API 주소
    :param uri: 리소스 URI
    :param body: 데이터
    :param parse_func: 결과 파싱을 위한 사용자 함수
    :return: 정답 여부
    """
    body = body or {}
    result = post_http_api(url, uri, body=body)
    if callable(parse_func):
        result = parse_func(result)

    return any(result in answers for answers in right_answer.values())


def assert_answer(
    right_answer: Union[Dict[str, Any], List[str]],
    capture_list: List[str],
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> bool:
    """
    API 결과가 정답과 일치하는지 확인하는 함수.

    :param right_answer: 정답 문장
    :param capture_list: API 결과를 캡쳐한 문장
    :param include_patterns: 포함해야 하는 패턴
    :param exclude_patterns: 포함하지 않아야 하는 패턴
    :return: Pass/Fail 여부
    """
    include_patterns = include_patterns or []
    exclude_patterns = exclude_patterns or []

    if isinstance(right_answer, dict):
        return _assert_dict_answer(right_answer, capture_list, include_patterns, exclude_patterns)
    elif isinstance(right_answer, list):
        return _assert_list_answer(right_answer, capture_list, include_patterns, exclude_patterns)

    return False


def _assert_dict_answer(
    right_answer: Dict[str, Any], capture_list: List[str], include_patterns: List[str], exclude_patterns: List[str]
) -> bool:
    """딕셔너리 정답을 검증하는 내부 함수."""
    for idx, key in enumerate(right_answer.keys()):
        if right_answer[key] not in capture_list[idx]:
            return False

        if not _check_patterns(capture_list[idx], include_patterns, exclude_patterns):
            return False

    return True


def _assert_list_answer(
    right_answer: List[str], capture_list: List[str], include_patterns: List[str], exclude_patterns: List[str]
) -> bool:
    """리스트 정답을 검증하는 내부 함수."""
    for capture in capture_list:
        if capture not in right_answer:
            return False

        if not _check_patterns(capture, include_patterns, exclude_patterns):
            return False

    return True


def _check_patterns(text: str, include_patterns: List[str], exclude_patterns: List[str]) -> bool:
    """포함 및 제외 패턴을 확인하는 내부 함수."""
    for pattern in include_patterns:
        if not re.search(pattern, text):
            return False

    for pattern in exclude_patterns:
        if re.search(pattern, text):
            return False

    return True


def load_module(module_name: str, file_path: str) -> Any:
    """
    .py 파일을 읽어 모듈을 동적으로 로딩하는 함수.

    :param module_name: 모듈 이름
    :param file_path: 파일 경로
    :return: 로드된 모듈
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def read_file_to_chunks(f_path: str, chunk_sz: int) -> List[bytes]:
    """
    파일 내용을 읽어 chunks로 분할하는 함수.

    :param f_path: 파일 경로
    :param chunk_sz: 청크 크기
    :return: 청크 리스트
    """
    with open(f_path, "rb") as f:
        chunks = []
        while True:
            chunk = f.read(chunk_sz)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks


def save_chunks_to_file(chunks: List[bytes], f_path: str) -> int:
    """
    분할된 청크를 하나의 파일에 출력하는 함수.

    :param chunks: 청크 리스트
    :param f_path: 파일 경로
    :return: 작성된 바이트 수
    """
    result = 0  # write size

    with open(f_path, "wb") as f:
        for idx, chunk in enumerate(chunks, start=1):
            result += f.write(chunk)
            print(f"{f_path} > {idx}/{len(chunks)}")

    return result


def convert_datetime_to_timestamp(timedelta, short: bool = False) -> str:
    """시간을 타임스탬프로 변환하는 함수."""
    return timedelta.strftime("%Y%m%d%H%M%S.%f")[:-3] if short else timedelta.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def convert_text_to_md5(text: str) -> str:
    """텍스트를 MD5 해시로 변환하는 함수."""
    assert isinstance(text, str)
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def uuid5(name: str) -> uuid.UUID:
    """이름을 기반으로 UUID5를 생성하는 함수."""
    return uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=name)


def uuid4() -> uuid.UUID:
    """UUID4를 생성하는 함수."""
    return uuid.uuid4()


def uuid_to_b64uuid(uuid4: uuid.UUID) -> str:
    """UUID4를 Base64 URL 안전한 문자열로 변환하는 함수."""
    return base64.urlsafe_b64encode(uuid4.bytes).decode("utf-8")


def b64uuid_to_uuid(b64uuid: str) -> str:
    """Base64 URL 안전한 문자열을 UUID로 변환하는 함수."""
    return str(uuid.UUID(bytes=base64.urlsafe_b64decode(b64uuid)))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증 함수."""
    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호 해시 생성 함수."""
    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return crypt_context.hash(password)


def get_hostname() -> str:
    """호스트 이름을 반환하는 함수."""
    return socket.gethostname()


def get_pid() -> int:
    """현재 프로세스 ID를 반환하는 함수."""
    return os.getpid()


def get_proc_listen_port(pid: int) -> List[int]:
    """주어진 PID의 리슨 포트를 반환하는 함수."""
    os_name = platform.platform()
    ports: set[int] = set()
    pattern = re.compile(r":[0-9]+")

    if "macOS" in os_name:
        read_lines = os.popen("lsof -i -P | grep -i LISTEN").readlines()
    elif "Linux" in os_name:
        read_lines = os.popen("ss -tuln | grep -i LISTEN").readlines()
    else:
        return []

    for line in read_lines:
        if str(pid) in line:
            match = pattern.findall(line)
            ports.update(int(p[1:]) for p in match)

    return sorted(ports)


def check_string(string: str, value: Any, is_strict: bool = False) -> bool:
    """
    문자열 값 검증 함수.

    :param string: 검증할 문자열
    :param value: 비교할 값
    :param is_strict: 엄격한 비교 여부
    :return: 검증 결과
    """
    if not string:
        return False

    return string == value if is_strict else string.lower() == value.lower()


def check_is_empty_string(value: Any) -> bool:
    """주어진 값이 빈 문자열인지 확인하는 함수."""
    return isinstance(value, str) and not value.strip()


def is_valid_regex(value: str) -> bool:
    """정규 표현식의 유효성을 확인하는 함수."""
    try:
        re.compile(value)
        return True
    except re.error:
        return False


def check_value_is_dict(value: Any) -> bool:
    """주어진 값이 딕셔너리인지 확인하는 함수."""
    return isinstance(value, dict)


def check_value_is_list(value: Any) -> bool:
    """주어진 값이 리스트인지 확인하는 함수."""
    return isinstance(value, list)
