#!/usr/bin/env python3
"""
Agent 查询知识图谱示例
演示如何根据程序的 Autophase 特征查找最优的编译器优化序列
"""
import json
from knowledge_base.build_kg import gen_kg_from_md


class CompilerOptimizationAgent:
    """编译器优化智能代理"""
    
    def __init__(self, kg_data):
        self.entities = {e['entity_name']: e for e in kg_data['entities']}
        self.relationships = kg_data['relationships']
        
        # 构建特征组合到优化序列的映射
        self.feature_to_passes = {}
        self.feature_to_performance = {}
        
        for rel in self.relationships:
            if "recommends optimization pass" in rel['description']:
                feature = rel['src_id']
                pass_name = rel['tgt_id']
                position = int(rel['description'].split('position ')[1])
                weight = rel['weight']
                
                if feature not in self.feature_to_passes:
                    self.feature_to_passes[feature] = []
                
                self.feature_to_passes[feature].append({
                    'pass': pass_name,
                    'position': position,
                    'weight': weight
                })
            
            elif "achieves" in rel['description'] and "performance improvement" in rel['description']:
                feature = rel['src_id']
                perf_level = rel['tgt_id']
                improvement = rel['weight']
                
                self.feature_to_performance[feature] = {
                    'level': perf_level,
                    'improvement': improvement
                }
        
        # 排序优化序列
        for feature in self.feature_to_passes:
            self.feature_to_passes[feature].sort(key=lambda x: x['position'])
    

    def categorize_features(self, features):
        """将数值特征分类为范围"""
        key_features = ["TotalInsts", "TotalBlocks", "TotalFuncs", "NumCallInst"]
        
        categorized = []
        
        for feat_name in key_features:
            if feat_name in features:
                feat_value = features[feat_name]
                
                if feat_name in ["TotalInsts", "TotalBlocks"]:
                    if feat_value < 50:
                        range_cat = "Low"
                    elif feat_value < 150:
                        range_cat = "Medium"
                    else:
                        range_cat = "High"
                    categorized.append(f"{feat_name}_{range_cat}")
                elif feat_name in ["NumCallInst"]:
                    if feat_value < 10:
                        range_cat = "Few"
                    elif feat_value < 25:
                        range_cat = "Moderate"
                    else:
                        range_cat = "Many"
                    categorized.append(f"{feat_name}_{range_cat}")
                else:
                    categorized.append(f"{feat_name}_{feat_value}")
        
        return "_".join(categorized[:4])  # 只取前4个特征
    

    def find_optimization_sequence(self, program_features):
        """根据程序特征查找最优的编译器优化序列"""
        print(f"🔍 Analyzing program features...")
        print(f"Input features: {program_features}")
        
        # 生成特征组合标识符
        feature_signature = self.categorize_features(program_features)
        print(f"Generated feature signature: {feature_signature}")
        
        # 查找匹配的特征组合
        if feature_signature in self.feature_to_passes:
            passes_info = self.feature_to_passes[feature_signature]
            
            print(f"\n✅ Found matching optimization strategy!")
            
            # 获取优化序列
            optimization_sequence = [p['pass'] for p in passes_info]
            
            print(f"🛠️ Recommended optimization sequence:")
            for i, pass_info in enumerate(passes_info):
                pass_name = pass_info['pass']
                weight = pass_info['weight']
                print(f"  {i+1}. {pass_name} (priority: {weight:.3f})")
            
            # 获取性能预期
            if feature_signature in self.feature_to_performance:
                perf_info = self.feature_to_performance[feature_signature]
                improvement = perf_info['improvement']
                level = perf_info['level']
                print(f"\n📈 Expected performance improvement:")
                print(f"  - Level: {level}")
                print(f"  - Improvement: {improvement:.1%}")
            else:
                print(f"\n📈 Performance improvement: Data not available")
            
            return optimization_sequence
        else:
            print(f"\n❌ No exact match found for this feature combination.")
            
            # 尝试找到相似的特征组合
            similar_features = self._find_similar_features(feature_signature)
            if similar_features:
                print(f"🔍 Found similar feature combinations:")
                for sim_feature in similar_features[:3]:  # 显示前3个相似的
                    passes = [p['pass'] for p in self.feature_to_passes[sim_feature]]
                    print(f"  - {sim_feature}: {len(passes)} optimization passes")
                
                # 使用最相似的特征组合
                best_match = similar_features[0]
                print(f"\n🎯 Using most similar strategy: {best_match}")
                
                passes_info = self.feature_to_passes[best_match]
                optimization_sequence = [p['pass'] for p in passes_info]
                
                print(f"🛠️ Recommended optimization sequence:")
                for i, pass_info in enumerate(passes_info[:10]):  # 只显示前10个
                    pass_name = pass_info['pass']
                    weight = pass_info['weight']
                    print(f"  {i+1}. {pass_name} (priority: {weight:.3f})")
                
                return optimization_sequence
            else:
                print(f"🔧 Using general optimization strategy: -Oz")
                return ["-Oz"]
    

    def _find_similar_features(self, target_signature):
        """查找相似的特征组合"""
        target_parts = target_signature.split('_')
        
        similarities = []
        for feature in self.feature_to_passes.keys():
            feature_parts = feature.split('_')
            
            # 计算相似度（匹配的部分数量）
            matches = 0
            for i, part in enumerate(target_parts):
                if i < len(feature_parts) and part == feature_parts[i]:
                    matches += 1
            
            similarity = matches / len(target_parts)
            if similarity > 0.5:  # 至少50%相似
                similarities.append((feature, similarity))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [f[0] for f in similarities]


