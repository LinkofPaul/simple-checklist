var createForm = document.createElement("form");
createForm.setAttribute('class', 'form-signin')
createForm.setAttribute('action', "/setup");
createForm.setAttribute('method', "post");
createForm.setAttribute('id', "createForm");
createForm.innerHTML = `
    <div class="form-label-group">
        <input name="name" class="form-control create-list-name" id="createNameId" type="text" placeholder="Name of Checklist" maxlength="75" required>
    </div>
    <div class="form-label-group">
        <input name="password" class="form-control create-list-password" id="createPasswordId" type="password" placeholder="Password" maxlength="256" required> 
    </div>
    <div id="nameTakenDiv" style="display: none; color:red">Name already taken</div>
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

$(document).on('submit', '#createForm', function(event){
    event.preventDefault();
    $.ajax({
        data : {
            name : $('#createNameId').val(),
            password : $('#createPasswordId').val()
        },
        type : 'POST',
        url : '/setup'
    })
    .done(function(data){
        if (data.error){
            document.getElementById("nameTakenDiv").style.display = "block"
            document.getElementById('createNameId').value = "";
            document.getElementById('createPasswordId').value = "";
        } else {
            document.getElementById("nameTakenDiv").style.display = "none"
            window.location.assign(data.redirectURL)
        }
    })
})

$(document).on('keyup', '#search_text_id', function(event){
    event.preventDefault();
    $.ajax({
        data : {
            search_text : $('#search_text_id').val()
        },
        type : 'POST',
        url : '/search'
    })
    .done(function(data){
        document.getElementById('searchReplyField').innerHTML = "";
        unorderedList = document.createElement("div");
        search_field_size = (data.names_length > 10) ? 10 : data.names_length
        for(i = 0; i < search_field_size; i++){
            listIteam = document.createElement("div");
            unorderedList.appendChild(listIteam)

            listForm = document.createElement("form");
            listForm.setAttribute('action', "/login");
            listForm.setAttribute('method', "post");
            listForm.setAttribute('id', "loginForm");
            listIteam.appendChild(listForm)

            name_input = document.createElement("input");
            name_input.setAttribute('type', 'hidden')
            name_input.setAttribute('name', 'checklist_name')
            idAtt = "checklistIdfor" + data.names_concat[i]
            name_input.setAttribute('id', idAtt)
            name_input.setAttribute('value', data.names[i])
            listForm.appendChild(name_input)

            name_div = document.createElement("div");
            hide_func = 'hidePasswordField("' + data.names_concat[i] + '")'
            name_div.setAttribute('onclick', hide_func);
            name_div.setAttribute('style', "cursor:pointer");
            name_div.innerHTML = data.names[i]
            listForm.appendChild(name_div)

            pass_div = document.createElement("div");
            pass_div.setAttribute('id', data.names_concat[i]);
            pass_div.setAttribute('style', "display:none");
            passAtt = "passIdfor" + data.names_concat[i]
            pass_div.innerHTML = `<input type="password" id="`
                                    + passAtt + `" name="password" placeholder="Password" maxlength="256">
                                  <input type="submit" value="open">`
            listForm.appendChild(pass_div)

            wrongpass_div = document.createElement("div");
            errorLoginDiv = "errorLoginDivfor" + data.names_concat[i]
            wrongpass_div.setAttribute('id', errorLoginDiv)
            wrongpass_div.setAttribute('style', "display: none; color:red")
            wrongpass_div.innerHTML = "Wrong password"
            pass_div.append(wrongpass_div)
        }
        document.getElementById('searchReplyField').appendChild(unorderedList)
    })
})

$(document).on('submit', '#loginForm', function(event){
    event.preventDefault();
    
    formElem = event.target
    objectId = formElem.children[2].getAttribute('id')

    checklistLoginId = "#checklistIdfor" + objectId
    passLoginId = "#passIdfor" + objectId
    errorLoginId = "errorLoginDivfor" + objectId
    $.ajax({
        data : {
            checklist_name : $(checklistLoginId).val(),
            password : $(passLoginId).val()
        },
        type : 'POST',
        url : '/login'
    })
    .done(function(data){
        if (data.error){
            document.getElementById(errorLoginId).style.display = "block"
            document.getElementById('passIdfor' + objectId).value = "";
        } else {
            document.getElementById(errorLoginId).style.display = "none"
            window.location.assign(data.redirectURL)
        }
    })
})

$(document).on('keydown', '#searchForm', function(event){
    if(event.keyCode == 13){
        event.preventDefault();
    }
})

function hidePasswordField(element_id){
	if (document.getElementById(element_id).style.display == "block"){
        document.getElementById("errorLoginDivfor" + element_id).style.display = "none"
        document.getElementById(element_id).style.display = "none"
	} else{
		document.getElementById(element_id).style.display = "block"
	}
}

