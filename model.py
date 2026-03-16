import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

class CatDogModel:
    def __init__(self, model_path="best_model.pth", num_classes=2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path, num_classes)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        self.class_names = ["cat", "dog"]
    
    def _load_model(self, model_path, num_classes):
        model = models.resnet18(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        
        if os.path.exists(model_path):
            checkpoint = torch.load(model_path, map_location=self.device)
            model.load_state_dict(checkpoint['model_state_dict'])
            print(f"模型已从 {model_path} 加载")
        else:
            print(f"警告: 未找到模型文件 {model_path}")
        
        model = model.to(self.device)
        model.eval()
        return model
    
    def predict(self, image_path):
        if isinstance(image_path, str):
            image = Image.open(image_path).convert('RGB')
        else:
            image = image_path
        
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            result = {
                'predicted_class': self.class_names[predicted.item()],
                'confidence': confidence.item() * 100,
                'probabilities': {
                    self.class_names[i]: prob.item() * 100 
                    for i, prob in enumerate(probabilities[0])
                }
            }
        
        return result
    
    def predict_batch(self, image_paths):
        results = []
        for image_path in image_paths:
            result = self.predict(image_path)
            results.append(result)
        return results

# 使用示例
if __name__ == "__main__":
    import os
    
    # 创建模型实例
    model = CatDogModel()
    
    # 示例预测
    test_image = "test_dog.jpg"  # 替换为实际图片路径
    if os.path.exists(test_image):
        result = model.predict(test_image)
        print(f"预测结果: {result['predicted_class']}")
        print(f"置信度: {result['confidence']:.2f}%")
        print(f"详细概率: {result['probabilities']}")
    else:
        print(f"测试图片 {test_image} 不存在")
