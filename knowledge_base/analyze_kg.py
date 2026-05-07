#!/usr/bin/env python3
"""
查看知识图谱结构和内容
"""
import json
from build_kg import gen_kg_from_md
import os

def analyze_kg():
    """分析知识图谱结构"""
    print("🔍 Analyzing knowledge graph generated from markdown...")
    md_file = "<repo_root>/knowledge_base/docs/autophase_features.md"
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found")
        return
    print(f"📄 Source file: {md_file}")
    
    # 解析知识图谱数据
    kg_path = "<repo_root>/knowledge_base/compiler_kg/autophase_features_kg.json"
    if os.path.exists(kg_path):
        print(f"📚 Loading knowledge graph from {kg_path} ...")
        with open(kg_path, 'r') as f:
            kg_data = json.load(f)
    else:
        print("📚 Generating knowledge graph from markdown...")
        kg_data = gen_kg_from_md(md_file)           
        kg_dir = "<repo_root>/knowledge_base/compiler_kg"
        os.makedirs(kg_dir, exist_ok=True)
        with open(kg_path, 'w') as f:
            json.dump(kg_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 Knowledge Graph Statistics:")
    print(f"- Total Entities: {len(kg_data['entities'])}")
    print(f"- Total Relationships: {len(kg_data['relationships'])}")
    
    # 分析实体类型
    print(f"\n🏷️ Entity Types Distribution:")
    entity_types = {}
    for entity in kg_data['entities']:
        etype = entity['entity_type']
        entity_types[etype] = entity_types.get(etype, 0) + 1
    for etype, count in sorted(entity_types.items()):
        print(f"  - {etype}: {count}")
    
    # 展示一些特征组合实体（这是我们的核心实体）
    print(f"\n🎯 Feature Combination Examples (Core Entities):")
    feature_entities = [e for e in kg_data['entities'] if e['entity_type'] == 'autophase_feature_combination']
    for i, entity in enumerate(feature_entities[:5]):  # 显示前5个
        print(f"\n  {i+1}. {entity['entity_name']}")
        description = entity['description']
        if "Recommended passes:" in description:
            passes_part = description.split("Recommended passes:")[1].split("Performance improvement:")[0].strip()
            perf_part = description.split("Performance improvement:")[1].strip()
            print(f"     📝 Description: {description.split('.')[0]}...")
            print(f"     🔧 Recommended passes: {passes_part}")
            print(f"     📈 Performance: {perf_part}")
    
    # 展示优化 pass 实体
    print(f"\n🛠️ Compiler Optimization Pass Examples:")
    pass_entities = [e for e in kg_data['entities'] if e['entity_type'] == 'compiler_optimization_pass']
    for i, entity in enumerate(pass_entities[:8]):  # 显示前8个
        print(f"  {i+1}. {entity['entity_name']}: {entity['description']}")
    
    # 展示性能改进级别
    print(f"\n🚀 Performance Improvement Levels:")
    perf_entities = [e for e in kg_data['entities'] if e['entity_type'] == 'performance_improvement_level']
    for entity in perf_entities:
        print(f"  - {entity['entity_name']}: {entity['description']}")
    
    # 分析关系类型
    print(f"\n🔗 Relationship Examples:")
    relationships = kg_data['relationships']
    rel_types = {}
    for rel in relationships:
        rel_desc = rel['description']
        if "recommends optimization pass" in rel_desc:
            rel_types['feature_to_pass'] = rel_types.get('feature_to_pass', 0) + 1
        elif "achieves" in rel_desc and "performance improvement" in rel_desc:
            rel_types['feature_to_performance'] = rel_types.get('feature_to_performance', 0) + 1
        else:
            rel_types['other'] = rel_types.get('other', 0) + 1
    
    print(f"  Relationship types:")
    for rtype, count in rel_types.items():
        print(f"    - {rtype}: {count}")
    
    # 显示一些示例关系
    print(f"\n  Sample relationships:")
    feature_to_pass_rels = [r for r in relationships if "recommends optimization pass" in r['description']]
    for i, rel in enumerate(feature_to_pass_rels[:5]):
        print(f"    {i+1}. {rel['src_id']} -> {rel['tgt_id']}")
        print(f"       {rel['description']} (weight: {rel['weight']:.3f})")
    
    # 将分析结果保存到 JSON 文件
    # output_file = "kg_analysis_result.json"
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(kg_data, f, indent=2, ensure_ascii=False)
    # print(f"\n💾 Full knowledge graph data saved to: {output_file}")
    
    # 总结
    print(f"\n✅ Knowledge Graph Summary:")
    print(f"   🎯 Core concept: Autophase Features → Optimization Passes")
    print(f"   📊 Features: {len(feature_entities)} distinct feature combinations")
    print(f"   🛠️ Passes: {len(pass_entities)} optimization techniques")
    print(f"   🚀 Performance: {len(perf_entities)} improvement levels")
    print(f"   🔗 Mappings: {len(relationships)} feature-to-optimization relationships")
    
    print(f"\n🎉 This knowledge graph enables agents to:")
    print(f"   1. Input program's Autophase features")
    print(f"   2. Find matching feature combinations")
    print(f"   3. Get recommended optimization passes")
    print(f"   4. Understand expected performance improvements")


if __name__ == "__main__":
    analyze_kg()
