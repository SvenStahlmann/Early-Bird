$(document).ready(function () {
    set_active_encounter();
})

function set_active_encounter() {
    if (document.getElementById('encounter-id')) {
        let encounter_id = document.getElementById('encounter-id').innerHTML;
        encounter_id = encounter_id.split('\"').join('');
        console.log(encounter_id);

        if (document.getElementById('encounter-' + encounter_id)) {
            let active_encounter = document.getElementById('encounter-' + encounter_id);
            console.log(active_encounter);
            active_encounter.parentElement.parentElement.previousElementSibling.click();
            active_encounter.classList.add('active');
        }
    }
}