def demo_agent_usage():
    """演示Agent的使用"""
    print("🤖 Compiler Optimization Agent Demo")
    print("=" * 50)
    
    # 加载知识图谱（如已存在则直接加载，否则生成并保存）
    import os
    import glob
    kg_path = "/root/AwareCompiler/knowledge_base/compiler_kg/autophase_features_kg.json"
    if os.path.exists(kg_path):
        print(f"📚 Loading knowledge graph from {kg_path} ...")
        with open(kg_path, 'r') as f:
            kg_data = json.load(f)
    else:
        print("📚 Generating knowledge graph from markdown...")
        kg_data = gen_kg_from_md("/root/AwareCompiler/knowledge_base/docs/autophase_features.md") # TODO：使用lightrag生成KG
        kg_dir = "/root/AwareCompiler/knowledge_base/compiler_kg"
        os.makedirs(kg_dir, exist_ok=True)
        with open(kg_path, 'w') as f:
            json.dump(kg_data, f, ensure_ascii=False, indent=2)
    agent = CompilerOptimizationAgent(kg_data)
    print(f"✅ Knowledge graph loaded: {len(kg_data['entities'])} entities, {len(kg_data['relationships'])} relationships")
    

    # 示例1：中等复杂度程序
    print(f"\n" + "="*50)
    print(f"📝 Example 1: Medium complexity program")
    print(f"="*50)
    
    program1_features = {
        "TotalInsts": 85,
        "TotalBlocks": 12,
        "TotalFuncs": 10,
        "NumCallInst": 15,
        "NumLoadInst": 20,
        "NumStoreInst": 8,
        "BranchCount": 10,
        "NumICmpInst": 3
    }
    
    sequence1 = agent.find_optimization_sequence(program1_features)
    
    # 示例2：高复杂度程序
    print(f"\n" + "="*50)
    print(f"📝 Example 2: High complexity program")
    print(f"="*50)
    
    program2_features = {
        "TotalInsts": 180,
        "TotalBlocks": 25,
        "TotalFuncs": 12,
        "NumCallInst": 28,
        "NumLoadInst": 35,
        "NumStoreInst": 20,
        "BranchCount": 22,
        "NumICmpInst": 8
    }
    
    sequence2 = agent.find_optimization_sequence(program2_features)
    
    # 示例3：简单程序
    print(f"\n" + "="*50)
    print(f"📝 Example 3: Simple program")
    print(f"="*50)
    
    program3_features = {
        "TotalInsts": 35,
        "TotalBlocks": 5,
        "TotalFuncs": 3,
        "NumCallInst": 5,
        "NumLoadInst": 8,
        "NumStoreInst": 4,
        "BranchCount": 3,
        "NumICmpInst": 1
    }
    
    sequence3 = agent.find_optimization_sequence(program3_features)
    
    print(f"\n" + "="*50)
    print(f"🎉 Demo completed!")
    print(f"💡 The agent successfully mapped program features to optimization strategies.")
    print(f"🚀 This enables automatic compiler optimization based on program characteristics.")


if __name__ == "__main__":
    demo_agent_usage()
