// 使用 import.meta.glob() 加载本地 images 文件夹中的图片文件
const images = import.meta.glob("/images/*.(png|jpg|jpeg|gif|svg)");

// 遍历 images 对象
for (const path in images) {
  // 通过路径获取加载函数
  const loadImage = images[path];
  // 加载图片并获取其 URL
  loadImage().then((module) => {
    const imageUrl = module.default;
    // 在这里可以使用 imageUrl，例如将其赋值给 img 标签的 src 属性
    console.log(`Image URL for ${path}:`, imageUrl);
  });
}
