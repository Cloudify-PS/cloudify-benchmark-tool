from cloudify.decorators import workflow
from cloudify.workflows import ctx

@workflow
def run_operation(**kwargs):
    graph = ctx.graph_mode()

    for node in ctx.nodes:
        for instance in node.instances:
            graph.add_task(instance.execute_operation('cloudify.interfaces.lifecycle.start'))

    return graph.execute()

run_operation()
