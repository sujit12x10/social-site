$(document).ready(function(){
    console.log('hello world')
    $('#update-btn').click(function(){
        $('.ui.modal')
        .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
})


// getting csrftoken
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrf_token = getCookie("csrftoken");


// like unlike
const likeForms = [...document.getElementsByClassName('like-form')]
const likeBtns = [...document.getElementsByClassName("like-btn")]

likeBtns.forEach((btn) => {
    btn.addEventListener('click', (event) => {
        event.preventDefault()
        const postId = btn.getAttribute('data-id')
        const previousAction = btn.getAttribute('data-action')
        const newAction = previousAction === "like" ? "unlike" : "like"
        const icon = previousAction === "like" ? "down" : "up"
        const likeIcon = document.getElementById(`icon${postId}`)
        const newIcon = document.createElement('i')
        newIcon.id = `icon${postId}`
        newIcon.classList.add('thumbs', `${icon}`, 'icon')
        likeIcon.parentNode.replaceChild(newIcon, likeIcon)

        btn.dataset.action = newAction
        const func = async() => {
            resp = await fetch('http://127.0.0.1:8000/posts/liked/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify({
                    'post_id': parseInt(postId)
                })
            })
            const likeBox = document.getElementById(`likes${postId}`)
            data = await resp.json()
            
            const newSpan = document.createElement('span')
            newSpan.id = `likes${postId}`
            likeOrLikes = parseInt(data.likes) === 1 ? 'like' : 'likes'
            newSpan.innerText =  `${data.likes} ${likeOrLikes}` 
            likeBox.parentNode.replaceChild(newSpan, likeBox)
        }
        func()
    })
})


// comment toggle
document.addEventListener('DOMContentLoaded', () => {
    const btns = [...document.getElementsByClassName('cmt_btn')]
    btns.forEach((btn) => {
        btn.addEventListener('click', (event) => {
            const id = event.target.dataset.id
            const commentBox = document.getElementById(`comment-box${id}`)
            commentBox.style.display = commentBox.style.display !== 'block' ? 'block' : 'none'
        })
    })
})


// comment adding
const commentBtns = [...document.getElementsByClassName('cmnt-btn')]
commentBtns.forEach((btn) => {
    btn.addEventListener('click', (ele) => {
        console.log('working');
        const postId = btn.getAttribute('data-id')
        const form = document.getElementById(`form${postId}`)
        const body = form.body.value
        const commentBox = document.getElementById(`comment-box${postId}`)
        const commentNumberBox = document.getElementById(`comments${postId}`)
        ele.preventDefault()
        const cmntFunc = async () => {
            const resp = await fetch('http://127.0.0.1:8000/posts/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify({
                    'body': body,
                    'post_id': parseInt(postId),
                    'submit_c_form': ''
                })
            })
            const result = await resp.json()
            console.log(result['date']);
            commentBox.innerHTML = `
            <div class="ui segment mb-5">
                <img class="ui avatar image" src=${result['pic_url']} alt="">
                <span>${result['name']}</span> | ${result['date']}
                <div class="mt-5">${body}</div>
            </div>` + commentBox.innerHTML
            const commentOrComments = parseInt(result['comments']) === 1 ? ' comment': ' comments'
            commentNumberBox.innerHTML = parseInt(result['comments']) + commentOrComments
            form.reset()
        }
        if (body != ""){
            cmntFunc()
        }
    })
})



// modal
$(document).ready(function(){
    console.log('hello world')
    $('#update-btn').click(function(){
        $('.ui.modal')
        .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
})



// navbar
/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
navToggle = document.getElementById('nav-toggle'),
navClose = document.getElementById('nav-close')

/* Menu show */
navToggle.addEventListener('click', () =>{
   navMenu.classList.add('show-menu')
})

/* Menu hidden */
navClose.addEventListener('click', () =>{
   navMenu.classList.remove('show-menu')
})

/*=============== SEARCH ===============*/
const search = document.getElementById('search'),
searchBtn = document.getElementById('search-btn'),
searchLink = document.getElementById('search-text'),
searchClose = document.getElementById('search-close')

/* Search show */
searchBtn.addEventListener('click', () =>{
   search.classList.add('show-search')
})

searchLink.addEventListener('click', () =>{
   search.classList.add('show-search')
})

/* Search hidden */
searchClose.addEventListener('click', () =>{
   search.classList.remove('show-search')
})

/*=============== LOGIN ===============*/
const login = document.getElementById('login'),
loginBtn = document.getElementById('login-btn'),
loginClose = document.getElementById('login-close')

/* Login show */
loginBtn.addEventListener('click', () =>{
   login.classList.add('show-login')
})

/* Login hidden */
loginClose.addEventListener('click', () =>{
   login.classList.remove('show-login')
})