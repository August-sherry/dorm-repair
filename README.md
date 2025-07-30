【宿舍智能报修系统 · README.md】

## 功能简介  
平台采用 B/S 架构，后端基于 **FastAPI + SQL Server**，前端基于 **Vue3 + TypeScript + Vite**。  
整个系统由「前台」与「后台」两部分组成：  

- **前台**  
  - 学生端：报修提交、工单追踪、五星评价  
  - 维修工端：登录、接单、完工、查看 KPI  

- **后台**  
  - 管理员：新增维修工、实时 KPI 排行、工单全览  

## 演示地址  
- 前台（学生/维修工）：[http](http://localhost:5173/select-role)
- 后台（管理员）：http://localhost:5173/admin/login

后台演示账号：  
管理员口令：`111` 

## 代码结构  
```
.
├── backend/          # FastAPI 后端
├── frontend/         # Vue3 + TypeScript 前端
```

## 部署运行

### 后端（FastAPI）
1. 安装 Python 3.11  
2. 进入 `backend` 目录，安装依赖  
   ```bash
   pip install -r requirements.txt
   ```
3. 安装 SQL Server 2019，新建数据库 `dorm`  
   ```sql
   CREATE DATABASE dorm;
   ```
4. 执行脚本初始化数据  
   ```bash
   python init_db.py
   ```
5. 启动服务  
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### 前端（Vue3）
1. 安装 Node 18+  
2. 进入 `frontend` 目录，安装依赖  
   ```bash
   npm install
   ```
3. 启动开发服务器  
   ```bash
   npm run dev
   ```

服务启动后，浏览器访问对应端口即可体验完整功能。
