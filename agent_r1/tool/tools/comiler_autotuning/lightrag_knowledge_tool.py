"""
Intelligent LLVM Pass Sequence Recommendation Tool (Rewritten Version)

Feature matching and pass sequence recommendation based on autophase_features.md knowledge base
"""

import os
import json
import re
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict, Counter

# Set environment variables to avoid flash attention issues
os.environ["TRANSFORMERS_DISABLE_FLASH_ATTENTION"] = "1"
os.environ["TRANSFORMERS_DISABLE_XFORMERS"] = "1"

from agent_r1.tool.tool_base import Tool

class LightRAGCompilerTool(Tool):
    """
    Intelligent LLVM Pass Sequence Recommendation Tool based on autophase_features.md knowledge base
    """
    
    def __init__(self, knowledge_base_path: str = None):
        """
        Initialize the tool
        
        Args:
            knowledge_base_path: Path to knowledge base
        """
        name = "lightrag_compiler_optimization"
        description = "Intelligent LLVM Pass sequence recommendation tool based on autophase_features.md knowledge base, returns enhanced prompts through feature matching"
        parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query string containing autophase features, used for program feature analysis and pass sequence recommendation"
                }
            },
            "required": ["query"]
        }
        
        super().__init__(name, description, parameters)
        
        # Set knowledge base path
        if knowledge_base_path is None:
            current_dir = Path(__file__).parent
            knowledge_base_path = current_dir / "knowledge_base"
        
        self.knowledge_base_path = Path(knowledge_base_path)
        
        # Load knowledge base
        self.knowledge_entries = self._load_autophase_knowledge()
        
        # Important feature weights (based on compiler optimization experience)
        self.feature_weights = {
            'TotalInsts': 1.0,
            'TotalBlocks': 0.8,
            'TotalMemInst': 0.9,
            'BranchCount': 0.7,
            'TotalFuncs': 0.6,
            'NumLoadInst': 0.8,
            'NumStoreInst': 0.8,
            'NumCallInst': 0.7,
            'NumAddInst': 0.6,
            'NumMulInst': 0.6,
            'NumICmpInst': 0.5,
            'NumAllocaInst': 0.7,
            'NumBitCastInst': 0.4,
            'NumBrInst': 0.6,
            'NumGetElementPtrInst': 0.5,
            'NumLShrInst': 0.4,
            'NumAShrInst': 0.4,
            'NumAndInst': 0.5,
            'NumOrInst': 0.5,
            'NumPHIInst': 0.6,
            'returnInt': 0.3,
            'CriticalCount': 0.5,
            'NumEdges': 0.4,
            'const32Bit': 0.3,
            'const64Bit': 0.3,
            'numConstZeroes': 0.2,
            'numConstOnes': 0.2,
            'UncondBranches': 0.4,
            'binaryConstArg': 0.3,
        }
    
    def _load_autophase_knowledge(self) -> List[Dict]:
        """Load autophase_features.md knowledge base"""
        knowledge_entries = []
        
        try:
            file_path = self.knowledge_base_path / "autophase_features.md"
            if not file_path.exists():
                print(f"Knowledge base file {file_path} does not exist")
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse each data entry
            entries = re.split(r'\n### [^\n]+\n', content)
            
            for entry in entries:
                if not entry.strip():
                    continue
                    
                entry_data = {}
                
                # Extract file path
                file_path_match = re.search(r'\*\*File Path:\*\* `([^`]+)`', entry)
                if file_path_match:
                    entry_data['file_path'] = file_path_match.group(1)
                
                # Extract performance improvement
                performance_match = re.search(r'\*\*Performance Improvement \(OverOz\):\*\* ([-\d.]+)', entry)
                if performance_match:
                    entry_data['performance_improvement'] = float(performance_match.group(1))
                
                # Extract optimal pass sequence
                pass_sequence_match = re.search(r'\*\*Optimal Pass Sequence:\*\*\n```json\n(\[.*?\])\n```', entry, re.DOTALL)
                if pass_sequence_match:
                    try:
                        entry_data['optimal_pass_sequence'] = json.loads(pass_sequence_match.group(1))
                    except:
                        continue
                
                # Extract autophase features
                features_section = re.search(r'\*\*Autophase Features:\*\*\n\n\| Feature \| Value \|\n\|[^\n]+\|\n((?:\| [^\n]+ \|\n)+)', entry)
                if features_section:
                    features = {}
                    feature_lines = features_section.group(1).strip().split('\n')
                    for line in feature_lines:
                        if '|' in line:
                            parts = [p.strip() for p in line.split('|') if p.strip()]
                            if len(parts) >= 2:
                                feature_name = parts[0]
                                try:
                                    feature_value = int(parts[1])
                                    features[feature_name] = feature_value
                                except:
                                    continue
                    entry_data['autophase_features'] = features
                
                # Only keep complete entries
                if all(key in entry_data for key in ['file_path', 'performance_improvement', 'optimal_pass_sequence', 'autophase_features']):
                    knowledge_entries.append(entry_data)
            
            print(f"Successfully loaded {len(knowledge_entries)} knowledge base entries")
            return knowledge_entries
            
        except Exception as e:
            print(f"Failed to load knowledge base: {e}")
            return []
    
    def _extract_autophase_features(self, query: str) -> Dict[str, int]:
        """Extract autophase features from query"""
        features = {}
        
        # Look for JSON format features
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', query, re.DOTALL)
        if json_match:
            try:
                features = json.loads(json_match.group(1))
                # Ensure all values are numbers
                features = {k: int(v) if isinstance(v, (int, float, str)) and str(v).isdigit() else v for k, v in features.items()}
                return features
            except:
                pass
        
        # Look for common feature patterns
        patterns = {
            r'Total instructions?:\s*(\d+)': 'TotalInsts',
            r'Total blocks?:\s*(\d+)': 'TotalBlocks', 
            r'Memory instructions?:\s*(\d+)': 'TotalMemInst',
            r'Branch count:\s*(\d+)': 'BranchCount',
            r'TotalInsts["\']?\s*[:=]\s*(\d+)': 'TotalInsts',
            r'TotalBlocks["\']?\s*[:=]\s*(\d+)': 'TotalBlocks',
            r'TotalMemInst["\']?\s*[:=]\s*(\d+)': 'TotalMemInst',
            r'BranchCount["\']?\s*[:=]\s*(\d+)': 'BranchCount',
            r'NumLoadInst["\']?\s*[:=]\s*(\d+)': 'NumLoadInst',
            r'NumStoreInst["\']?\s*[:=]\s*(\d+)': 'NumStoreInst',
            r'NumCallInst["\']?\s*[:=]\s*(\d+)': 'NumCallInst',
            r'NumAddInst["\']?\s*[:=]\s*(\d+)': 'NumAddInst',
            r'NumMulInst["\']?\s*[:=]\s*(\d+)': 'NumMulInst',
            r'NumICmpInst["\']?\s*[:=]\s*(\d+)': 'NumICmpInst',
        }
        
        for pattern, feature_name in patterns.items():
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                features[feature_name] = int(match.group(1))
        
        return features
    
    def _calculate_feature_similarity(self, features1: Dict[str, int], features2: Dict[str, int]) -> float:
        """Calculate similarity between two feature sets"""
        if not features1 or not features2:
            return 0.0
        
        # Get common features
        common_features = set(features1.keys()) & set(features2.keys())
        if not common_features:
            return 0.0
        
        # Calculate weighted Euclidean distance
        total_weight = 0
        weighted_distance = 0
        
        for feature in common_features:
            weight = self.feature_weights.get(feature, 0.1)
            total_weight += weight
            
            val1 = features1[feature]
            val2 = features2[feature]
            
            # Handle zero values
            if val1 == 0 and val2 == 0:
                continue
            elif val1 == 0 or val2 == 0:
                weighted_distance += weight
            else:
                # Calculate relative difference
                relative_diff = abs(val1 - val2) / max(val1, val2)
                weighted_distance += weight * relative_diff
        
        if total_weight == 0:
            return 0.0
        
        # Convert to similarity (0-1 range)
        similarity = 1 / (1 + weighted_distance / total_weight)
        return similarity
    
    def _calculate_composite_score(self, similarity: float, performance_improvement: float) -> float:
        """
        Calculate composite score balancing similarity and performance improvement
        
        Args:
            similarity: Feature similarity score (0-1)
            performance_improvement: Performance improvement value (can be negative)
            
        Returns:
            Composite score (higher is better)
        """
        # Normalize performance improvement to 0-1 range
        # Use sigmoid function to handle both positive and negative values
        normalized_performance = 1 / (1 + math.exp(-performance_improvement * 10))
        
        # Weighted combination: 60% similarity, 40% performance
        # This ensures we don't pick sequences that are too dissimilar even if they perform well
        similarity_weight = 0.6
        performance_weight = 0.4
        
        composite_score = similarity_weight * similarity + performance_weight * normalized_performance
        
        return composite_score
    
    def _find_best_entry(self, query_features: Dict[str, int]) -> Tuple[Dict, float, float]:
        """
        Find the best knowledge base entry based on composite score
        
        Args:
            query_features: Query program features
            
        Returns:
            Tuple of (best_entry, similarity, composite_score)
        """
        if not self.knowledge_entries:
            return None, 0.0, 0.0
        
        best_entry = None
        best_score = 0.0
        best_similarity = 0.0
        
        for entry in self.knowledge_entries:
            similarity = self._calculate_feature_similarity(
                query_features, entry['autophase_features']
            )
            
            # Only consider entries with minimum similarity threshold
            if similarity < 0.05:  # Very low threshold to avoid filtering out good performers
                continue
            
            performance = entry['performance_improvement']
            composite_score = self._calculate_composite_score(similarity, performance)
            
            if composite_score > best_score:
                best_score = composite_score
                best_entry = entry
                best_similarity = similarity
        
        return best_entry, best_similarity, best_score
    
    def _find_most_similar_entry(self, query_features: Dict[str, int]) -> Tuple[Dict, float]:
        """Find the most similar knowledge base entry"""
        if not self.knowledge_entries:
            return None, 0.0
        
        best_entry = None
        best_similarity = 0.0
        
        for entry in self.knowledge_entries:
            similarity = self._calculate_feature_similarity(
                query_features, entry['autophase_features']
            )
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_entry = entry
        
        return best_entry, best_similarity
    
    def _generate_enhanced_prompt(self, query: str, best_entry: Dict, similarity: float, composite_score: float) -> str:
        """Generate enhanced prompt"""
        if not best_entry:
            return "No similar knowledge base entries found. Please use general optimization strategies."
        
        similar_features = best_entry['autophase_features']
        optimal_sequence = best_entry['optimal_pass_sequence']
        performance = best_entry['performance_improvement']
        
        # Format feature table
        feature_table = "| Feature | Value |\n|---------|-------|\n"
        for feature, value in similar_features.items():
            feature_table += f"| {feature} | {value} |\n"
        
        enhanced_prompt = f"""Based on knowledge base retrieval, the best program case was found (similarity: {similarity:.3f}, composite score: {composite_score:.3f}):

**Selected Program's Autophase Features:**
{feature_table}

**Optimal Pass Sequence for this Program:**
```json
{json.dumps(optimal_sequence, indent=2)}
```

**Performance Improvement (OverOz):** {performance}

**Selection Rationale:**
This program was selected using a composite scoring algorithm that balances feature similarity ({similarity:.1%}) and performance improvement ({performance:.1%}). The composite score of {composite_score:.3f} represents the optimal trade-off between program similarity and optimization effectiveness.
Based on this optimally selected case, it is recommended to use this pass sequence for compiler optimization.
"""

        return enhanced_prompt
    
    def execute(self, args: Dict) -> str:
        """
        Execute RAG retrieval and return enhanced prompt
        
        Args:
            args: Dictionary containing query parameters
                - query: Query string containing autophase features
        
        Returns:
            Enhanced prompt string
        """
        try:
            query = args.get("query", "")
            
            if not query:
                return "Query content cannot be empty"
            
            # Extract autophase features
            query_features = self._extract_autophase_features(query)
            
            if not query_features:
                return "Could not extract valid autophase features from query, please check input format."
            
            # Find best knowledge base entry
            best_entry, similarity, composite_score = self._find_best_entry(query_features)
            
            if not best_entry or similarity < 0.1:
                return "No sufficiently similar knowledge base entries found. Consider using general compiler optimization strategies."
            
            # Generate enhanced prompt
            enhanced_prompt = self._generate_enhanced_prompt(query, best_entry, similarity, composite_score)
            
            return enhanced_prompt
            
        except Exception as e:
            return f"Error occurred during processing: {str(e)}"
    
    def get_most_similar_pass_sequence(self, query: str) -> List[str]:
        """
        Get most similar pass sequence (for SFT data generation)
        
        Args:
            query: Query string
            
        Returns:
            Optimal pass sequence list
        """
        try:
            query_features = self._extract_autophase_features(query)
            if not query_features:
                return []
            
            best_entry, similarity, composite_score = self._find_best_entry(query_features)
            if best_entry and similarity > 0.1:
                return best_entry['optimal_pass_sequence']
            
            return []
            
        except Exception as e:
            print(f"Error occurred while getting pass sequence: {e}")
            return []


if __name__ == "__main__":
    # Test the tool
    tool = LightRAGCompilerTool()
    
    # Test query
    test_query = """
    Looking at the autophase features, I can see:
    ```json
    {
        "TotalInsts": 180,
        "TotalBlocks": 33,
        "TotalMemInst": 106,
        "BranchCount": 28,
        "NumLoadInst": 45,
        "NumStoreInst": 32,
        "NumCallInst": 12
    }
    ```
    """
    
    print("Test query:", test_query)
    result = tool.execute({"query": test_query})
    print("\nEnhanced prompt:")
    print(result) 