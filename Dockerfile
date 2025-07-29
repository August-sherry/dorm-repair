# 使用官方 Python 镜像
FROM python:3.11-slim

# 工作目录
WORKDIR /app

# 复制并安装依赖
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# 复制后端源码
COPY backend /app

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]