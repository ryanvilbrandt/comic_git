import { new_lines_to_array, find_get_parameter } from "./utils.js";

export async function load_tagged() {
    let json_list_promise = fetch_all_json_data();
    let json_list = await json_list_promise;
    let tag = find_get_parameter("tag");
    build_tagged_list(json_list, tag);
    document.getElementById("page-title").innerText = 'Posts tagged with "' + tag + '"';
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

function build_tagged_list(json_list, tag) {
    let html = "<ul>";
    Object.keys(json_list).forEach(key => {
        let comic = json_list[key];
        if (comic["tags"].includes(tag)) {
            html += build_page_link(key, comic);
        }
    });
    html += "</ul>";
    document.getElementById("tagged").innerHTML = html;
}

function build_page_link(comic_id, comic_json) {
    let html = "        <li><a href='index.html?id=" + comic_id + "'>" + comic_json["title"] + "</a>";
    html += " -- " + comic_json["post_date"] +"</li>\n";
    return html;
}