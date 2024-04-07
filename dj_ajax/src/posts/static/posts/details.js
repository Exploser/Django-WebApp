const backBtn = document.getElementById("back-btn")
const deleteBtn = document.getElementById("delete-btn")
const updateBtn = document.getElementById("update-btn")
const url = window.location.href + "data/"
const spinnerBox = document.getElementById('spinner-box')
const postBox = document.getElementById('post-box')

const titleInput = document.getElementById('id_title')
const bodyInput = document.getElementById('id_body')

backBtn.addEventListener('click', ()=> {
    history.back()
})

$.ajax({
    type: 'GET',
    url: url,
    success: function (response){
        console.log(response)
        const data = response.data

        if (data.logged_in !== data.author){
            
        } else {
            updateBtn.classList.remove('not-visible')
            deleteBtn.classList.remove('not-visible')
        }

        const titleEl = document.createElement('h3')
        titleEl.setAttribute('class', 'mt-3')

        const bodyEl = document.createElement('h3')
        bodyEl.setAttribute('class', 'mt-1')

        titleEl.textContent = data.title
        bodyEl.textContent = data.body

        postBox.appendChild(titleEl)
        postBox.appendChild(bodyEl)

        titleInput.value = data.title
        bodyInput.value = data.body

        spinnerBox.classList.add('not-visible')
    },
    error: function (error){
        console.log(url)
        console.log(error)
    },
})