function load_encounter(instance) {
    $.ajax({
        type: "GET",
        url: '/ajax/encounter?id=' + instance,
        success: function (data) {
            clear_options('encounter');
            build_options(data, 'encounter');
            load_token(document.getElementById('select-encounter').value);
        }
    });
}

function load_token(encounter) {
    $.ajax({
        type: "GET",
        url: '/ajax/items?id=' + encounter,
        success: function (data) {
            clear_options('token');
            build_options(data, 'token');
        }
    });
}

function load_token_items(token) {
    $.ajax({
        type: "GET",
        url: '/ajax/token_items?id=' + token,
        success: function (data) {
            clear_items();

            let select = document.getElementById('select-items');
            let items = Object.assign({}, data.selected, data.unselected);

            for (let [key, value] of Object.entries(items)) {
                if (items.hasOwnProperty(key)) {
                    let option = document.createElement('option');
                    option.setAttribute('value', key);
                    option.innerHTML = value;
                    select.appendChild(option);
                }
            }

            check_multiple_values('select-items', Object.keys(data.selected));
        }
    });
}


function check_multiple_values(objectId, values) {
    let selectMultiObject = document.getElementById(objectId);
    for (var i = 0, l = selectMultiObject.options.length, o; i < l; i++) {
        o = selectMultiObject.options[i];
        if (values.indexOf(o.value) !== -1) {
            o.selected = true;
        } else {
            o.selected = false;
        }
    }
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
            if (specifier === 'token' && data[counter].fields.slot !== 'TOKEN') {
                continue;
            } else {
                let option = document.createElement('option');
                option.setAttribute('value', data[counter].pk);
                option.innerHTML = data[counter].fields.name;
                select.appendChild(option);
            }
        }
    }
}

function clear_options(specifier) {
    let select = document.getElementById('select-' + specifier);

    while (select.firstChild && select.childElementCount > 1) {
        select.removeChild(select.lastChild);
    }
}

function clear_items() {
    let select = document.getElementById('select-items');

    while (select.firstChild) {
        select.removeChild(select.lastChild);
    }
}