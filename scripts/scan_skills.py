import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional


def parse_frontmatter(content: str) -> Dict[str, str]:
    """解析 SKILL.md 的 frontmatter 部分，支持 YAML block scalars 和多行值"""
    frontmatter = {}
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        yaml_content = match.group(1).strip()
        try:
            import yaml
            parsed = yaml.safe_load(yaml_content)
            if isinstance(parsed, dict):
                frontmatter = {k: str(v) for k, v in parsed.items()}
        except ImportError:
            lines = yaml_content.split('\n')
            key = None
            value_lines = []
            for line in lines:
                if ':' in line and not line.strip().startswith(('-', '>')):
                    if key is not None and value_lines:
                        frontmatter[key] = '\n'.join(value_lines).strip().strip('"').strip("'")
                    parts = line.split(':', 1)
                    key = parts[0].strip()
                    value_lines = [parts[1].strip()] if len(parts) > 1 else []
                elif key is not None:
                    value_lines.append(line.strip())
            if key is not None:
                frontmatter[key] = '\n'.join(value_lines).strip().strip('"').strip("'")
    return frontmatter


def scan_directory(skills_path: Path) -> List[Dict[str, str]]:
    """扫描单个技能目录"""
    skills = []
    if not skills_path.exists():
        return skills
    
    for skill_dir in skills_path.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_md_path = skill_dir / 'SKILL.md'
        if not skill_md_path.exists():
            continue
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter = parse_frontmatter(content)
            skill_info = {
                'name': frontmatter.get('name', skill_dir.name),
                'description': frontmatter.get('description', '未描述'),
                'path': str(skill_dir),
                'status': 'installed',
                'source': str(skills_path)
            }
            skills.append(skill_info)
        except Exception as e:
            print(f"读取技能 {skill_dir.name} 时出错: {e}")
    
    return skills


def scan_skills() -> List[Dict[str, str]]:
    """扫描所有技能目录，获取所有已安装技能的信息"""
    installed_skills = []
    
    # 扫描全局技能目录: ~/.agents/skills/
    home = str(Path.home())
    global_skills_dir = Path(home) / '.agents' / 'skills'
    installed_skills.extend(scan_directory(global_skills_dir))
    
    # 扫描当前工作目录下的本地技能目录: .trae/skills/
    cwd = os.getcwd()
    local_skills_dir = Path(cwd) / '.trae' / 'skills'
    installed_skills.extend(scan_directory(local_skills_dir))
    
    return installed_skills


def main():
    """主函数：扫描技能并输出结果"""
    skills = scan_skills()
    
    result = {
        'total': len(skills),
        'skills': skills
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
