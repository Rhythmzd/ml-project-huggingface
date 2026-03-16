"""
猫狗智能识别系统 - 模型自动上传模块
将训练好的模型自动发布到Hugging Face Hub
"""
import os
import time
from huggingface_hub import HfApi, create_repo, login

def upload_model():
    """上传模型到Huggingface"""
    # 从环境变量获取token
    token = os.environ.get('HF_TOKEN')
    if not token:
        raise ValueError("❌ 未找到 HF_TOKEN 环境变量！请在GitHub Secrets中设置。")
    
    # 配置
    repo_id = "wzx952/cat-dog-classifier"  # 你的Huggingface用户名
    
    print(f"�🐶 猫狗智能识别系统 - 开始上传模型到 {repo_id}...")
    print(f"🔑 Token前缀: {token[:10]}...")
    
    # 先登录
    try:
        login(token=token)
        print("✅ Huggingface登录成功")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        raise
    
    # 创建API实例
    api = HfApi(token=token)
    
    # 创建仓库（如果不存在）
    try:
        url = create_repo(
            repo_id=repo_id,
            token=token,
            repo_type="model",
            exist_ok=True,
            private=False
        )
        print(f"✅ 仓库已创建/确认: {repo_id}")
        print(f"📍 仓库URL: {url}")
        
        # 等待仓库完全创建
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️  创建仓库时出现问题: {e}")
        print(f"⚠️  尝试继续上传...")
    
    # 上传模型文件
    try:
        print("📤 开始上传文件...")
        api.upload_file(
            path_or_fileobj="best_model.pth",
            path_in_repo="best_model.pth",
            repo_id=repo_id,
            repo_type="model",
            token=token,
            commit_message="🐱🐶 猫狗智能识别系统 - 自动训练与部署"
        )
        print(f"✅ 模型已成功上传到 https://huggingface.co/{repo_id}")
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        print(f"💡 请检查:")
        print(f"   1. Token是否有写入权限")
        print(f"   2. 用户名是否正确: wxz952")
        print(f"   3. 是否已在Huggingface登录")
        raise
    
    # 上传README
    readme_content = """---
license: mit
tags:
- pytorch
- image-classification
- cats-dogs
- resnet18
---

# Cat Dog Classifier

这是一个简单的猫狗分类模型，使用ResNet18架构训练。

## 模型信息
- **架构**: ResNet18 (预训练)
- **输入**: 224x224 RGB图像
- **输出**: 猫/狗二分类
- **训练框架**: PyTorch
- **训练环境**: GitHub Actions

## 使用方法

### 方法1：直接加载PyTorch模型
```python
import torch
from torchvision import transforms
from PIL import Image

# 加载模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load("best_model.pth", map_location=device)
model.eval()

# 预测
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

image = Image.open("your_image.jpg")
input_tensor = transform(image).unsqueeze(0).to(device)

with torch.no_grad():
    output = model(input_tensor)
    probabilities = torch.nn.functional.softmax(output, dim=1)
    predicted_class = "cat" if probabilities[0][0] > 0.5 else "dog"
    confidence = max(probabilities[0][0].item(), probabilities[0][1].item()) * 100

print(f"预测结果: {predicted_class}")
print(f"置信度: {confidence:.2f}%")
```

### 方法2：使用Hugging Face Hub
```python
from huggingface_hub import hf_hub_download
import torch

# 下载模型
model_path = hf_hub_download(repo_id="wzx952/cat-dog-classifier", filename="best_model.pth")
model = torch.load(model_path)
model.eval()
```

## 训练数据
- 使用标准的猫狗图像数据集进行训练
- 训练集：10张猫图片 + 10张狗图片（演示用）
- 验证集：5张猫图片 + 5张狗图片（演示用）

## 训练参数
- **优化器**: Adam (lr=0.001)
- **损失函数**: 交叉熵损失
- **训练轮数**: 5
- **批次大小**: 32

## 项目信息
- **GitHub仓库**: https://github.com/Rhythmzd/ml-project-huggingface
- **CI/CD**: GitHub Actions自动训练和部署
- **Hugging Face**: 自动上传模型和文档

## 演示说明
⚠️ **注意**: 这是一个演示项目，使用随机生成的虚拟数据进行训练。实际使用时需要替换为真实的猫狗图像数据集。

## 许可证
MIT License
"""
    
    try:
        api.upload_file(
            path_or_fileobj=readme_content.encode(),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="model",
            token=token,
            commit_message="📝 添加模型文档"
        )
        print("✅ README上传成功")
    except Exception as e:
        print(f"❌ README上传失败: {e}")

if __name__ == "__main__":
    upload_model()
