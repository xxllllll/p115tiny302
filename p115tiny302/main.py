import os
import sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import unquote
import re
from datetime import datetime
from collections import deque
import asyncio
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI()

# 设置静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 日志存储
logs = deque(maxlen=100)

def add_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append({"timestamp": timestamp, "message": message})
    logger.info(message)

def log_request(host: str, method: str, path: str, status_code: int):
    try:
        path = unquote(path)
    except:
        pass
    add_log(f"{host} - {method} {path} - {status_code}")

# 路由处理
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/logs")
async def get_logs():
    return list(logs)

class UvicornLogFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return any((
            '302' in msg,
            '404' in msg,
            'Starting' in msg,
            'Application' in msg,
            'Error' in msg,
            'Exception' in msg,
            'Cookies length' in msg,
            'pickcode' in msg.lower(),
            'Uvicorn running' in msg,
            'Started server process' in msg,
            'Waiting for application startup' in msg,
            'Application startup complete' in msg
        ))

async def run_302_service():
    try:
        cookies = os.getenv('COOKIES', '')
        if not cookies and os.path.exists('115-cookies.txt'):
            with open('115-cookies.txt', 'r') as f:
                cookies = f.read().strip()
        
        add_log("Starting 302 service...")
        add_log(f"Cookies length: {len(cookies)}")
        
        from p115tiny302 import make_application, Client
        from blacksheep.server.responses import Response
        from functools import wraps
        
        # 创建 client 实例并传递给 make_application
        client = Client(cookies)
        app_302 = make_application(client)

        # 为blacksheep应用添加日志记录
        original_handle = app_302.handle

        @wraps(original_handle)
        async def handle_with_logging(request):
            try:
                response = await original_handle(request)
                if isinstance(response, Response):
                    if response.status in [302, 404] or 'pickcode' in str(request.url):
                        log_request(
                            request.client_ip,
                            request.method,
                            str(request.url),
                            response.status
                        )
                return response
            except Exception as e:
                error_msg = str(e)
                if "FileNotFoundError" in error_msg:
                    log_request(
                        request.client_ip,
                        request.method,
                        str(request.url),
                        404
                    )
                    return Response(404, content="File not found")
                else:
                    add_log(f"Error handling request: {error_msg}")
                    raise

        app_302.handle = handle_with_logging

        # 配置uvicorn日志
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(message)s"
        log_config["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
        
        config = uvicorn.Config(
            app_302, 
            host="0.0.0.0", 
            port=8000,
            log_config=log_config,
            access_log=True
        )
        server = uvicorn.Server(config)
        
        # 添加日志过滤器
        for handler in logging.getLogger("uvicorn").handlers:
            handler.addFilter(UvicornLogFilter())
        
        await server.serve()
    except Exception as e:
        add_log(f"Error in 302 service: {str(e)}")
        raise

async def run_web_interface():
    # 配置uvicorn日志
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(message)s"
    log_config["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8001,
        log_config=log_config,
        access_log=True
    )
    server = uvicorn.Server(config)
    
    # 添加日志过滤器
    for handler in logging.getLogger("uvicorn").handlers:
        handler.addFilter(UvicornLogFilter())
    
    await server.serve()

async def main():
    # 并发运行两个服务
    await asyncio.gather(
        run_302_service(),
        run_web_interface()
    )

if __name__ == "__main__":
    asyncio.run(main())
