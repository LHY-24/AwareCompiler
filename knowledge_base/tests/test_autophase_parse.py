#!/usr/bin/env python3
"""
直接测试数据解析，不依赖任何外部服务
"""
import os
import sys
import re
import json

def parse_md_simple(md_file_path):
    """parse markdown file"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割文档为单独的条目
    entries = re.split(r'### train/poj104-v1/.*?\.ll', content)[1:]
    
    entities = []
    relationships = []
    
    for entry in entries:
        if not entry.strip():
            continue
            
        # 提取文件路径
        file_path_match = re.search(r'\*\*File Path:\*\* `([^`]+)`', entry)
        if not file_path_match:
            continue
        file_path = file_path_match.group(1)
        file_name = os.path.basename(file_path).replace('.ll', '')
        
        # 提取性能改进指标
        overoz_match = re.search(r'\*\*Performance Improvement \(OverOz\):\*\* ([0-9.]+)', entry)
        overoz = float(overoz_match.group(1)) if overoz_match else 0.0
        
        # 提取最优优化序列
        pass_seq_match = re.search(r'\*\*Optimal Pass Sequence:\*\*\s*```json\s*(\[.*?\])\s*```', entry, re.DOTALL)
        optimal_passes = []
        if pass_seq_match:
            try:
                optimal_passes = json.loads(pass_seq_match.group(1))
            except:
                optimal_passes = []
        
        # 创建程序实体
        entities.append({
            "entity_name": file_name,
            "entity_type": "llvm_program",
            "description": f"LLVM IR program with performance improvement {overoz}",
            "overoz": overoz,
            "optimal_passes": optimal_passes
        })
    
    return entities


def main():
    md_file = "/root/AwareCompiler/knowledge_base/docs/autophase_features.md"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found")
        return
    
    print("🔍 Parsing markdown file...")
    print(f"File: {md_file}")
    
    try:
        entities = parse_md_simple(md_file)
        
        print(f"\n✅ Success! Found {len(entities)} programs")
        
        # 统计分析
        with_improvement = [e for e in entities if e['overoz'] > 0]
        total_passes = sum(len(e['optimal_passes']) for e in entities)
        
        print(f"\n📊 Statistics:")
        print(f"  - Total programs: {len(entities)}")
        print(f"  - With performance improvement: {len(with_improvement)}")
        print(f"  - Total optimization passes: {total_passes}")
        
        # 显示一些示例
        print(f"\n📝 Sample programs:")
        for i, entity in enumerate(entities[:5]):
            print(f"  {i+1}. {entity['entity_name']}")
            print(f"     OverOz: {entity['overoz']}")
            print(f"     Passes: {entity['optimal_passes']}")
        
        # 保存结果
        # output_file = "./simple_parse_result.json"
        # with open(output_file, 'w', encoding='utf-8') as f:
        #     json.dump(entities, f, indent=2, ensure_ascii=False)
        # print(f"\n💾 Results saved to: {output_file}")
        
        print(f"\n🎉 Parsing completed successfully!")
        print("✅ The markdown parsing functionality is working correctly.")
        
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
