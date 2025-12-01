import os
import shutil
from PIL import Image
from pathlib import Path

# ========== 配置区域 ==========
# 1. 你的原始证书文件夹路径（根据你的描述修改）
SOURCE_CERT_DIR = Path(r"C:\Users\86185\Desktop\证书")
# 2. 你的GitHub项目目录路径（克隆仓库后，填写实际路径）
TARGET_PROJECT_DIR = Path(r"C:\Users\86185\certificates")
# 3. 证书在网页上的最大显示宽度（像素）
MAX_IMAGE_WIDTH = 800
# =============================

# 目标目录路径
TARGET_CERT_DIR = TARGET_PROJECT_DIR / "certificates"
TARGET_CERT_DIR.mkdir(parents=True, exist_ok=True)

def process_and_copy_certificates():
    """处理并复制证书图片到项目目录"""
    print("正在处理证书图片...")
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    cert_files = []
    
    for file_path in SOURCE_CERT_DIR.iterdir():
        if file_path.suffix.lower() in image_extensions and file_path.is_file():
            try:
                # 打开并优化图片
                with Image.open(file_path) as img:
                    # 调整大小，保持宽高比
                    if img.width > MAX_IMAGE_WIDTH:
                        ratio = MAX_IMAGE_WIDTH / float(img.width)
                        new_height = int(float(img.height) * ratio)
                        img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
                    
                    # 保存到目标目录
                    target_path = TARGET_CERT_DIR / file_path.name
                    # 转换为RGB模式以确保JPEG兼容性，PNG则保留透明度
                    if target_path.suffix.lower() in ('.jpg', '.jpeg'):
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                    img.save(target_path, optimize=True, quality=85)
                    
                    cert_files.append({
                        'filename': file_path.name,
                        'path': f"certificates/{file_path.name}"
                    })
                    print(f"  已处理: {file_path.name}")
            except Exception as e:
                print(f"  处理 {file_path.name} 时出错: {e}")
    
    print(f"共处理了 {len(cert_files)} 张证书图片。")
    return cert_files

def generate_html_page(certificates):
    """生成美观的HTML展示页面"""
    print("正在生成网页...")
    
    html_content = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的获奖证书集</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #4a6fa5;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 2.8rem;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            font-size: 1.2rem;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .stats {{
            display: inline-flex;
            gap: 20px;
            margin-top: 20px;
            background: #f8f9fa;
            padding: 12px 25px;
            border-radius: 50px;
            font-weight: 500;
        }}
        
        .stats span {{
            color: #4a6fa5;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }}
        
        .cert-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}
        
        .cert-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }}
        
        .cert-img-container {{
            flex-grow: 1;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8f9fa;
            padding: 20px;
            min-height: 250px;
        }}
        
        .cert-img {{
            max-width: 100%;
            max-height: 240px;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}
        
        .cert-info {{
            padding: 20px;
            border-top: 1px solid #eee;
        }}
        
        .cert-name {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 1.1rem;
            margin-bottom: 5px;
            word-break: break-word;
        }}
        
        .cert-actions {{
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }}
        
        .btn {{
            padding: 8px 18px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .btn-view {{
            background: #4a6fa5;
            color: white;
        }}
        
        .btn-view:hover {{
            background: #3a5a80;
        }}
        
        .btn-download {{
            background: #f0f0f0;
            color: #555;
            border: 1px solid #ddd;
        }}
        
        .btn-download:hover {{
            background: #e0e0e0;
        }}
        
        footer {{
            text-align: center;
            margin-top: 60px;
            padding: 25px;
            color: #7f8c8d;
            font-size: 0.95rem;
            border-top: 1px solid #eaeaea;
        }}
        
        .last-updated {{
            margin-top: 10px;
            font-size: 0.85rem;
            color: #95a5a6;
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
            }}
            h1 {{
                font-size: 2.2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-award"></i> 获奖证书集</h1>
            <p class="subtitle">此页面通过二维码附于我的个人简历中，集中展示了我所获得的荣誉与资质认证。所有证书均真实有效，可点击查看大图或下载。</p>
            <div class="stats">
                <div><i class="fas fa-certificate"></i> 证书总数: <span>{len(certificates)}</span></div>
                <div><i class="fas fa-sync-alt"></i> 最后更新: <span id="currentDate"></span></div>
            </div>
        </header>
        
        <main>
            <div class="gallery">
'''
    
    # 为每张证书生成卡片
    for cert in certificates:
        name_without_ext = os.path.splitext(cert['filename'])[0]
        # 简单清理文件名作为展示名
        display_name = name_without_ext.replace('_', ' ').replace('-', ' ')
        
        html_content += f'''
                <div class="cert-card">
                    <div class="cert-img-container">
                        <img src="{cert['path']}" alt="{display_name}" class="cert-img" loading="lazy">
                    </div>
                    <div class="cert-info">
                        <div class="cert-name">{display_name}</div>
                        <div class="cert-actions">
                            <a href="{cert['path']}" target="_blank" class="btn btn-view">
                                <i class="fas fa-expand-alt"></i> 查看大图
                            </a>
                            <a href="{cert['path']}" download class="btn btn-download">
                                <i class="fas fa-download"></i> 下载
                            </a>
                        </div>
                    </div>
                </div>
'''
    
    html_content += '''
            </div>
        </main>
        
        <footer>
            <p>© 2025 我的职业档案 | 本页面通过 GitHub Pages 部署，内容可动态更新</p>
            <p class="last-updated">扫描简历上的二维码即可随时访问此最新页面</p>
        </footer>
    </div>

    <script>
        // 动态更新日期
        const now = new Date();
        const options = {{ year: 'numeric', month: 'long', day: 'numeric' }};
        document.getElementById('currentDate').textContent = now.toLocaleDateString('zh-CN', options);
        
        // 为图片加载添加平滑效果
        document.addEventListener('DOMContentLoaded', function() {{
            const images = document.querySelectorAll('.cert-img');
            images.forEach(img => {{
                img.style.opacity = '0';
                img.style.transition = 'opacity 0.5s ease';
                img.onload = function() {{
                    this.style.opacity = '1';
                }};
                // 如果图片已缓存
                if (img.complete) img.onload();
            }});
        }});
    </script>
</body>
</html>
'''
    
    # 将HTML写入文件
    html_file_path = TARGET_PROJECT_DIR / "index.html"
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"网页已生成: {html_file_path}")
    return html_file_path

def main():
    print("="*50)
    print("开始生成证书展示页面...")
    print("="*50)
    
    # 1. 处理证书图片
    cert_list = process_and_copy_certificates()
    
    if not cert_list:
        print("未找到任何证书图片，请检查源文件夹路径。")
        return
    
    # 2. 生成HTML页面
    generate_html_page(cert_list)
    
    # 3. 给出后续操作提示
    print("\n" + "="*50)
    print("✅ 本地文件处理完成！")
    print("\n【后续操作指南】")
    print("1. 使用Git命令将变更推送到GitHub仓库：")
    print("   git add .")
    print("   git commit -m '更新证书集'")
    print("   git push origin main")
    print("\n2. 在GitHub仓库设置中开启GitHub Pages：")
    print("   Settings -> Pages -> Source: 选择 'main' branch -> Save")
    print("\n3. 等待几分钟后，访问生成的Pages网址（格式如：https://你的用户名.github.io/my-certificates/）")
    print("4. 将该网址复制到任何二维码生成工具（如草料二维码[citation:2]），生成二维码图片。")
    print("5. 将二维码图片插入到你的纸质简历中[citation:2]。")
    print("="*50)

if __name__ == "__main__":
    main()