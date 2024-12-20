# 115网盘302跳转服务 Docker版

这是一个基于Docker的115网盘302跳转服务，使用 p115tiny302 包提供302跳转功能，并提供Web界面查看运行日志。

![Docker Build Status](https://github.com/xxllllll/p115tiny302/actions/workflows/docker-build.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/xxllllll/p115tiny302)
![Docker Image Version](https://img.shields.io/docker/v/xxllllll/p115tiny302/latest)

## 功能特点

- 支持115网盘文件的302跳转
- 实时显示运行日志的Web界面
- 支持Docker部署
- 自动保存最近100条日志记录
- 使用官方 p115tiny302 包
- 自动跟踪 p115tiny302 版本更新

## 快速开始

### 使用 Docker Pull

```bash
# 拉取最新版本
docker pull xxllllll/p115tiny302:latest

# 或指定版本
docker pull xxllllll/p115tiny302:x.y.z
```

### 运行容器

1. 准备cookies文件：
   将115网盘的cookies保存到文件 `115-cookies.txt` 中

2. 运行容器：
   ```bash
   docker run -d \
     -p 8000:8000 \
     -p 8001:8001 \
     -v /path/to/115-cookies.txt:/app/115-cookies.txt \
     --name p115tiny302 \
     xxllllll/p115tiny302
   ```

### 从源码构建

1. 克隆仓库：
   ```bash
   git clone https://github.com/xxllllll/p115tiny302.git
   cd p115tiny302
   ```

2. 构建镜像：
   ```bash
   docker build -t p115tiny302 .
   ```

3. 运行容器：
   ```bash
   docker run -d \
     -p 8000:8000 \
     -p 8001:8001 \
     -v /path/to/115-cookies.txt:/app/115-cookies.txt \
     --name p115tiny302 \
     p115tiny302
   ```

## 服务访问

- 302跳转服务：http://localhost:8000
- Web管理界面：http://localhost:8001

## 自动构建

本项目通过 GitHub Actions 实现自动化构建和发布：

- 每天北京时间凌晨 0 点自动检查 PyPI 更新
- 发现新版本时自动构建并推送到 Docker Hub
- 使用 p115tiny302 的版本号作为 Docker 标签
- 支持手动触发构建
- 使用 Docker 层缓存加速构建
- 避免重复构建相同版本

## 环境要求

- Docker
- 有效的115网盘cookies

## 版本说明

Docker 镜像版本与 p115tiny302 包版本保持一致。例如：
- `latest`: 最新版本
- `0.0.3`: 对应 p115tiny302 0.0.3 版本

## 注意事项

1. 确保cookies文件格式正确
2. 8000端口用于302跳转服务
3. 8001端口用于Web管理界面
4. 容器会自动保存最近100条日志记录
5. 建议使用具体版本标签而不是 latest 标签

## 贡献指南

欢迎提交 Issue 和 Pull Request。在提交 PR 之前，请确保：

1. 代码风格符合项目规范
2. 添加必要的测试
3. 更新相关文档

## 许可证

MIT License

## 相关链接

- [p115tiny302 PyPI](https://pypi.org/project/p115tiny302/)
- [Docker Hub 仓库](https://hub.docker.com/r/xxllllll/p115tiny302)
- [GitHub 仓库](https://github.com/xxllllll/p115tiny302)

## 更新日志

### 最新版本
- 添加自动构建支持
- 优化日志记录
- 改进错误处理
- 支持 Docker 层缓存
