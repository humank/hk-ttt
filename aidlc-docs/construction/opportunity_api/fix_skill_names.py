#!/usr/bin/env python3
"""
數據修復腳本：更新舊的生成的技能名稱為更友好的名稱
"""

import sqlite3
import re
from datetime import datetime

def fix_skill_names():
    """修復資料庫中的技能名稱"""
    
    # 連接到資料庫
    conn = sqlite3.connect('opportunity_management.db')
    cursor = conn.cursor()
    
    try:
        # 查找所有使用生成格式的技能名稱
        cursor.execute("""
            SELECT id, skill_name, skill_type, importance_level 
            FROM skill_requirements 
            WHERE skill_name LIKE 'Skill_%'
        """)
        
        old_skills = cursor.fetchall()
        
        if not old_skills:
            print("✅ 沒有找到需要修復的技能名稱")
            return
        
        print(f"🔍 找到 {len(old_skills)} 個需要修復的技能")
        
        # 定義技能名稱映射
        skill_mapping = {
            ('TECHNICAL', 'MUST_HAVE'): ['Python 程式設計', 'Java 開發', 'JavaScript 前端', 'AWS 雲端服務', 'Docker 容器化'],
            ('TECHNICAL', 'NICE_TO_HAVE'): ['React.js', 'Node.js', 'MongoDB', 'Redis', 'Kubernetes'],
            ('TECHNICAL', 'PREFERRED'): ['微服務架構', 'CI/CD 流程', 'API 設計', '資料庫設計', '系統架構'],
            ('SOFT', 'MUST_HAVE'): ['團隊合作', '溝通能力', '問題解決', '時間管理', '領導能力'],
            ('SOFT', 'NICE_TO_HAVE'): ['創新思維', '學習能力', '適應能力', '客戶服務', '專案管理'],
            ('SOFT', 'PREFERRED'): ['跨文化溝通', '衝突解決', '決策能力', '談判技巧', '教學能力'],
            ('DOMAIN', 'MUST_HAVE'): ['金融科技', '電子商務', '醫療保健', '教育科技', '物聯網'],
            ('DOMAIN', 'NICE_TO_HAVE'): ['區塊鏈', '人工智慧', '機器學習', '大數據', '網路安全'],
            ('DOMAIN', 'PREFERRED'): ['數位轉型', '敏捷開發', 'DevOps', '雲端原生', '邊緣運算']
        }
        
        # 更新每個技能
        updated_count = 0
        for skill_id, old_name, skill_type, importance_level in old_skills:
            # 根據技能類型和重要性選擇合適的名稱
            key = (skill_type, importance_level)
            if key in skill_mapping:
                # 使用索引來確保不同的技能有不同的名稱
                skill_options = skill_mapping[key]
                new_name = skill_options[updated_count % len(skill_options)]
            else:
                # 默認名稱
                type_names = {
                    'TECHNICAL': '技術技能',
                    'SOFT': '軟技能',
                    'DOMAIN': '領域知識'
                }
                new_name = type_names.get(skill_type, '專業技能')
            
            # 更新資料庫
            cursor.execute("""
                UPDATE skill_requirements 
                SET skill_name = ? 
                WHERE id = ?
            """, (new_name, skill_id))
            
            print(f"✅ 更新: {old_name} → {new_name} ({skill_type}, {importance_level})")
            updated_count += 1
        
        # 提交更改
        conn.commit()
        print(f"\n🎉 成功更新了 {updated_count} 個技能名稱")
        
        # 驗證更新結果
        cursor.execute("""
            SELECT skill_name, skill_type, importance_level, COUNT(*) as count
            FROM skill_requirements 
            GROUP BY skill_name, skill_type, importance_level
            ORDER BY skill_type, importance_level
        """)
        
        updated_skills = cursor.fetchall()
        print(f"\n📊 更新後的技能統計:")
        for skill_name, skill_type, importance, count in updated_skills:
            print(f"  • {skill_name} ({skill_type}, {importance}): {count} 次使用")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 開始修復技能名稱...")
    fix_skill_names()
    print("✅ 修復完成！")
