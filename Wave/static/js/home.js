//will show tabs if selected
function showTab(e){
    var target_id = this.firstElementChild.id
    var target_class = this.firstElementChild.className
    if (target_class == "showing"){
        return;
    }
    var sibling = this.nextElementSibling
    if (sibling == undefined){
        sibling = this.previousElementSibling
    }
    let show_this=target_id
    let hide_this = sibling.firstElementChild.id

    this.firstElementChild.setAttribute("class", "showing");
    sibling.firstElementChild.classList.remove("showing");
    hideElements(hide_this)
    showElements(show_this)
}

function hideElements(class_name){
    var hidden = document.getElementsByClassName(class_name);
    for (var i of hidden) {
        i.style.display ="none";
    }

}
function showElements(class_name){
    var shown = document.getElementsByClassName(class_name);
    for (var i of shown) {
        i.style.display ="block";
    }

}

//set up tabs 
//TODO - set up animation (still working on)
function setTabs() {
    var tabs = document.getElementById("tabs").children;
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener("click", showTab);
    }
    hideElements('github_post');
    hideElements('upload_image');

    //Creating a textarea with auto-resize
    //https://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize
    //DreamTeK -https://stackoverflow.com/users/2120261/dreamtek
    // Annswer - https://stackoverflow.com/posts/25621277/revisions
    $('textarea').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
      }).on('input', function () {
        this.style.height = 50+ 'px';
        this.style.height = (this.scrollHeight) + 'px';
      });
    
}




//message for empty
function setEmptyMessage() {
    var githubs = document.getElementsByClassName('github_post');
    if (githubs.length == 0){
        var git = document.getElementById('empty_git');
        git.style.display = "block";
    }
}

