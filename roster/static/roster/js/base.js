$(document).ready(function () {
    // Set active sidebar link
    set_active_specialization();

    // Initialize search autocomplete
    autocomplete_roster();
})

function set_active_specialization() {
    if (document.getElementById('specialization-id')) {
        let specialization_id = document.getElementById('specialization-id').innerHTML;
        specialization_id = specialization_id.split('\"').join('');

        if (document.getElementById('specialization-' + specialization_id)) {
            let active_encounter = document.getElementById('specialization-' + specialization_id);
            active_encounter.parentElement.parentElement.previousElementSibling.click();
            active_encounter.parentElement.parentElement.previousElementSibling.classList.add('active');
            active_encounter.classList.add('active');
        }
    }
}

function autocomplete_roster() {
    new autoComplete({
        selector: 'input[id="search-input"]',
        minChars: 2,
        source: function (term, response) {
            $.getJSON('/roster/ajax/autocomplete', {search: term}, function (data) {
                if (data.length === 0) {
                    response([['Nichts passendes gefunden!', [], []]]);
                } else {
                    response(data);
                }
            });
        },
        renderItem: function (data) {
            let html = '';

            if (data[4] === 'specialization') {
                html += '<div class="autocomplete-suggestion" data-val="' + data[0] + '"><input type="hidden" value="' + data[4] + '-' + data[2] + '">';
                html += '<img class="sidebar-img" src="/media/' + data[3] + '"> ';
                html += data[1] + ' - '  + data[0] + '</div>'
            } else if (data[3] === 'character') {
                html += '<div class="autocomplete-suggestion" data-val="' + data[0] + '"><input type="hidden" value="' + data[3] + '-' + data[1] + '">';
                html += '<img class="sidebar-img" src="/media/' + data[2] + '"> ';
                html += data[0] + '</div>'
            }

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
    window.location.href = '/roster/search?search=' + search_param;
}

function search_event(e) {
    if (e.keyCode === 13) {
        search();
    }
}
