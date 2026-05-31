# 部署到 Render（免费24小时在线）

## 准备工作

1. 注册 [GitHub](https://github.com) 账号
2. 注册 [Render](https://render.com) 账号（用GitHub登录）
3. 将本项目代码推送到GitHub仓库

## 步骤一：创建GitHub仓库

```bash
# 在项目根目录初始化git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 在GitHub上创建新仓库，然后关联推送
git remote add origin https://github.com/你的用户名/ahust-forum.git
git push -u origin main
```

## 步骤二：部署后端服务

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. 点击 "New +" → "Web Service"
3. 选择你的GitHub仓库
4. 填写配置：
   - **Name**: `ahust-forum-backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
5. 点击 "Advanced" 添加环境变量：
   - `JWT_SECRET_KEY`: 随机生成的密钥（可用 `openssl rand -base64 32` 生成）
   - `FLASK_ENV`: `production`
6. 点击 "Create Web Service"

## 步骤三：部署前端服务

1. 在Render Dashboard点击 "New +" → "Static Site"
2. 选择同一个GitHub仓库
3. 填写配置：
   - **Name**: `ahust-forum-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
4. 点击 "Advanced" 添加环境变量：
   - `VUE_APP_API_URL`: `https://ahust-forum-backend.onrender.com`（替换为你的后端地址）
5. 点击 "Create Static Site"

## 步骤四：配置完成后

- **前端访问地址**: `https://ahust-forum-frontend.onrender.com`
- **后端API地址**: `https://ahust-forum-backend.onrender.com`

## 注意事项

### Render免费版限制
- **休眠**: 15分钟无访问会休眠，下次访问需要10-30秒唤醒
- **流量**: 每月100GB带宽
- **存储**: 1GB磁盘空间（已配置）

### 数据库说明
- 使用SQLite，数据存储在磁盘上
- 免费版重启后数据会保留（因为配置了磁盘）

### 图片上传
- 图片保存在服务器磁盘上
- 免费版重启后图片不会丢失

## 更新部署

每次代码更新后，推送到GitHub，Render会自动重新部署：

```bash
git add .
git commit -m "更新内容"
git push
```

## 替代方案

如果Render部署遇到问题，也可以尝试：
- [Railway](https://railway.app) - 类似Render，每月500小时免费
- [Vercel](https://vercel.com) + [Supabase](https://supabase.com) - 前端+后端分离方案
