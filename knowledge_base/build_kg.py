import os
import sys
import re
import json
from lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed


def gen_kg_from_md(md_file_path: str) -> dict:
    """
    从 markdown 文件中解析编译器优化相关信息，构建以 Autophase Features 为核心的知识图谱
    """
    entities = []
    relationships = []
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割文档为单独的条目
    entries = re.split(r'### train/.*?\.ll', content)[1:]

    # 用于存储特征组合到优化序列的映射
    feature_combinations = {}
    
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
        
        # 提取 Autophase 特征
        features = {}
        feature_table_match = re.search(r'\*\*Autophase Features:\*\*.*?\| Feature \| Value \|.*?\|-+\|-+\|(.*?)(?=\n---|\n\*\*|\Z)', entry, re.DOTALL)
        if feature_table_match:
            feature_lines = feature_table_match.group(1).strip().split('\n')
            for line in feature_lines:
                if '|' in line and line.strip():
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2:
                        feature_name = parts[0]
                        feature_value = parts[1]
                        try:
                            features[feature_name] = int(feature_value)
                        except:
                            features[feature_name] = feature_value
        
        # 创建关键特征的实体和优化建议
        key_features = ["TotalInsts", "TotalBlocks", "TotalFuncs", "NumCallInst", 
                       "NumLoadInst", "NumStoreInst", "BranchCount", "NumICmpInst"]
        
        # 生成特征组合标识符
        feature_signature = []
        for feat_name in key_features:
            if feat_name in features:
                feat_value = features[feat_name]
                # 将数值特征分类为范围
                if feat_name in ["TotalInsts", "TotalBlocks"]:
                    if feat_value < 50:
                        range_cat = "Low"
                    elif feat_value < 150:
                        range_cat = "Medium"
                    else:
                        range_cat = "High"
                    feature_signature.append(f"{feat_name}_{range_cat}")
                elif feat_name in ["NumCallInst", "NumLoadInst", "NumStoreInst"]:
                    if feat_value < 10:
                        range_cat = "Few"
                    elif feat_value < 25:
                        range_cat = "Moderate"
                    else:
                        range_cat = "Many"
                    feature_signature.append(f"{feat_name}_{range_cat}")
                else:
                    # 其他特征直接使用数值
                    feature_signature.append(f"{feat_name}_{feat_value}")
        
        # 创建特征组合实体
        if feature_signature:
            feature_combo_name = "_".join(feature_signature[:4])  # 只取前4个特征避免名称过长
            
            # 构建详细的特征描述
            feature_desc_parts = []
            optimization_context = []
            
            for feat_name in key_features:
                if feat_name in features:
                    feat_value = features[feat_name]
                    feature_desc_parts.append(f"{feat_name}: {feat_value}")
                    
                    # 添加优化上下文
                    if feat_name == "TotalInsts" and feat_value > 100:
                        optimization_context.append("complex program requiring aggressive optimization")
                    elif feat_name == "NumCallInst" and feat_value > 15:
                        optimization_context.append("call-heavy program benefiting from inlining")
                    elif feat_name == "NumLoadInst" and feat_value > 20:
                        optimization_context.append("memory-intensive program needing memory optimization")
            
            feature_description = "; ".join(feature_desc_parts)
            context_description = "; ".join(optimization_context) if optimization_context else "standard optimization applicable"
            
            # 格式化优化序列
            pass_sequence_str = " -> ".join(optimal_passes) if optimal_passes else "No specific optimization needed"
            
            # 创建或更新特征组合实体
            if feature_combo_name not in feature_combinations:
                feature_entity = {
                    "entity_name": feature_combo_name,
                    "entity_type": "autophase_feature_combination",
                    "description": f"Autophase feature pattern: {feature_description}. Optimization context: {context_description}. Recommended passes: {pass_sequence_str}. Performance improvement: {overoz}",
                    "source_id": md_file_path
                }
                entities.append(feature_entity)
                feature_combinations[feature_combo_name] = {
                    "passes": optimal_passes,
                    "performance": overoz,
                    "count": 1,
                    "examples": [file_name]
                }
            else:
                # 更新已存在的特征组合
                feature_combinations[feature_combo_name]["count"] += 1
                feature_combinations[feature_combo_name]["examples"].append(file_name)
                if overoz > feature_combinations[feature_combo_name]["performance"]:
                    feature_combinations[feature_combo_name]["passes"] = optimal_passes
                    feature_combinations[feature_combo_name]["performance"] = overoz
            
            # 为每个优化pass创建实体
            for i, pass_name in enumerate(optimal_passes):
                pass_entity_name = pass_name.replace('--', '').replace('-', '_')
                
                # 避免重复创建相同的pass实体
                if not any(e["entity_name"] == pass_entity_name for e in entities):
                    pass_entity = {
                        "entity_name": pass_entity_name,
                        "entity_type": "compiler_optimization_pass",
                        "description": f"Compiler optimization pass: {pass_name}",
                        "source_id": md_file_path
                    }
                    entities.append(pass_entity)
                
                # 创建特征组合到优化pass的关系
                relationships.append({
                    "src_id": feature_combo_name,
                    "tgt_id": pass_entity_name,
                    "description": f"recommends optimization pass at position {i+1}",
                    "keywords": f"optimization,recommendation,sequence_{i+1},performance_{overoz}",
                    "weight": (1.0 / (i + 1)) * (1.0 + overoz),  # 考虑位置和性能改进
                    "source_id": md_file_path
                })
            
            # 如果有显著的性能改进，创建性能改进实体
            if overoz > 0.01:  # 只有超过1%的改进才创建
                perf_level = "High" if overoz > 0.05 else "Medium" if overoz > 0.02 else "Low"
                perf_entity_name = f"Performance_Improvement_{perf_level}"
                
                # 避免重复创建相同的性能实体
                if not any(e["entity_name"] == perf_entity_name for e in entities):
                    perf_entity = {
                        "entity_name": perf_entity_name,
                        "entity_type": "performance_improvement_level",
                        "description": f"{perf_level} performance improvement level (improvement > {overoz:.3f})",
                        "source_id": md_file_path
                    }
                    entities.append(perf_entity)
                
                # 创建特征组合到性能改进的关系
                relationships.append({
                    "src_id": feature_combo_name,
                    "tgt_id": perf_entity_name,
                    "description": f"achieves {perf_level.lower()} performance improvement",
                    "keywords": f"performance,improvement,{perf_level.lower()}",
                    "weight": overoz,
                    "source_id": md_file_path
                })
    
    return {
        "chunks": [],
        "entities": entities,
        "relationships": relationships
    }


def build_kg_from_md(md_file_path: str, working_dir: str = "./compiler_kg"):
    """
    从 markdown 文件构建编译器优化知识图谱
    """
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    rag = LightRAG(
        working_dir=working_dir,
        llm_model_func=gpt_4o_mini_complete,
        embedding_func=openai_embed,
    )

    kg_data = gen_kg_from_md(md_file_path)
    rag.insert_custom_kg(kg_data)
    
    print(f"Knowledge graph built successfully!")
    print(f"- Total entities: {len(kg_data['entities'])}")
    print(f"- Total relationships: {len(kg_data['relationships'])}")
    print(f"- Working directory: {working_dir}")
    
    return rag


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_kg.py <md_file_path> [working_dir]")
        print("Example: python build_kg.py ./docs/autophase_temp.md ./compiler_kg")
        sys.exit(1)
    
    md_file = sys.argv[1]
    working_dir = sys.argv[2] if len(sys.argv) > 2 else "./compiler_kg"
    
    if not os.path.exists(md_file):
        print(f"Error: Markdown file {md_file} not found")
        sys.exit(1)
    
    build_kg_from_md(md_file, working_dir)
