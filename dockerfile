FROM python3.12.2-slim

RUN apt-get update && apt-get install -y ffmpeg && 
    apt-get clean && rm -rf varlibaptlists

WORKDIR app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [python, app.py]
