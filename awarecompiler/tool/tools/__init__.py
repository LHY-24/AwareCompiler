"""
Specific tool implementations
"""

from awarecompiler.tool.tools.compiler_autotuning.instrcount_tool import InstrCountTool
from awarecompiler.tool.tools.compiler_autotuning.knowledge_tool import KnowledgeTool

__all__ = [
    'InstrCountTool',
    'KnowledgeTool',
] 

def _default_tools(env):
    if env == 'optimizer':
        return [InstrCountTool(), KnowledgeTool()]
    else:
        raise NotImplementedError
