let counter = 1;

// Fires if value of select-instance changes
function load_encounter(instance) {
    $.ajax({
        type: "GET",
        url: '/ajax/encounter?id=' + instance,
        success: function (data) {
            // Clear all options of select-encounter
            clear_options('encounter');

            // Populate select-encounter with options of ajax request data
            build_options(data, 'encounter');

            // Populate items of specified encounter (onchange doesn't fire if value gets set via javascript)
            load_items(document.getElementById('select-encounter').value);
        }
    });
}

// Fires if value of select-encounter changes
function load_items(encounter) {
    $.ajax({
        type: "GET",
        url: '/ajax/items?id=' + encounter,
        success: function (data) {
            // Clear all options of select-item
            clear_options('item');

            // Populate select-item with options of ajax request data
            build_options(data, 'item');

            // Create selects and populate entitlements of specified item (onchange doesn't fire if value gets via javascript)
            load_entitlements(document.getElementById('select-item').value);
        }
    });
}

// Build options of select fields
function build_options(data, specifier) {
    // Get specific select field
    let select = document.getElementById('select-' + specifier);

    // If ajax request found nothing
    if (data.length === 0 || data === {} || $.isEmptyObject(data)) {
        // Create disabled option
        let option = document.createElement('option');
        option.setAttribute('disabled', 'true');
        option.innerHTML = 'Nichts gefunden!';
        select.appendChild(option);
    } else {
        // Create options
        for (let count = 0; count < data.length; count++) {
            let option = document.createElement('option');
            option.setAttribute('value', data[count].pk);
            option.innerHTML = data[count].fields.name;
            select.appendChild(option);
        }
    }
}

// Clear all options of specified select field
function clear_options(specifier) {
    // Get specified select field
    let select = document.getElementById('select-' + specifier);

    // Delete select field
    while (select.firstChild && select.childElementCount > 1) {
        select.removeChild(select.lastChild);
    }
}

// Build new select field for specializations
function add_select_specialization() {
    counter++;

    // Elemente für die neue Priorität erstellen
    let grid = document.createElement('div');
    grid.classList.add('grid-x', 'grid-padding-x');

    let specialization_cell = document.createElement('div');
    specialization_cell.classList.add('cell', 'small-12', 'medium-9');

    let specialization_label = document.createElement('label');
    specialization_label.setAttribute('for', 'select-specialization-' + counter);
    specialization_label.innerHTML = 'Spezialisierung:';

    let specialization_select = document.createElement('select');
    specialization_select.setAttribute('id', 'select-specialization-' + counter);
    specialization_select.setAttribute('name', 'specializations');
    specialization_select.setAttribute('required', 'true');

    let priority_cell = document.createElement('div');
    priority_cell.classList.add('cell', 'small-10', 'medium-2');

    let priority_label = document.createElement('label');
    priority_label.setAttribute('for', 'priority-' + counter);
    priority_label.innerHTML = 'Priorität:';

    let priority_input = document.createElement('input');
    priority_input.setAttribute('id', 'priority-' + counter);
    priority_input.setAttribute('type', 'number');
    priority_input.setAttribute('name', 'priority');
    priority_input.setAttribute('required', 'true');

    let button_cell = document.createElement('div');
    button_cell.classList.add('cell', 'small-2', 'medium-1', 'text-center');

    let button = document.createElement('button');
    button.classList.add('button', 'alert');
    button.setAttribute('id', 'delete-specialization-' + counter);
    button.setAttribute('type', 'button');
    button.setAttribute('onclick', 'delete_select_specialization(this.id)');
    button.setAttribute('style', 'margin-top: 24px');

    let button_icon = document.createElement('i');
    button_icon.classList.add('fas', 'fa-minus-square');

    // Fügen wir das ganze zusammen...
    specialization_cell.appendChild(specialization_label);
    specialization_cell.appendChild(specialization_select);

    priority_cell.appendChild(priority_label);
    priority_cell.appendChild(priority_input);

    button.appendChild(button_icon);
    button_cell.appendChild(button);

    grid.appendChild(specialization_cell);
    grid.appendChild(priority_cell);
    grid.appendChild(button_cell);

    // Bringen wir das ganze auf die Seite...
    document.getElementById('priority-container').appendChild(grid);

    // Neue Auswahlmöglichkeit mit Optionen füllen
    load_specializations(counter);
}

// Delete specific select field for specializations
function delete_select_specialization(id) {
    let splitted_id = id.split('-');
    let select_specialization = document.getElementById('select-specialization-' + splitted_id[2]);

    let grid = select_specialization.parentElement.parentElement;
    let specialization_cell = select_specialization.parentElement;
    let priority_cell = specialization_cell.nextElementSibling;
    let button_cell = priority_cell.nextElementSibling;

    while (specialization_cell.firstChild) {
        specialization_cell.removeChild(specialization_cell.lastChild);
    }

    while (priority_cell.firstChild) {
        priority_cell.removeChild(priority_cell.lastChild);
    }

    while (button_cell.firstChild) {
        button_cell.removeChild(button_cell.lastChild);
    }

    while (grid.firstChild) {
        grid.removeChild(grid.lastChild);
    }
}

// Get specializations with ajax request and populate select field
function load_specializations(id) {
    $.ajax({
        type: "GET",
        url: '/ajax/specializations',
        success: function (data) {
            let select = document.getElementById('select-specialization-' + id);

            if (data.length === 0 || data === {} || $.isEmptyObject(data)) {
                let option = document.createElement('option');
                option.setAttribute('disabled', 'true');
                option.innerHTML = 'Nichts gefunden!';
                select.appendChild(option);
            } else {
                for (let count = 0; count < data.length; count++) {
                    let option = document.createElement('option');
                    option.setAttribute('value', data[count][0]);
                    option.innerHTML = data[count][1] + ' - ' + data[count][2];
                    select.appendChild(option);
                }
            }
        }
    });
}

// Get entitlements with ajax request and create + populate select and priority fields (+ delete button)
function load_entitlements(id) {
    // Clear all select specialization fields except for the first one
    clear_all_select_specializations();

    $.ajax({
        type: "GET",
        url: '/ajax/entitlements?id=' + id,
        success: function (data) {
            // If ajax request found nothing
            if (data.length === 0 || data === {} || $.isEmptyObject(data)) {
                // Reset values of first select and priority field
                document.getElementById('select-specialization-1').selectIndex = 0;
                document.getElementById('priority-1').value = '';
            } else {
                for (let count = 0; count < data.length - 1; count++) {
                    // Add select field for specializations for each entitlement - 1
                    add_select_specialization();
                }

                let specialization_selects = document.getElementsByName('specializations');
                let priorities = document.getElementsByName('priority');

                // Timeout 200ms
                setTimeout(function () {
                    // Set values of select and priority field just created
                    for (let count = 0; count < data.length; count++) {
                        specialization_selects[count].value = data[count][2];
                        priorities[count].value = data[count][3];
                    }
                }, 200);
            }
        }
    })
}

function clear_all_select_specializations() {
    let specialization_selects = document.getElementsByName('specializations');

    for (let count = specialization_selects.length - 1; count > 0; count--) {
        delete_select_specialization(specialization_selects[count].id);
    }
}