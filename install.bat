@echo off
chcp 65001 > nul
echo ========================================
echo   技能管理大师 - 快速安装脚本
echo ========================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.6+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查 PyYAML 是否安装
python -c "import yaml" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 PyYAML 依赖...
    pip install pyyaml
    if errorlevel 1 (
        echo [错误] PyYAML 安装失败，请手动运行: pip install pyyaml
        pause
        exit /b 1
    )
    echo [成功] PyYAML 安装完成
)

echo.
echo [步骤 1/4] 创建全局技能目录...
mkdir "%USERPROFILE%\.agents\skills\技能管理大师" 2>nul
echo [成功] 目录创建完成

echo.
echo [步骤 2/4] 复制技能文件...
copy SKILL.md "%USERPROFILE%\.agents\skills\技能管理大师\" >nul
if errorlevel 1 (
    echo [错误] SKILL.md 复制失败
    pause
    exit /b 1
)
echo [成功] SKILL.md 复制完成

echo.
echo [步骤 3/4] 复制脚本文件...
copy scripts\*.py "%USERPROFILE%\.agents\skills\技能管理大师\" >nul
if errorlevel 1 (
    echo [错误] 脚本文件复制失败
    pause
    exit /b 1
)
echo [成功] 脚本文件复制完成

echo.
echo [步骤 4/4] 初始化技能表...
python "%USERPROFILE%\.agents\skills\技能管理大师\update_skill_table.py"
echo [成功] 技能表初始化完成

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 技能管理大师已安装到:
echo %USERPROFILE%\.agents\skills\技能管理大师
echo.
echo 常用命令:
echo   扫描技能: python %%USERPROFILE%%\.agents\skills\技能管理大师\scan_skills.py
echo   更新表:   python %%USERPROFILE%%\.agents\skills\技能管理大师\update_skill_table.py
echo   同步检查: python %%USERPROFILE%%\.agents\skills\技能管理大师\sync_skills.py
echo.
pause
