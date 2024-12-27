FROM python:3.12-slim

# 添加构建参数
ARG BUILDTIME=unknown

WORKDIR /app

# 首先复制 requirements.txt
COPY requirements.txt .

# 添加 no-cache 参数并使用 --no-cache-dir
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt && \
    # 强制更新 pip
    pip install --no-cache-dir --upgrade pip && \
    # 清除 pip 缓存
    pip cache purge && \
    # 安装最新版本的 p115tiny302
    pip install --no-cache-dir --upgrade p115tiny302 && \
    # 显示安装的版本
    pip show p115tiny302 | grep Version

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
    TZ=Asia/Shanghai \
    P115TINY302_COOKIES=""

# 设置权限
RUN chmod -R 755 /app

# 暴露端口
EXPOSE 8000 8001

# 启动应用
CMD ["python", "-u", "main.py"] 
