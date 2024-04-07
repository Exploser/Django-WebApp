const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}y" role="alert">
        ${msg}
    </div> `
}