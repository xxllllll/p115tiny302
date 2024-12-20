# 115网盘302跳转服务 Docker版

这是一个基于Docker的115网盘302跳转服务，使用 p115tiny302 包提供302跳转功能，并提供Web界面查看运行日志。

## 功能特点

- 支持115网盘文件的302跳转
- 实时显示运行日志的Web界面
- 支持Docker部署
- 自动保存最近100条日志记录
- 使用官方 p115tiny302 包

## 使用方法

1. 准备cookies文件：
   将115网盘的cookies保存到文件 `115-cookies.txt` 中

2. 构建Docker镜像：
   ```bash
   docker build -t 115-302 .
   ```

3. 运行容器：
   ```bash
   docker run -d \
     -p 8000:8000 \
     -p 8001:8001 \
     -v /path/to/115-cookies.txt:/app/115-cookies.txt \
     --name 115-302 \
     115-302
   ```

4. 访问服务：
   - 302跳转服务：http://localhost:8000
   - Web管理界面：http://localhost:8001

## 环境要求

- Docker
- Python 3.12+
- 有效的115网盘cookies

## 注意事项

1. 确保cookies文件格式正确
2. 8000端口用于302跳转服务
3. 8001端口用于Web管理界面
4. 容器会自动保存最近100条日志记录
