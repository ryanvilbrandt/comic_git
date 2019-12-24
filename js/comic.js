import { find_get_parameter } from "/js/utils.js";

export async function load_comic_data() {
    let response = await fetch("comics/directory_list");
    let text = await response.text();
    let directory_list = new_lines_to_int_array(text);
    let current_index = get_current_index(directory_list);
    let directory = "comics/" + directory_list[current_index] + "/";
    let info_response = await fetch(directory + "info.json");
    let post_response = await fetch(directory + "post.html");
    load_navigation_bar(directory_list, current_index);

    let json = await info_response.json();
    console.log(json);
    load_title(json["title"]);
    load_post_date(json["post_date"]);
    load_comic_tag(directory + json["filename"], json["alt_text"]);
    load_tags(json["tags"]);
    load_post_body(await post_response.text());
}

function new_lines_to_int_array(s) {
    return s.trim().split('\r\n').map(x => parseInt(x.trim()));
}

function get_current_index(directory_list) {
    let current_id = find_get_parameter("id");
    return (current_id == null) ? directory_list.length - 1 : directory_list.indexOf(parseInt(current_id));
}

function load_navigation_bar(directory_list, current_index) {
    let first_id = directory_list[0];
    let last_id = directory_list[directory_list.length - 1];
    let previous_id = (current_index === 0) ? first_id : directory_list[current_index - 1];
    let next_id = (current_index === directory_list.length - 1) ? last_id : directory_list[current_index + 1];
    console.log(first_id);
    console.log(previous_id);
    console.log(next_id);
    console.log(last_id);
    document.getElementById("navigation-bar").innerHTML = `<table id="navigation-buttons">
    <tr>
        <td id="navigation-button-first">
            <a href="index.html?id=` + first_id + `">&lt;&lt;</a>
        </td>
        <td id="navigation-button-previous">
            <a href="index.html?id=` + previous_id + `">&lt;</a>
        </td>
        <td id="navigation-button-next">
            <a href="index.html?id=` + next_id + `">&gt;</a>
        </td>
        <td id="navigation-button-last">
            <a href="index.html?id=` + last_id + `">&gt;&gt;</a>
        </td>
    </tr>
</table>`;
}

function load_title(title) {
    document.getElementById("comic-title").innerHTML = title;
}

function load_post_date(post_date) {
    document.getElementById("post-date").innerHTML = "Posted on: " + post_date;
}

function load_comic_tag(path, alt_text) {
    document.getElementById("comic-page").innerHTML =
        '<img id="comic-image" src="' + path + '" alt="' + alt_text + '"/>';
}

function load_tags(tags) {
    document.getElementById("tags").innerHTML = "Tags: " + tags.join(", ");
}

function load_post_body(post_body) {
    document.getElementById("post-body").innerHTML = post_body;
}
