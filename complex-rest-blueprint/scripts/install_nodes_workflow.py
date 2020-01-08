from cloudify.decorators import workflow
from cloudify.workflows import ctx

@workflow
def run_operation(**kwargs):
    graph = ctx.graph_mode()


    send_event_starting_tasks = {}
    send_event_done_tasks = {}

    for node in ctx.nodes:
        for instance in node.instances:
            send_event_starting_tasks[instance.id] = instance.send_event('Starting to run operation')
            send_event_done_tasks[instance.id] = instance.send_event('Done running operation')

    for node in ctx.nodes:
        for instance in node.instances:

            sequence = graph.sequence()

            sequence.add(
                send_event_starting_tasks[instance.id],
                instance.execute_operation('cloudify.interfaces.lifecycle.configure'),
                instance.execute_operation('cloudify.interfaces.lifecycle.start'),
                send_event_done_tasks[instance.id])

    for node in ctx.nodes:
        for instance in node.instances:
            for rel in instance.relationships:

                instance_starting_task = send_event_starting_tasks.get(instance.id)
                target_done_task = send_event_done_tasks.get(rel.target_id)

                if instance_starting_task and target_done_task:
                    graph.add_dependency(instance_starting_task, target_done_task)

    return graph.execute()

run_operation()
