# 猫狗分类器 - ML项目示例

这是一个简单的机器学习项目，演示如何：
- 训练一个PyTorch图像分类模型
- 使用GitHub Actions自动化训练流程
- 自动上传模型到Huggingface Hub

## 项目特点

- 🐱 **简单实用**: 使用ResNet18进行猫狗图像分类
- 🚀 **自动化部署**: GitHub Actions自动训练和上传
- 🤗 **Hugging Face集成**: 模型自动发布到Hugging Face Hub
- 📊 **实验跟踪**: 集成WandB记录训练过程

## 📋 项目结构

```
ml-project-huggingface/
├── train.py              # 模型训练脚本
├── upload_to_hf.py       # 上传到Huggingface的脚本
├── model.py              # 模型推理脚本
├── requirements.txt      # Python依赖
├── .github/workflows/    # GitHub Actions配置
│   ├── train-and-upload.yml  # 完整训练+上传工作流
│   └── upload-hf.yml         # 单独上传工作流
├── data/                 # 数据目录
│   ├── train/           # 训练数据
│   └── val/             # 验证数据
└── best_model.pth       # 训练后的模型文件（自动生成）
```

## 🚀 快速开始

### 本地运行

1. **安装依赖**：
```bash
pip install -r requirements.txt
```

2. **训练模型**：
```bash
python train.py
```

3. **模型将保存为** `best_model.pth`

### 设置GitHub Actions自动化

1. **Fork或创建此仓库**

2. **获取Huggingface Token**
   - 访问 https://huggingface.co/settings/tokens
   - 创建一个新的token（需要写入权限）

3. **在GitHub中设置Secret**
   - 进入你的仓库 → Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - 名称: `HF_TOKEN`
   - 值: 粘贴你的Huggingface token

4. **修改配置**
   - 编辑 `upload_to_hf.py` 文件
   - 将 `wzx952` 改为你的Huggingface用户名

5. **触发工作流**
   - 推送代码到main分支，或
   - 在GitHub Actions页面手动触发

## GitHub Actions自动部署

### 设置Secrets

在GitHub仓库设置中添加以下Secrets：

- `HF_TOKEN`: Hugging Face访问令牌
- `HF_USERNAME`: Hugging Face用户名
- `WANDB_API_KEY`: WandB API密钥（可选）

### 工作流程

1. **触发条件**: 推送到main/master分支或手动触发
2. **环境设置**: Ubuntu + Python 3.9
3. **依赖安装**: 自动安装所有必需包
4. **模型训练**: 运行训练脚本
5. **自动上传**: 训练完成后上传到Hugging Face Hub

## Hugging Face模型

训练完成后，模型会自动上传到：
`https://huggingface.co/YOUR_USERNAME/cat-dog-classifier`

### 使用Hugging Face模型

```python
from transformers import AutoModelForImageClassification, AutoFeatureExtractor

# 加载模型
model = AutoModelForImageClassification.from_pretrained("YOUR_USERNAME/cat-dog-classifier")
feature_extractor = AutoFeatureExtractor.from_pretrained("YOUR_USERNAME/cat-dog-classifier")

# 预测
from PIL import Image
image = Image.open("path/to/image.jpg")
inputs = feature_extractor(image, return_tensors="pt")
outputs = model(**inputs)
predicted_class_idx = outputs.logits.argmax(-1).item()
```

## 模型架构

- **骨干网络**: ResNet18 (预训练)
- **分类头**: 全连接层 (2类输出)
- **输入尺寸**: 224x224 RGB图像
- **优化器**: Adam (lr=0.001)
- **损失函数**: 交叉熵损失

## 性能指标

- 训练轮数: 5
- 批次大小: 32
- 验证准确率: 训练后自动记录

## 扩展建议

1. **数据增强**: 添加更多数据增强技术
2. **模型优化**: 尝试其他架构如EfficientNet
3. **超参数调优**: 使用Optuna等工具
4. **部署应用**: 创建Gradio或Streamlit应用
5. **模型量化**: 减小模型大小用于移动端

## 贡献指南

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 致谢

- [PyTorch](https://pytorch.org/)
- [Hugging Face](https://huggingface.co/)
- [WandB](https://wandb.ai/)
- [GitHub Actions](https://github.com/features/actions)
