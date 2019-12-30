import { new_lines_to_array, load_links_bar, load_title } from "./utils.js";

export async function load_page() {
    await Promise.all([load_title("Archive"), load_links_bar(), load_archive()]);
}

async function load_archive() {
    let sections_promise = fetch_archive_sections();
    let json_list_promise = fetch_all_json_data();
    let sections = await sections_promise;
    let json_list = await json_list_promise;
    build_archive_list(sections, json_list);
}

async function fetch_archive_sections() {
    let path = "./your_content/archive_sections.txt";
    let response = await fetch(path);
    if (response.status === 404) {
        console.log("Could not find the file " + "./your_content/archive_sections.txt");
        return [];
    }
    console.log("Fetched archive sections");
    let text = await response.text();
    return new_lines_to_array(text);
}

async function fetch_all_json_data() {
    let response = await fetch("./your_content/directory_list.txt");
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
    let response = await fetch("./your_content/comics/" + comic_num + "/info.json");
    console.log("Fetched " + comic_num);
    return response.json();
}

function build_archive_list(sections, json_list) {
    let html = "<ul>\n";
    if (sections.length === 0) {
        Object.keys(json_list).forEach(key => {
            html += build_page_link(key, json_list[key]);
        });
    } else {
        sections.forEach(section => {
            console.log("Building section " + section);
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
    document.getElementById("archives").innerHTML = html;
}

function build_page_link(comic_id, comic_json) {
    let html = "        <li><a href='index.html?id=" + comic_id + "'>" + comic_json["title"] + "</a>";
    html += " -- " + comic_json["post_date"] +"</li>\n";
    return html;
}