FROM python:3.12-slim

WORKDIR /app

# 首先复制 requirements.txt
COPY requirements.txt .

# 安装依赖并清理缓存
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir p115tiny302==$(pip index versions p115tiny302 | grep -m1 'Available versions:' | grep -oP '\d+\.\d+\.\d+' | head -1)

# 创建必要的目录
RUN mkdir -p /app/static /app/templates

# 复制静态文件和模板
COPY static /app/static
COPY templates /app/templates

# 复制主程序
COPY main.py .

# 创建cookies文件
RUN touch /app/115-cookies.txt && \
    chmod 666 /app/115-cookies.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    TZ=Asia/Shanghai

# 设置权限
RUN chmod -R 755 /app

# 暴露端口
EXPOSE 8000 8001

# 启动应用
CMD ["python", "-u", "main.py"] 