import { ajax_call, find_get_parameter } from "/js/utils.js";

export function load_comic_data() {
    ajax_call("comics/directory_list", load_directory_list);
}

let current_id;

function load_directory_list(xhttp) {
    let directory_list = xhttp.responseText.trim().split('\r\n').map(x => parseInt(x.trim()));
    let current_index = get_current_index(directory_list);
    document.getElementById("navigation-bar").innerHTML = build_navigation_bar(directory_list, current_index);
    current_id = directory_list[current_index];
    ajax_call("comics/" + current_id + "/info.json", load_comic_elements);
}

function get_current_index(directory_list) {
    let current_id = find_get_parameter("id");
    return (current_id == null) ? directory_list.length - 1 : directory_list.indexOf(parseInt(current_id));
}

function build_navigation_bar(directory_list, current_index) {
    let first_id = directory_list[0];
    let last_id = directory_list[directory_list.length - 1];
    let previous_id = (current_index === 0) ? first_id : directory_list[current_index - 1];
    let next_id = (current_index === directory_list.length - 1) ? last_id : directory_list[current_index + 1];
    console.log(first_id);
    console.log(previous_id);
    console.log(next_id);
    console.log(last_id);
    return `<table class="navigation-buttons">
    <tr>
        <td class="navigation-button-first">
            <a href="index.html?id=` + first_id + `">&lt;&lt;</a>
        </td>
        <td class="navigation-button-previous">
            <a href="index.html?id=` + previous_id + `">&lt;</a>
        </td>
        <td class="navigation-button-next">
            <a href="index.html?id=` + next_id + `">&gt;</a>
        </td>
        <td class="navigation-button-last">
            <a href="index.html?id=` + last_id + `">&gt;&gt;</a>
        </td>
    </tr>
</table>`;
}

function load_comic_elements(xhttp) {
    let comic_info = JSON.parse(xhttp.responseText);

}

function build_comic_tag(path, alt_text) {
    return '<img class="comic-page" src="' + path.toString() + '" alt="' + alt_text.toString() + '"/>';
}

function build_navigation_buttons_tag(path, alt_text) {
    return '<img class="comic-page" src="' + path.toString() + '" alt="' + alt_text.toString() + '"/>';
}
