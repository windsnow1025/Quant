import os

from dotenv import load_dotenv


def main():
    load_dotenv()
    api_key = os.environ.get("API_KEY")


if __name__ == "__main__":
    main()
