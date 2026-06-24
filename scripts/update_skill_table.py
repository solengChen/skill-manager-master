import os
import json
import sys
from pathlib import Path


def classify_skill(skill: dict) -> str:
    """根据技能名称和描述对技能进行分类"""
    name = skill.get('name', '').lower()
    description = skill.get('description', '').lower()
    
    ai_keywords = ['ai', 'image', 'face', 'generate', '生成', '图像', '人工智能', 'brainstorm', 'creativity']
    dev_keywords = ['code', 'develop', 'design', 'skill', 'create', 'build', 'review', 'architecture', 'frontend', 'backend', 'web', 'react', 'python', 'javascript', 'typescript', '开发', '设计', '代码', '创建', '审查', '架构']
    cloud_keywords = ['azure', 'cloud', 'aws', 'gcp', 'kubernetes', 'docker', 'compute', 'serverless', '云', '微软']
    data_keywords = ['database', 'postgres', 'sql', 'data', 'analytics', '数据']
    test_keywords = ['test', 'tdd', 'unit', 'integration', 'testing', '测试']
    
    if any(kw in name or kw in description for kw in ai_keywords):
        return 'AI 功能类'
    if any(kw in name or kw in description for kw in test_keywords):
        return '测试类'
    if any(kw in name or kw in description for kw in cloud_keywords):
        return '云服务类'
    if any(kw in name or kw in description for kw in data_keywords):
        return '数据类'
    if any(kw in name or kw in description for kw in dev_keywords):
        return '开发工具类'
    
    return '其他'


def generate_markdown(skills_data: dict) -> str:
    """根据技能数据生成 Markdown 格式的技能管理表"""
    md = []
    
    md.append("# 技能管理表")
    md.append("")
    md.append("## 已安装技能")
    md.append("")
    md.append("| 技能名称 | 功能描述 | 分类 | 安装状态 |")
    md.append("|---------|---------|------|---------|")
    
    for skill in skills_data.get('skills', []):
        category = classify_skill(skill)
        desc = skill.get('description', '')
        if len(desc) > 100:
            desc = desc[:100] + '...'
        md.append(f"| {skill.get('name', '')} | {desc} | {category} | ✅ 已安装 |")
    
    md.append("")
    md.append(f"**更新时间**: {skills_data.get('update_time', '')}")
    md.append(f"**技能总数**: {skills_data.get('total', 0)}")
    md.append("")
    
    # 按分类分组
    categories = {}
    for skill in skills_data.get('skills', []):
        cat = classify_skill(skill)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)
    
    for cat_name, cat_skills in sorted(categories.items()):
        md.append(f"## {cat_name}")
        md.append("")
        for skill in cat_skills:
            md.append(f"- **{skill.get('name', '')}**: {skill.get('description', '')[:150]}...")
        md.append("")
    
    return "\n".join(md)


def update_skill_table():
    """更新技能管理表（JSON + Markdown）"""
    script_dir = Path(__file__).parent
    
    scan_script = script_dir / 'scan_skills.py'
    if scan_script.exists():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(scan_script)],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            try:
                skills_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                skills_data = {'total': 0, 'skills': []}
        else:
            skills_data = {'total': 0, 'skills': []}
    else:
        skills_data = {'total': 0, 'skills': []}
    
    # 添加更新时间
    from datetime import datetime
    skills_data['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 保存 JSON 格式
    json_path = script_dir / 'skill_table.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(skills_data, f, ensure_ascii=False, indent=2)
    
    # 保存 Markdown 格式
    md_path = script_dir / '技能管理表.md'
    md_content = generate_markdown(skills_data)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"技能管理表已更新:")
    print(f"- JSON: {json_path}")
    print(f"- Markdown: {md_path}")
    print(f"- 技能总数: {skills_data.get('total', 0)}")


def main():
    """主函数：更新技能管理表"""
    update_skill_table()


if __name__ == '__main__':
    main()
