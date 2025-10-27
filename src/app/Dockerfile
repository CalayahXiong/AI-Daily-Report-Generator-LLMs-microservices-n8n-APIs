FROM python:3.10-slim

WORKDIR /src/app
# copy this file into docker image
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# copy source code of this project
COPY . .

# expose the port for accessing the running workflow
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
