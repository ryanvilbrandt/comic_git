import { new_lines_to_array } from "./utils.js";

export async function load_archive() {
    let sections_promise = fetch_archive_sections();
    let json_list_promise = fetch_all_json_data();
    let sections = await sections_promise;
    let json_list = await json_list_promise;
    build_archive_list(sections, json_list);
}

async function fetch_archive_sections() {
    let response = await fetch("./comics/archive_sections.txt");
    console.log("Fetched archive sections");
    let text = await response.text();
    return new_lines_to_array(text);
}

async function fetch_all_json_data() {
    let response = await fetch("./comics/directory_list.txt");
    console.log("Fetched directory list");
    let text = await response.text();
    let directory_list = new_lines_to_array(text);
    console.log(directory_list);
    let json_dicts = await Promise.all(directory_list.map(i => fetch_json_data(i)));
    let new_obj = {};
    for (let i=0; i < json_dicts.length; i++) {
        new_obj[directory_list[i]] = json_dicts[i];
    }
    return new_obj;
}

async function fetch_json_data(comic_num) {
    let response = await fetch("./comics/" + comic_num + "/info.json");
    console.log("Fetched " + comic_num);
    return response.json();
}

function build_archive_list(sections, json_list) {
    let html = "<div id='archive-list'>\n";
    html += "<ul>\n";
    if (sections.length === 0) {
        Object.keys(json_list).forEach(key => {
            html += build_page_link(key, json_list[key]);
        });
    } else {
        sections.forEach(section => {
            html += "    <li>" + section + "\n";
            html += "    <ul>";
            Object.keys(json_list).forEach(key => {
                let comic = json_list[key];
                if (comic["tags"].includes(section)) {
                    html += build_page_link(key, comic);
                }
            });
            html += "    </ul></li>";
        });
    }
    html += "</ul>";
    html += "</div>";
    document.getElementById("archives").innerHTML = html;
}

function build_page_link(comic_id, comic_json) {
    let html = "        <li><a href='index?id=" + comic_id + "'>" + comic_json["title"] + "</a>";
    html += " -- " + comic_json["post_date"] +"</li>\n";
    return html;
}