$(document).ready(function () {
    // Set active sidebar link
    set_active_encounter();

    autocomplete();
})

function set_active_encounter() {
    if (document.getElementById('encounter-id')) {
        let encounter_id = document.getElementById('encounter-id').innerHTML;
        encounter_id = encounter_id.split('\"').join('');

        if (document.getElementById('encounter-' + encounter_id)) {
            let active_encounter = document.getElementById('encounter-' + encounter_id);
            active_encounter.parentElement.parentElement.previousElementSibling.click();
            active_encounter.parentElement.parentElement.previousElementSibling.classList.add('active');
            active_encounter.classList.add('active');
        }
    }
}

function autocomplete() {
    new autoComplete({
    selector: 'input[id="search-input"]',
    source: function(term, response){
        $.getJSON('/raids/ajax/autocomplete', { search: term }, function(data){ console.log(data); response(data); });
    }
});
}

function submit_search_form() {

}