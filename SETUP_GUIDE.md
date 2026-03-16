# 🚀 项目部署详细指南

## 📋 步骤概览
1. ✅ Git仓库初始化（已完成）
2. ✅ GitHub仓库创建（已完成）
3. 🔲 获取Hugging Face Token
4. 🔲 配置GitHub Secrets
5. 🔲 测试GitHub Actions

---

## 🔑 步骤3：获取Hugging Face Token

### 方法1：直接访问
```
https://huggingface.co/settings/tokens
```

### 方法2：通过导航
1. 访问 https://huggingface.co
2. 点击右上角你的头像
3. 选择 "Settings"
4. 在左侧菜单找到 "Access Tokens"
5. 点击 "New token"

### 创建Token步骤：
1. **Name**: 输入 `ml-project-token`
2. **Role**: 选择 `Write` （这允许上传模型）
3. 点击 "Generate a token"
4. **立即复制token**（只显示一次！）

---

## 🔐 步骤4：配置GitHub Secrets

### 访问仓库设置：
1. 打开：https://github.com/Rhythmzd/ml-project-huggingface
2. 点击绿色的 "Settings" 按钮
3. 在左侧菜单找到：
   - "Secrets and variables" 
   - 点击 "Actions"

### 添加Secrets：
点击 "New repository secret"，逐个添加：

#### 1. HF_TOKEN
- **Name**: `HF_TOKEN`
- **Secret**: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` （你复制的token）

#### 2. HF_USERNAME  
- **Name**: `HF_USERNAME`
- **Secret**: `Rhythmzd`

#### 3. WANDB_API_KEY（可选）
- **Name**: `WANDB_API_KEY`
- **Secret**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` （WandB的API key）

---

## 🎯 步骤5：触发GitHub Actions

配置完成后，有两种方式触发训练：

### 方法1：手动触发
1. 访问：https://github.com/Rhythmzd/ml-project-huggingface/actions
2. 点击左侧的 "Train Model and Deploy to Hugging Face"
3. 点击 "Run workflow" 按钮
4. 点击绿色的 "Run workflow"

### 方法2：推送代码触发
```bash
# 在项目目录下执行
echo "# 触发训练" >> README.md
git add README.md
git commit -m "Trigger training"
git push origin main
```

---

## 📊 监控训练进度

训练过程可以在GitHub Actions页面实时查看：
- 访问：https://github.com/Rhythmzd/ml-project-huggingface/actions
- 点击正在运行的工作流
- 可以看到训练日志和进度

---

## 🎉 完成后

训练成功后，你的模型会出现在：
```
https://huggingface.co/Rhythmzd/cat-dog-classifier
```

---

## ❓ 常见问题

### Q: 找不到Hugging Face token页面？
A: 确保你已经登录Hugging Face账户，token页面地址是：https://huggingface.co/settings/tokens

### Q: GitHub Secrets页面找不到？
A: 在仓库页面点击 "Settings" → 左侧 "Secrets and variables" → "Actions"

### Q: 训练失败了怎么办？
A: 检查GitHub Actions的错误日志，通常是因为：
- HF_TOKEN未设置或错误
- 网络连接问题
- 依赖包安装失败

---

## 🆘 需要帮助？

如果遇到任何问题，请告诉我：
1. 你卡在哪一步？
2. 看到什么错误信息？
3. 我可以帮你具体解决！
