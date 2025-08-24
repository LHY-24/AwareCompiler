# 基于 Markdown 文件构建知识图谱指南

## 概述

本项目提供了从 Markdown 文件（特别是编译器优化相关的文档）构建知识图谱的功能。

## 主要功能

### 1. 支持的数据类型

从 `autophase_features.md` 文件中提取以下信息：
- **程序文件**: LLVM IR 程序文件路径和基本信息
- **性能指标**: OverOz 性能改进指标
- **优化序列**: 最优编译器优化 pass 序列
- **Autophase 特征**: 程序的静态分析特征

### 2. 知识图谱实体类型

- `llvm_program`: LLVM IR 程序
- `performance_metric`: 性能改进指标
- `compiler_pass`: 编译器优化 pass
- `autophase_small/medium/large`: 按规模分类的 Autophase 特征
- `autophase_numeric`: 数值型 Autophase 特征

### 3. 关系类型

- `program achieves performance improvement`: 程序与性能指标的关系
- `uses compiler pass at position X`: 程序使用优化 pass 的关系
- `has autophase feature`: 程序具有的静态特征

## 使用方法

### 方法 1: 命令行使用

```bash
# 从 Markdown 文件构建知识图谱
python build_kg.py agent_r1/tool/tools/comiler_autotuning/knowledge_base/autophase_features.md

# 指定自定义工作目录
python build_kg.py autophase_features.md ./my_compiler_kg
```

### 方法 2: 程序化使用

```python
from build_kg import build_kg_from_md, gen_kg_from_md

# 1. 只解析数据（不构建 RAG）
kg_data = gen_kg_from_md("autophase_features.md")
print(f"Found {len(kg_data['entities'])} entities")
print(f"Found {len(kg_data['relationships'])} relationships")

# 2. 构建完整的知识图谱
rag = build_kg_from_md("autophase_features.md", "./compiler_kg")

# 3. 查询知识图谱
result = rag.query("What compiler passes work best for programs with high instruction count?")
print(result)
```

## 测试和验证

运行测试脚本：
```bash
python test_md_kg.py
```

测试脚本会：
1. 解析 Markdown 文件
2. 显示提取的实体和关系统计
3. 验证数据解析的正确性

## 知识图谱查询示例

构建完成后，可以进行各种查询：

```python
# 查询性能优化相关
result = rag.query("Which compiler passes provide the best performance improvements?")

# 查询特定特征的程序
result = rag.query("Find programs with high branch count and their optimization strategies")

# 查询优化序列模式
result = rag.query("What are common optimization pass sequences?")
```

## 文件结构

```
/root/AwareCompiler/knowledge_base
├── build_kg.py                    # 主要的知识图谱构建脚本
├── tests/                         
│   └── test_autophase_parse.md      # 测试脚本
├── docs/
│   └── autophase_features.md      # 输入的 Markdown 文件
└── compiler_kg/                   # 生成的知识图谱工作目录
    ├── graph_chunk_entity_relation.graphml
    ├── entities.json
    ├── relationships.json
    └── ...
```

## 扩展和自定义

### 添加新的实体类型

在 `gen_kg_from_md` 函数中添加新的实体提取逻辑：

```python
# 示例：添加函数调用图实体
call_graph_entity = {
    "entity_name": f"CALL_GRAPH_{file_name}",
    "entity_type": "call_graph",
    "description": f"Function call graph for {file_name}",
    "source_id": md_file_path
}
entities.append(call_graph_entity)
```

### 自定义特征权重

修改特征权重计算逻辑：

```python
# 自定义权重计算
weight = calculate_custom_weight(feat_name, feat_value)
```

### 支持其他 Markdown 格式

修改正则表达式模式以支持不同的 Markdown 格式：

```python
# 自定义条目分割模式
entries = re.split(r'your_custom_pattern', content)
```

## 依赖项

- `lightrag`: 知识图谱构建和查询
- `openai`: LLM 和嵌入功能（需要 API 密钥）

## 注意事项

1. **API 密钥**: 确保设置了 OpenAI API 密钥环境变量
2. **内存使用**: 大型文档可能需要较多内存
3. **文件格式**: 当前版本针对特定的 Markdown 格式优化，其他格式可能需要调整解析逻辑
4. **错误处理**: 建议在生产环境中添加更完善的错误处理机制

## 常见问题

1. **ImportError**: 确保安装了所有依赖项
2. **API 错误**: 检查 OpenAI API 密钥和网络连接
3. **解析错误**: 检查 Markdown 文件格式是否符合预期
4. **内存不足**: 尝试处理更小的文件或增加系统内存
