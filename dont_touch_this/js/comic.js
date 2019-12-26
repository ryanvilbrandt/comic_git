import { find_get_parameter, new_lines_to_array, load_links_bar } from "./utils.js";

export async function load_page() {
    await Promise.all([load_links_bar(), load_comic_data()]);
}

async function load_comic_data() {
    let response = await fetch("./your_content/directory_list.txt");
    if (!response.ok) {
        console.log("Error when fetching " + response.url + ": " + response.status + " " + response.statusText);
        return
    }
    let text = await response.text();
    let directory_list = new_lines_to_array(text);
    let current_index = get_current_index(directory_list);
    let directory = "./your_content/comics/" + directory_list[current_index] + "/";
    let info_response = await fetch(directory + "info.json");
    let post_response = await fetch(directory + "post.html");
    let next_id = load_navigation_bar(directory_list, current_index);

    let json = await info_response.json();
    load_title(json["title"]);
    load_post_date(json["post_date"]);
    load_comic_image(directory + json["filename"], json["alt_text"], next_id);
    load_tags(json["tags"]);
    load_post_body(await post_response.text());
}

function get_current_index(directory_list) {
    let current_id = find_get_parameter("id");
    return (current_id == null) ? directory_list.length - 1 : directory_list.indexOf(current_id);
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
            <a class="navigation-button" href="index.html?id=` + first_id + `">First</a>
        </td>
        <td id="navigation-button-previous">
            <a class="navigation-button" href="index.html?id=` + previous_id + `">Previous</a>
        </td>
        <td id="navigation-button-next">
            <a class="navigation-button" href="index.html?id=` + next_id + `">Next</a>
        </td>
        <td id="navigation-button-last">
            <a class="navigation-button" href="index.html?id=` + last_id + `">Last</a>
        </td>
    </tr>
</table>`;
    return next_id;  // Return so that the comic page itself can be a link
}

function load_title(title) {
    document.getElementById("comic-title").innerHTML = title;
}

function load_post_date(post_date) {
    document.getElementById("post-date").innerHTML = "Posted on: " + post_date;
}

function load_comic_image(path, alt_text, next_id) {
    let html = '<a href="index.html?id=' + next_id + '">';
    html += '<img id="comic-image" src="' + path + '" title="' + alt_text + '"/>';
    html += "</a>";
    document.getElementById("comic-page").innerHTML = html;
}

function load_tags(tags) {
    let tag_links = tags.map(t => '<a href="tagged.html?tag=' + t + '">' + t + '</a>');
    document.getElementById("tags").innerHTML = "Tags: " + tag_links.join(", ");
}

function load_post_body(post_body) {
    document.getElementById("post-body").innerHTML = post_body;
}
