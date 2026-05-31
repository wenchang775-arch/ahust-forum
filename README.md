# 安徽理工大学校园贴吧

一个专为安徽理工大学师生打造的校园交流社区平台。

## 功能特性

- **用户系统**：注册、登录、个人资料管理
- **板块分类**：校园生活、学习交流、社团活动、二手交易、求职招聘、情感交流
- **帖子功能**：发布、浏览、搜索帖子，支持置顶和精华帖标记
- **互动功能**：评论、点赞、回复
- **响应式设计**：适配各种设备屏幕

## 技术栈

### 后端
- Python Flask
- SQLite 数据库
- Flask-JWT-Extended 认证
- Flask-CORS 跨域支持

### 前端
- Vue 3
- Element Plus UI组件库
- Vue Router 路由管理
- Axios HTTP请求

## 安装与运行

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

后端服务将在 http://localhost:5000 运行

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

前端服务将在 http://localhost:8080 运行

## 使用说明

1. 访问 http://localhost:8080 进入首页
2. 点击右上角"注册"创建账号
3. 登录后可以发布帖子、评论互动
4. 浏览不同板块的内容
5. 使用搜索功能查找感兴趣的帖子

## 项目结构

```
ahust-forum/
├── backend/           # 后端代码
│   ├── app.py        # Flask应用主文件
│   └── requirements.txt
├── frontend/          # 前端代码
│   ├── public/
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面视图
│   │   ├── router/      # 路由配置
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
└── README.md
```

## 默认账号

系统初始化时没有默认账号，需要用户自行注册。

## 注意事项

- 首次运行后端会自动创建SQLite数据库和初始板块数据
- 请确保后端服务先启动，再启动前端
- 建议使用现代浏览器访问以获得最佳体验

## 开发团队

安徽理工大学校园贴吧开发团队

## 许可证

MIT License