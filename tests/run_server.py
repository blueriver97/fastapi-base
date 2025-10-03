import argparse

import uvicorn


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--port", type=int, default=9090)
    parser.add_argument("-R", "--reload", type=bool, default=True)
    parser.add_argument("--env_file", type=str, default=".env")
    return parser.parse_args()


if __name__ == "__main__":
    args = args_parse()

    uvicorn.run(
        "base.api:http_app",
        host="0.0.0.0",
        port=args.port,
        reload=args.reload,
        reload_includes="timestamp.tmp",
        env_file=args.env_file,
        reload_dirs=["../src/base"],
    )
