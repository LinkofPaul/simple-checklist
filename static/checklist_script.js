var createForm = document.createElement("form");
createForm.setAttribute('action', "/setup");
createForm.setAttribute('method', "post");
createForm.innerHTML = `
    <label>Name of checklist: </label><input name="name" type="text" required> <br>
    <label>Password: </label><input name="password" type="password" required> <br> 
    <input type="submit" value="Create">
    `
document.getElementById("createButton").addEventListener("click", function(){
    var fromDivEl = document.getElementById("formDiv")
    if (fromDivEl.style.display === "none") {
        fromDivEl.insertAdjacentElement('afterbegin', createForm);
        fromDivEl.style.display = "block";
    } else {
        fromDivEl.style.display = "none";
        fromDivEl.removeChild(createForm)
    }
});

$(document).on('keyup', '#search_text_id', function(event){
    $.ajax({
        data : {
            search_text : $(search_text_id).val()
        },
        type : 'POST',
        url : '/search'
    })
    .done(function(data){
        document.getElementById('searchReplyField').innerHTML = "";

        unorderedList = document.createElement("ul");
        search_field_size = (data.names_length > 10) ? 10 : data.names_length
        for(i = 0; i < search_field_size; i++){
            listIteam = document.createElement("li");
            unorderedList.appendChild(listIteam)

            listForm = document.createElement("form");
            listForm.setAttribute('action', "/login");
            listForm.setAttribute('method', "post");
            listIteam.appendChild(listForm)

            name_input = document.createElement("input");
            name_input.setAttribute('type', 'hidden')
            name_input.setAttribute('name', 'checklist_name')
            name_input.setAttribute('value', data.names[i])
            listForm.appendChild(name_input)

            name_div = document.createElement("div");
            hide_func = 'hidePasswordField("' + data.names[i] + '")'
            name_div.setAttribute('onclick', hide_func);
            name_div.setAttribute('style', "cursor:pointer");
            name_div.innerHTML = data.names[i]
            listForm.appendChild(name_div)

            pass_div = document.createElement("div");
            pass_div.setAttribute('id', data.names[i]);
            pass_div.setAttribute('style', "display:none");
            pass_div.innerHTML = `<label>Password: </label><input type="password" name="password" required>
                                  <input type="submit" value="open">`
            listForm.appendChild(pass_div)
        }
        document.getElementById('searchReplyField').appendChild(unorderedList)
    })
    event.preventDefault();
})

$(document).on('keydown', '#searchForm', function(event){
    if(event.keyCode == 13){
        event.preventDefault();
    }
})

function hidePasswordField(element_id){
	if (document.getElementById(element_id).style.display == "block"){
		document.getElementById(element_id).style.display = "none"
	} else{
		document.getElementById(element_id).style.display = "block"
	}
}

