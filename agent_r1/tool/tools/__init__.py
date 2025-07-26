"""
Specific tool implementations
"""

from agent_r1.tool.tools.comiler_autotuning.instrcount_tool import InstrCountTool
from agent_r1.tool.tools.comiler_autotuning.lightrag_knowledge_tool import LightRAGCompilerTool

__all__ = [
    'InstrCountTool',
    'LightRAGCompilerTool',
] 

def _default_tools(env):
    if env == 'optimizer':
        return [InstrCountTool(), LightRAGCompilerTool()]
    else:
        raise NotImplementedError
