import os
import json
import sys
from pathlib import Path


def get_installed_skills():
    """获取当前实际安装的技能"""
    scan_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scan_skills.py')
    
    if os.path.exists(scan_script):
        import subprocess
        result = subprocess.run(
            [sys.executable, scan_script],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return {s['name']: s for s in data.get('skills', [])}
            except json.JSONDecodeError:
                return {}
    return {}


def get_recorded_skills():
    """获取技能表中记录的技能"""
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skill_table.json')
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return {s['name']: s for s in data.get('skills', [])}
            except (json.JSONDecodeError, KeyError):
                return {}
    return {}


def sync_skills():
    """对比技能表与实际安装状态，输出差异报告"""
    installed = get_installed_skills()
    recorded = get_recorded_skills()
    
    installed_names = set(installed.keys())
    recorded_names = set(recorded.keys())
    
    # 新增的技能（已安装但未记录）
    new_skills = installed_names - recorded_names
    # 删除的技能（已记录但未安装）
    removed_skills = recorded_names - installed_names
    # 状态变化的技能
    changed_skills = []
    
    for name in installed_names & recorded_names:
        if installed[name].get('description') != recorded[name].get('description'):
            changed_skills.append(name)
    
    result = {
        'installed_count': len(installed),
        'recorded_count': len(recorded),
        'new_skills': [installed[name] for name in sorted(new_skills)],
        'removed_skills': [recorded[name] for name in sorted(removed_skills)],
        'changed_skills': [installed[name] for name in sorted(changed_skills)],
        'needs_sync': len(new_skills) > 0 or len(removed_skills) > 0 or len(changed_skills) > 0
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


def main():
    """主函数：执行同步检查"""
    sync_skills()


if __name__ == '__main__':
    main()
