function updateLogs() {
    fetch('/api/logs')
        .then(response => response.json())
        .then(logs => {
            const logContent = document.getElementById('logContent');
            if (logs && logs.length > 0) {
                const newHtml = logs.map(log => `
                    <div class="log-entry">
                        <span class="timestamp">${log.timestamp}</span>
                        <span class="message">${log.message}</span>
                    </div>
                `).join('');
                
                // 只有当内容变化时才更新
                if (logContent.innerHTML !== newHtml) {
                    logContent.innerHTML = newHtml;
                    // 滚动到底部
                    logContent.scrollTop = logContent.scrollHeight;
                }
            } else {
                logContent.innerHTML = `
                    <div class="log-entry">
                        <span class="message">等待日志...</span>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching logs:', error);
            const logContent = document.getElementById('logContent');
            logContent.innerHTML = `
                <div class="log-entry error">
                    <span class="message">获取日志失败: ${error.message}</span>
                </div>
            `;
        });
}

// 页面加载完成后立即更新一次
document.addEventListener('DOMContentLoaded', () => {
    updateLogs();
});

// 每1秒更新一次日志
setInterval(updateLogs, 1000);

// 添加页面可见性检测
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        updateLogs();
    }
}); 