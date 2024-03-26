from torch.utils.data import Dataset
from torchvision import transforms
import torch
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

class HotdogOrNotDataset(Dataset):
    def __init__(self, folder):
        self.folder = folder
        self.transform = transform
        self.images = tuple(os.listdir(folder))
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, index):        
        img, y, img_id = None, None, None
        labels = {'hotdog': 1,
                   'not_hotdog': 0,
                   }
        img_id = self.images[index]
        img_name = os.path.join(self.folder, img_id)
        img = Image.open(img_name).convert('RGB')
        for keyword, label in labels.items():
            if keyword in img_id:
                y = np.array([1., 0.])
                break
        else:
            y = np.array([0., 1.])

        if self.transform:
            img = self.transform(img)
        return img, label, img_id
    
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(), 
])

def visualize_samples(dataset, indices, title=None, img_titles=None, count=10):
    # visualize random 10 samples
    plt.figure(figsize=(count*3,3))
    display_indices = indices[:count]
    if title:
        plt.suptitle("%s %s/%s" % (title, len(display_indices), len(indices)))        
    for i, index in enumerate(display_indices):    
        x, y, _ = dataset[index]
        plt.subplot(1,count,i+1)
        if img_titles:
            plt.title("Label: %s \n %s" % (y, img_titles[i]))
        else:
            plt.title("Label: %s" % y)
        plt.grid(False)
        plt.axis('off')
        if x.mode == 'RGB':
            plt.imshow(x)
        else:
            plt.imshow(transforms.functional.to_pil_image(x), cmap='Greys')
    plt.show()
