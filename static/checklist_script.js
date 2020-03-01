$('.task_remove_button').hide();

function show_remove_button(task_name) {
    $("#" + task_name).show();
};

function hide_remove_button(task_name) {
    $("#" + task_name).hide();
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