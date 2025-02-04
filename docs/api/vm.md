# Virtual Machine API Reference

## OptimizedGenomeVM

::: src.vm.optimized_vm.OptimizedGenomeVM
    handler: python
    selection:
      members:
        - execute
        - execute_bytecode
        - _execute_instruction
        - _parallel_load
        - _process_chunk

## Bytecode

::: src.compiler.bytecode.OpCode
    handler: python

::: src.compiler.bytecode.Instruction
    handler: python

::: src.compiler.bytecode.BytecodeGenerator
    handler: python
    selection:
      members:
        - generate
        - _generate_node

## Execution Context

::: src.vm.context.ExecutionContext
    handler: python
    selection:
      members:
        - get_variable
        - set_variable
        - create_scope
        - exit_scope 