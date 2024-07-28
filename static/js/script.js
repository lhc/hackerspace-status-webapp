document.addEventListener('DOMContentLoaded', function() {
    var switchInput = document.getElementById('switch');
    var clickSound = document.getElementById('click-sound');

    switchInput.addEventListener('change', function() {
        clickSound.play();
        if (switchInput.checked) {
            window.location.href = '/lhc_aberto';
        } else {
            window.location.href = '/lhc_fechado';
        }
    });
});
