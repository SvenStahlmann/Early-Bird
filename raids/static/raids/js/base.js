$(document).ready(function () {
    // Set active sidebar link
    set_active_encounter();

    // Initialize search autocomplete
    autocomplete_raids();
})

function set_active_encounter() {
    if (document.getElementById('encounter-id')) {
        let encounter_id = document.getElementById('encounter-id').innerHTML;
        encounter_id = encounter_id.split('\"').join('');

        if (document.getElementById('encounter-' + encounter_id)) {
            let active_encounter = document.getElementById('encounter-' + encounter_id);
            active_encounter.parentElement.parentElement.parentElement.setAttribute('aria-expanded', 'true');
            active_encounter.parentElement.parentElement.setAttribute('aria-hidden', 'false');
            active_encounter.parentElement.parentElement.removeAttribute('style');
            active_encounter.parentElement.parentElement.classList.add('is-active');
            active_encounter.parentElement.parentElement.previousElementSibling.classList.add('active');
            active_encounter.classList.add('active');
        }
    }
}

function autocomplete_raids() {
    new autoComplete({
        selector: 'input[id="search-input"]',
        minChars: 2,
        source: function (term, response) {
            $.getJSON('/raids/ajax/autocomplete', {search: term}, function (data) {
                if (data.length === 0) {
                    response([['Nichts passendes gefunden!', [], []]]);
                } else {
                    response(data);
                }
            });
        },
        renderItem: function (data) {
            let html = '<div class="autocomplete-suggestion" data-val="' + data[0] + '"><input type="hidden" value="' + data[2] + '-' + data[1] + '">';

            if (data[2] === 'encounter') {
                html += '<i class="fas fa-skull"></i> ';
            } else if (data[2] === 'item') {
                html += '<i class="fas fa-shield-alt"></i> ';
            }

            html += data[0] + '</div>'

            return html
        },
        onSelect: function (data) {
            // Set value on hidden search input field to 'specifier-id'
            if (data.type === 'keydown') {
                document.getElementById('search-hidden').value = document.getElementsByClassName('autocomplete-suggestion selected')[0].firstElementChild.value;
            }

            if (data.type === 'mousedown') {
                document.getElementById('search-hidden').value = data.target.firstElementChild.value;
            }
        }
    });
}

function search() {
    let search_param = document.getElementById('search-hidden').value;
    window.location.href = '/raids/search?search=' + search_param;
}

function search_event(e) {
    if (e.keyCode === 13) {
        search();
    }
}