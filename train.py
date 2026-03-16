import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from huggingface_hub import HfApi, HfFolder, Repository
import os
import wandb
from datetime import datetime

class SimpleCatDogClassifier:
    def __init__(self, model_name="resnet18", num_classes=2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.num_classes = num_classes
        self.model = self._build_model()
        
    def _build_model(self):
        if self.model_name == "resnet18":
            model = models.resnet18(pretrained=True)
            model.fc = nn.Linear(model.fc.in_features, self.num_classes)
        return model.to(self.device)
    
    def train(self, train_loader, val_loader, epochs=5, lr=0.001):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        
        # 只有在有WandB API key时才初始化
        if os.getenv("WANDB_API_KEY"):
            wandb.init(project="cat-dog-classification", config={
                "learning_rate": lr,
                "epochs": epochs,
                "model": self.model_name
            })
        else:
            print("WandB API key not found, skipping WandB logging")
        
        best_val_acc = 0.0
        
        for epoch in range(epochs):
            self.model.train()
            running_loss = 0.0
            correct = 0
            total = 0
            
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                
                optimizer.zero_grad()
                output = self.model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item()
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
                
                if batch_idx % 10 == 0:
                    if os.getenv("WANDB_API_KEY"):
                        wandb.log({
                            "batch_loss": loss.item(),
                            "batch_accuracy": 100. * correct / total
                        })
                    else:
                        print(f"Batch {batch_idx}: Loss={loss.item():.4f}, Acc={100. * correct / total:.2f}%")
            
            train_acc = 100. * correct / total
            
            # 验证
            val_acc = self._validate(val_loader, criterion)
            
            if os.getenv("WANDB_API_KEY"):
                wandb.log({
                    "epoch": epoch,
                    "train_loss": running_loss / len(train_loader),
                    "train_accuracy": train_acc,
                    "val_accuracy": val_acc
                })
            else:
                print(f"Epoch {epoch+1}: Train Loss={running_loss / len(train_loader):.4f}, Train Acc={train_acc:.2f}%, Val Acc={val_acc:.2f}%")
            
            print(f'Epoch {epoch+1}/{epochs}: Train Acc: {train_acc:.2f}%, Val Acc: {val_acc:.2f}%')
            
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                self._save_checkpoint(f'best_model.pth')
        
        if os.getenv("WANDB_API_KEY"):
            wandb.finish()
        return best_val_acc
    
    def _validate(self, val_loader, criterion):
        self.model.eval()
        val_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                val_loss += criterion(output, target).item()
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        
        return 100. * correct / total
    
    def _save_checkpoint(self, filename):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_name': self.model_name,
            'num_classes': self.num_classes
        }, filename)
    
    def push_to_huggingface(self, repo_name, model_path="best_model.pth"):
        api = HfApi()
        
        # 创建模型卡片
        model_card = f"""
---
license: mit
tags:
- pytorch
- image-classification
- cats-dogs
---

# {repo_name}

这是一个简单的猫狗分类模型，使用ResNet18架构训练。

## 模型描述
- 架构: {self.model_name}
- 类别数: {self.num_classes}
- 训练时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 使用方法
```python
from transformers import AutoModelForImageClassification
model = AutoModelForImageClassification.from_pretrained("{repo_name}")
```

## 训练数据
使用标准的猫狗图像数据集进行训练。
"""
        
        # 上传到Hugging Face
        api.create_repo(
            repo_id=repo_name,
            token=HfFolder.get_token(),
            exist_ok=True,
            repo_type="model"
        )
        
        api.upload_file(
            path_or_fileobj=model_path,
            path_in_repo=f"{model_path}",
            repo_id=repo_name,
            token=HfFolder.get_token(),
            repo_type="model"
        )
        
        api.upload_file(
            path_or_fileobj=model_card.encode(),
            path_in_repo="README.md",
            repo_id=repo_name,
            token=HfFolder.get_token(),
            repo_type="model"
        )
        
        print(f"模型已成功上传到 Hugging Face: https://huggingface.co/{repo_name}")

def get_data_loaders(data_dir="./data", batch_size=32, img_size=224):
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    # 假设数据集结构: data/train/cats, data/train/dogs, data/val/cats, data/val/dogs
    train_dataset = datasets.ImageFolder(os.path.join(data_dir, "train"), transform=transform)
    val_dataset = datasets.ImageFolder(os.path.join(data_dir, "val"), transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader

if __name__ == "__main__":
    # 设置Hugging Face token (需要在环境变量中设置HF_TOKEN)
    if os.getenv("HF_TOKEN"):
        HfFolder.save_token(os.getenv("HF_TOKEN"))
    
    # 创建分类器
    classifier = SimpleCatDogClassifier()
    
    # 获取数据加载器
    train_loader, val_loader = get_data_loaders()
    
    # 训练模型
    best_acc = classifier.train(train_loader, val_loader, epochs=5)
    
    # 上传到Hugging Face
    if os.getenv("HF_TOKEN"):
        repo_name = "your-username/cat-dog-classifier"  # 替换为你的用户名
        classifier.push_to_huggingface(repo_name)
    else:
        print("未设置HF_TOKEN环境变量，跳过上传到Hugging Face")
