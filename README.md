# 监听8080端口的Python服务器

这个项目包含了三种不同类型的服务器，都监听8080端口来接收消息：

## 1. HTTP服务器 (http_server.py)

基于HTTP协议的服务器，适合处理REST API请求。

### 功能特性：
- 支持GET和POST请求
- 自动解析JSON和文本消息
- 支持CORS跨域请求
- 提供详细的请求日志

### 启动服务器：
```bash
python http_server.py
```

### 测试示例：
```bash
# GET请求测试
curl "http://localhost:8080/test?param1=value1&param2=value2"

# POST JSON消息测试
curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{"type": "test", "message": "Hello Server", "data": {"key": "value"}}'

# POST文本消息测试
curl -X POST http://localhost:8080/message \
     -H "Content-Type: text/plain" \
     -d "这是一条文本消息"
```

## 2. TCP服务器 (tcp_server.py)

基于TCP协议的服务器，适合处理原始TCP连接和消息。

### 功能特性：
- 支持多客户端并发连接
- 自动解析JSON和文本消息
- 提供实时消息处理
- 包含测试客户端

### 启动服务器：
```bash
python tcp_server.py
```

### 运行测试客户端：
```bash
python tcp_server.py client
```

### 使用telnet测试：
```bash
telnet localhost 8080
# 然后输入消息，如：
# Hello TCP Server!
# {"type": "test", "message": "JSON消息"}
```

## 3. WebSocket服务器 (websocket_server.py)

基于WebSocket协议的服务器，适合实时双向通信。

### 功能特性：
- 支持实时双向通信
- 消息广播功能
- 自动解析JSON和文本消息
- 客户端管理

### 安装依赖：
```bash
pip install websockets
```

### 启动服务器：
```bash
python websocket_server.py
```

### 运行测试客户端：
```bash
python websocket_server.py client
```

### 在浏览器中测试：
打开浏览器控制台，运行以下JavaScript代码：
```javascript
// 连接WebSocket
const ws = new WebSocket('ws://localhost:8080');

ws.onopen = function() {
    console.log('WebSocket连接成功');
    
    // 发送消息
    ws.send(JSON.stringify({
        type: 'echo',
        message: '这是一条测试消息'
    }));
};

ws.onmessage = function(event) {
    console.log('收到消息:', JSON.parse(event.data));
};

// 广播消息示例
ws.send(JSON.stringify({
    type: 'broadcast',
    message: '这条消息将广播给所有客户端'
}));
```

## 服务器选择建议：

1. **HTTP服务器**: 
   - 适合REST API、Web服务
   - 无状态请求-响应模式
   - 易于测试和调试

2. **TCP服务器**: 
   - 适合自定义协议
   - 需要持久连接
   - 高性能要求

3. **WebSocket服务器**: 
   - 适合实时应用
   - 需要双向通信
   - Web浏览器兼容性好

## 消息格式示例：

### JSON消息格式：
```json
{
    "type": "message_type",
    "message": "消息内容",
    "data": {
        "key": "value",
        "timestamp": "2025-01-01T12:00:00"
    }
}
```

### 服务器响应格式：
```json
{
    "status": "success",
    "message": "消息已接收",
    "received_data": {...},
    "timestamp": "2025-01-01T12:00:00"
}
```

## 常见问题：

1. **端口被占用**：
   - 检查是否有其他程序使用8080端口
   - 使用 `lsof -i :8080` 查看端口使用情况
   - 可以修改代码中的端口号

2. **防火墙问题**：
   - 确保防火墙允许8080端口访问
   - 本地测试建议临时关闭防火墙

3. **依赖问题**：
   - WebSocket服务器需要安装websockets库
   - HTTP和TCP服务器使用Python标准库，无需额外安装