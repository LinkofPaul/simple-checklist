$('.task_remove_button').hide();

function show_remove_button(task_name) {
    $("#" + task_name).show();
};

function hide_remove_button(task_name) {
    $("#" + task_name).hide();
};