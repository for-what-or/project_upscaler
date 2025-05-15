from PIL import Image
import torch
import torchvision.transforms as transforms
from spandrel import ImageModelDescriptor, ModelLoader

def load_sr_model(model_path):
    """Загрузка модели"""
    model = ModelLoader().load_from_file(model_path)
    assert isinstance(model, ImageModelDescriptor)
    return model

def split_image(image, tile_size=256, padding=32):
    """Разбивает изображение на тайлы"""
    w, h = image.size
    tiles = []
    positions = []
    
    padded_img = Image.new("RGB", (w + 2*padding, h + 2*padding))
    padded_img.paste(image, (padding, padding))
    
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            left = x
            top = y
            right = min(x + tile_size + 2*padding, w + 2*padding)
            bottom = min(y + tile_size + 2*padding, h + 2*padding)
            
            tile = padded_img.crop((left, top, right, bottom))
            tiles.append(transforms.ToTensor()(tile).unsqueeze(0).cuda())
            positions.append((x, y, min(x + tile_size, w), min(y + tile_size, h)))
    return tiles, positions

def merge_tiles(tiles, positions, original_size, scale=4):
    """Собирает тайлы обратно в одно изображение"""
    w, h = original_size
    result = torch.zeros((3, h*scale, w*scale)).cuda()
    
    for tile, (x, y, x2, y2) in zip(tiles, positions):
        px = 32 * scale
        py = 32 * scale
        cropped = tile[:, :, py:-py or None, px:-px or None]
        result[:, y*scale:(y2)*scale, x*scale:(x2)*scale] = cropped.squeeze(0)

    return result