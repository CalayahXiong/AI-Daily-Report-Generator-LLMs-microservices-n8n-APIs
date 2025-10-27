# 使用官方轻量 Python 3.10 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /src/app

# 复制依赖文件，先安装依赖，提高构建缓存利用率
COPY requirements.txt .

# 升级 pip 并安装依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目源代码
COPY . .

# 暴露端口
EXPOSE 8000

# 默认启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
