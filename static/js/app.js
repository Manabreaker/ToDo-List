$(document).ready(function() {
    // Function to load tasks
    function loadTasks() {
        $.ajax({
            url: '/tasks',
            method: 'GET',
            success: function(data) {
                let taskList = '';
                data.forEach(function(task) {
                    let checked = task.is_completed ? 'checked' : '';
                    let strikeClass = task.is_completed ? 'class="completed-task"' : '';

                    taskList = `
                        <tr id="task-${task.id}" ${strikeClass}>
                            <td>${task.id}</td>
                            <td>${task.title}</td>
                            <td>${task.description}</td>
                            <td>
                                <input type="checkbox" class="toggle-status" data-id="${task.id}" ${checked}>
                                <button class="btn btn-danger btn-sm delete-task" data-id="${task.id}">Delete</button>
                            </td>
                        </tr>
                    ` + taskList; // Добавляем сверху
                });
                $('#taskList').html(taskList);
            },
            error: function() {
                alert('Failed to load tasks');
            }
        });
    }

    // Load tasks when page loads
    loadTasks();

    // Handle task creation
    $('#taskForm').on('submit', function(e) {
        e.preventDefault();

        let title = $('#title').val();
        let description = $('#description').val();

        $.ajax({
            url: '/tasks',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                title: title,
                description: description
            }),
            success: function() {
                $('#title').val('');
                $('#description').val('');
                loadTasks(); // Reload tasks
            },
            error: function() {
                alert('Failed to create task');
            }
        });
    });

    // Handle task deletion
    $(document).on('click', '.delete-task', function() {
        let taskId = $(this).data('id');

        $.ajax({
            url: `/tasks/${taskId}`,
            method: 'DELETE',
            success: function() {
                loadTasks(); // Reload tasks after deletion
            },
            error: function() {
                alert('Failed to delete task');
            }
        });
    });

    // Handle task status toggle
    $(document).on('change', '.toggle-status', function() {
        let taskId = $(this).data('id');
        let isCompleted = $(this).is(':checked');

        $.ajax({
            url: `/tasks/${taskId}`,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({
                is_completed: isCompleted
            }),
            success: function() {
                let row = $(`#task-${taskId}`);
                if (isCompleted) {
                    row.addClass('completed-task');
                } else {
                    row.removeClass('completed-task');
                }
            },
            error: function() {
                alert('Failed to update task status');
            }
        });
    });
});
