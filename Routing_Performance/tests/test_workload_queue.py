# fixture workload_queue contains workload.txt
def test_operations(workload_queue):
    # NOTE: add in cleanup at duration on the fly IF connection succeeds
    first = workload_queue.pop()
    assert first.time == 0.221267
    assert workload_queue.peek_duration() == 1749.814739
    # check not yet touched
    assert first.connection.is_processed is False
    assert workload_queue.peek_final_connection(
    ).connection.is_processed is False


# TODO these should test actual behaviours (if possible?).. - check statistics?
def test_workload_simple(workload_simple):
    pass


def test_workload(workload_queue):
    pass
