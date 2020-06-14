$(document).ready(function () {
    set_first_tab_active();
})

function set_first_tab_active() {
    if (document.getElementById('slot-tabs').firstElementChild) {
        document.getElementById('slot-tabs').firstElementChild.firstElementChild.click();
    }
}