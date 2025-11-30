var message_timeout = document.getElementById("message-timer")

setTimeout(function(){
    message_timeout.classList.remove('show')
}, 2500)

document.querySelectorAll('.toast').forEach(toastEl => {
    new bootstrap.Toast(toastEl).show();
});