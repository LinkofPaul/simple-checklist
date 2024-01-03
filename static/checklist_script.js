$('.task_remove_button').hide();

function toggle_remove_button(task_name) {
    $("#" + task_name).toggle();
};

$(document).on('submit', '#createTaskForm', function(event){
    event.preventDefault();
    $.ajax({
        data : {
            name : $('#checklistforTaskId').val(),
            newTask : $('#newTaskId').val()
        },
        type : 'POST',
        url : '/checklist/add_task'
    })
    .done(function(data){
        if (data.error){
            document.getElementById("taskTakenDiv").style.display = "block"
            document.getElementById("newTaskId").value = "";
        } else {
            document.getElementById("taskTakenDiv").style.display = "none"
            window.location.assign(data.redirectURL)
        }
    })
    
})