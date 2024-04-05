console.log("HELLO WORLD")

const helloWorldBox = document.getElementById('hello-world')
const postsBox = document.getElementById('posts-box')

helloWorldBox.innerHTML = 'hello world'

$.ajax({
    type: 'GET',
    url: '/hello-world/',
    success: function(response){
        console.log(response.text)
        helloWorldBox.textContent = response.text
    },
    error: function(error){
        console.log('error', error)
    }
})

$.ajax({
    type: 'GET',
    url: '/data/',
    success: function(response){
        console.log(response)
        const data = response.data
        console.log(data)
        data.forEach(element => {
            postsBox.innerHTML += `
                ${element.title} - <b>${element.body}</b><br>
            `
        });
    },
    error: function(error){
        console.error(error);
    }
})