function load_characters(raid_day) {
    $.ajax({
        type: "GET",
        url: '/ajax/characters?id=' + raid_day,
        success: function (data) {
            clear_options('characters');
            build_options(data, 'characters');
            load_parameters(raid_day, document.getElementById('select-characters').value);
        }
    });
}

function load_parameters(raid_day, character) {
    if (raid_day && character) {
        $.ajax({
            type: "GET",
            url: '/ajax/attendance/parameters?raid-day=' + raid_day + '&character=' + character,
            success: function (data) {
                console.log(data);
                set_parameters(data);
            }
        });
    }
}

function set_parameters(data) {
    let parameters = data[0].fields;

    document.getElementById('present').checked = parameters.present;
    document.getElementById('calendar-entry').checked = parameters.calendar_entry;
    document.getElementById('world-buffs').checked = parameters.world_buffs;
    document.getElementById('consumables').checked = parameters.consumables;
    document.getElementById('misconduct').checked = parameters.misconduct;
    document.getElementById('comment').innerHTML = parameters.comment;
}

function build_options(data, specifier) {
    let select = document.getElementById('select-' + specifier);

    if (data.length === 0 || data === {} || $.isEmptyObject(data)) {
        let option = document.createElement('option');
        option.setAttribute('disabled', 'true');
        option.innerHTML = 'Nichts gefunden!';
        select.appendChild(option);
    } else {
        for (let counter = 0; counter < data.length; counter++) {
            let option = document.createElement('option');
            option.setAttribute('value', data[counter].pk);
            option.innerHTML = data[counter].fields.name;
            select.appendChild(option);
        }
    }
}

function clear_options(specifier) {
    let select = document.getElementById('select-' + specifier);

    while (select.firstChild && select.childElementCount > 1) {
        select.removeChild(select.lastChild);
    }
}